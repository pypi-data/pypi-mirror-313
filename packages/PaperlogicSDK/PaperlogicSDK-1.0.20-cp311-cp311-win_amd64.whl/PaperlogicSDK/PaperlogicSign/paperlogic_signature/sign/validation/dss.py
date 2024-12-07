import hashlib
from dataclasses import dataclass
from dataclasses import field as data_field
from typing import Iterable, Optional

from asn1crypto import crl as asn1_crl
from asn1crypto import ocsp as asn1_ocsp
from asn1crypto import x509
from asn1crypto.x509 import Certificate
from ....paperlogic_certvalidator import ValidationContext
from ....paperlogic_certvalidator.path import ValidationPath

from ...pdf_utils import generic
from ...pdf_utils.generic import pdf_name
from ...pdf_utils.incremental_writer import IncrementalPdfFileWriter
from ...pdf_utils.misc import get_and_apply
from ...pdf_utils.rw_common import PdfHandler
from ...pdf_utils.writer import BasePdfFileWriter

from .errors import NoDSSFoundError, ValidationInfoReadingError

from ...pdf_utils.crypt import SerialisedCredential

__all__ = [
    'VRI',
    'DocumentSecurityStore',
    'enumerate_ocsp_certs',
]

@dataclass
class VRI:
    """
    VRI dictionary as defined in PAdES / ISO 32000-2.
    These dictionaries collect data that may be relevant for the validation of
    a specific signature.

    .. note::
        The data are stored as PDF indirect objects, not asn1crypto values.
        In particular, values are tied to a specific PDF handler.
    """

    certs: set = data_field(default_factory=set)
    """
    Relevant certificates.
    """

    ocsps: set = data_field(default_factory=set)
    """
    Relevant OCSP responses.
    """

    crls: set = data_field(default_factory=set)
    """
    Relevant CRLs.
    """

    def as_pdf_object(self) -> generic.DictionaryObject:
        """
        :return:
            A PDF dictionary representing this VRI entry.
        """
        vri = generic.DictionaryObject({pdf_name('/Type'): pdf_name('/VRI')})
        if self.ocsps:
            vri[pdf_name('/OCSP')] = generic.ArrayObject(self.ocsps)
        if self.crls:
            vri[pdf_name('/CRL')] = generic.ArrayObject(self.crls)
        vri[pdf_name('/Cert')] = generic.ArrayObject(self.certs)
        return vri


def enumerate_ocsp_certs(ocsp_response):
    """
    Essentially nabbed from _extract_ocsp_certs in ValidationContext
    """

    status = ocsp_response['response_status'].native
    if status == 'successful':
        response_bytes = ocsp_response['response_bytes']
        if response_bytes['response_type'].native == 'basic_ocsp_response':
            response = response_bytes['response'].parsed
            yield from response['certs']

class DocumentSecurityStore:
    """
    Representation of a DSS in Python.
    """

    def __init__(
        self,
        writer: Optional[BasePdfFileWriter],
        certs=None,
        ocsps=None,
        crls=None,
        vri_entries=None,
        backing_pdf_object=None,
    ):
        self.vri_entries = vri_entries if vri_entries is not None else {}
        self.certs = certs if certs is not None else {}
        self.ocsps = ocsps if ocsps is not None else []
        self.crls = crls if crls is not None else []

        self.writer = writer
        self.backing_pdf_object = (
            backing_pdf_object
            if backing_pdf_object is not None
            else generic.DictionaryObject()
        )

        ocsps_seen = {}
        for ocsp_ref in self.ocsps:
            ocsp_bytes = ocsp_ref.get_object().data
            ocsps_seen[ocsp_bytes] = ocsp_ref
        self._ocsps_seen = ocsps_seen

        crls_seen = {}
        for crl_ref in self.crls:
            crl_bytes = crl_ref.get_object().data
            crls_seen[crl_bytes] = crl_ref
        self._crls_seen = crls_seen
        self._modified = False

    @property
    def modified(self):
        return self._modified

    def _mark_modified(self):
        if not self._modified:
            self._modified = True
            if self.backing_pdf_object is not None:
                self.writer.update_container(self.backing_pdf_object)

    def _cms_objects_to_streams(self, objs, seen, dest):
        for obj in objs:
            obj_bytes = obj.dump()
            try:
                yield seen[obj_bytes]
            except KeyError:
                ref = self.writer.add_object(
                    generic.StreamObject(stream_data=obj_bytes)
                )
                self._mark_modified()
                seen[obj_bytes] = ref
                dest.append(ref)
                yield ref

    def _embed_certs_from_ocsp(self, ocsps):
        def extra_certs():
            for resp in ocsps:
                yield from enumerate_ocsp_certs(resp)

        return [self._embed_cert(cert_) for cert_ in extra_certs()]

    def _embed_cert(self, cert):
        if self.writer is None:
            raise TypeError('This DSS does not support updates.')

        try:
            return self.certs[cert.issuer_serial]
        except KeyError:
            pass

        ref = self.writer.add_object(
            generic.StreamObject(stream_data=cert.dump())
        )
        self._mark_modified()
        self.certs[cert.issuer_serial] = ref
        return ref

    @staticmethod
    def sig_content_identifier(contents) -> generic.NameObject:
        """
        Hash the contents of a signature object to get the corresponding VRI
        identifier.

        This is internal API.

        :param contents:
            Signature contents.
        :return:
            A name object to put into the DSS.
        """
        ident = hashlib.sha1(contents).digest().hex().upper()
        return pdf_name('/' + ident)

    def register_vri(self, identifier, *, certs=(), ocsps=(), crls=()):
        """
        Register validation information for a set of signing certificates
        associated with a particular signature.

        :param identifier:
            Identifier of the signature object (see `sig_content_identifier`).
            If ``None``, only embed the data into the DSS without associating
            it with any VRI.
        :param certs:
            Certificates to add.
        :param ocsps:
            OCSP responses to add.
        :param crls:
            CRLs to add.
        """

        if self.writer is None:
            raise TypeError('This DSS does not support updates.')

        ocsps = list(ocsps)
        crls = list(crls)

        ocsp_refs = set()
        crl_refs = set()
        cert_refs = {self._embed_cert(cert) for cert in certs}
        if ocsps:
            ocsp_refs = set(
                self._cms_objects_to_streams(
                    ocsps, self._ocsps_seen, self.ocsps
                )
            )
        if crls:
            crl_refs = set(
                self._cms_objects_to_streams(crls, self._crls_seen, self.crls)
            )
        # TODO while somewhat less common, CRL signing can also be delegated
        #  we should take that into account
        cert_refs.update(set(self._embed_certs_from_ocsp(ocsps)))

        # TODO do a better job of determining whether the VRI dictionary even
        #  needs updating.
        if identifier is not None:
            vri = VRI(certs=cert_refs, ocsps=ocsp_refs, crls=crl_refs)
            self.vri_entries[identifier] = self.writer.add_object(
                vri.as_pdf_object()
            )
            self._mark_modified()

    def as_pdf_object(self):
        """
        Convert the :class:`.DocumentSecurityStore` object to a python
        dictionary. This method also handles DSS updates.

        :return:
            A PDF object representing this DSS.
        """
        pdf_dict = self.backing_pdf_object
        pdf_dict['/Certs'] = generic.ArrayObject(list(self.certs.values()))
        if self.vri_entries:
            pdf_dict['/VRI'] = generic.DictionaryObject(self.vri_entries)

        if self.ocsps:
            pdf_dict[pdf_name('/OCSPs')] = generic.ArrayObject(self.ocsps)

        if self.crls:
            pdf_dict[pdf_name('/CRLs')] = generic.ArrayObject(self.crls)

        return pdf_dict

    def load_certs(self) -> Iterable[x509.Certificate]:
        """
        Return a generator that parses and yields all certificates in the DSS.

        :return:
            A generator yielding :class:`.Certificate` objects.
        """
        for cert_ref in self.certs.values():
            cert_stream: generic.StreamObject = cert_ref.get_object()
            cert = Certificate.load(cert_stream.data)
            yield cert

    def as_validation_context(
        self, validation_context_kwargs, include_revinfo=True
    ) -> ValidationContext:
        """
        Construct a validation context from the data in this DSS.

        :param validation_context_kwargs:
            Extra kwargs to pass to the ``__init__`` function.
        :param include_revinfo:
            If ``False``, revocation info is skipped.
        :return:
            A validation context preloaded with information from this DSS.
        """

        validation_context_kwargs = dict(validation_context_kwargs)
        extra_certs = validation_context_kwargs.pop('other_certs', [])
        certs = list(self.load_certs()) + extra_certs

        if include_revinfo:
            ocsps = list(validation_context_kwargs.pop('ocsps', ()))
            for ocsp_ref in self.ocsps:
                ocsp_stream: generic.StreamObject = ocsp_ref.get_object()
                resp = asn1_ocsp.OCSPResponse.load(ocsp_stream.data)
                ocsps.append(resp)
            validation_context_kwargs['ocsps'] = ocsps

            crls = list(validation_context_kwargs.pop('crls', ()))
            for crl_ref in self.crls:
                crl_stream: generic.StreamObject = crl_ref.get_object()
                crl = asn1_crl.CertificateList.load(crl_stream.data)
                crls.append(crl)
            validation_context_kwargs['crls'] = crls

        return ValidationContext(other_certs=certs, **validation_context_kwargs)

    @classmethod
    def read_dss(cls, handler: PdfHandler) -> 'DocumentSecurityStore':
        """
        Read a DSS record from a file and add the data to a validation context.

        :param handler:
            PDF handler from which to read the DSS.
        :return:
            A DocumentSecurityStore object describing the current state of the
            DSS.
        """
        try:
            dss_dict = handler.root['/DSS']
        except KeyError as e:
            raise NoDSSFoundError() from e

        cert_refs = {}
        cert_ref_list = get_and_apply(dss_dict, '/Certs', list, default=[])
        for cert_ref in cert_ref_list:
            cert_stream: generic.StreamObject = cert_ref.get_object()
            cert: Certificate = Certificate.load(cert_stream.data)
            cert_refs[cert.issuer_serial] = cert_ref

        ocsp_refs = get_and_apply(dss_dict, '/OCSPs', list, default=[])
        ocsps = []
        for ocsp_ref in ocsp_refs:
            ocsp_stream: generic.StreamObject = ocsp_ref.get_object()
            resp = asn1_ocsp.OCSPResponse.load(ocsp_stream.data)
            ocsps.append(resp)

        crl_refs = get_and_apply(dss_dict, '/CRLs', list, default=[])
        crls = []
        for crl_ref in crl_refs:
            crl_stream: generic.StreamObject = crl_ref.get_object()
            crl = asn1_crl.CertificateList.load(crl_stream.data)
            crls.append(crl)

        # shallow-copy the VRI dictionary
        try:
            vri_entries = dict(dss_dict['/VRI'])
        except KeyError:
            vri_entries = None

        # if the handler is a writer, the DSS will support updates
        if isinstance(handler, BasePdfFileWriter):
            writer = handler
        else:
            writer = None

        # the DSS returned will be backed by the original DSS object, so CRLs
        # are automagically preserved if they happened to be included in
        # the original file
        dss = cls(
            writer=writer,
            certs=cert_refs,
            ocsps=ocsp_refs,
            vri_entries=vri_entries,
            crls=crl_refs,
            backing_pdf_object=dss_dict,
        )
        return dss

    @classmethod
    def supply_dss_in_writer(
        cls,
        pdf_out: BasePdfFileWriter,
        sig_contents,
        *,
        certs=None,
        ocsps=None,
        crls=None,
        paths=None,
        validation_context=None,
        embed_roots: bool = True,
    ) -> 'DocumentSecurityStore':
        """
        Add or update a DSS, and optionally associate the new information with a
        VRI entry tied to a signature object.

        You can either specify the CMS objects to include directly, or
        pass them in as output from `paperlogic_certvalidator`.

        :param pdf_out:
            PDF writer to write to.
        :param sig_contents:
            Contents of the new signature (used to compute the VRI hash), as
            a hexadecimal string, including any padding.
            If ``None``, the information will not be added to any VRI
            dictionary.
        :param certs:
            Certificates to include in the VRI entry.
        :param ocsps:
            OCSP responses to include in the VRI entry.
        :param crls:
            CRLs to include in the VRI entry.
        :param paths:
            Validation paths that have been established, and need to be added
            to the DSS.
        :param validation_context:
            Validation context from which to draw OCSP responses and CRLs.
        :param embed_roots:
            .. versionadded:: 0.9.0

            Option that controls whether the root certificate of each validation
            path should be embedded into the DSS. The default is ``True``.

            .. note::
                Trust roots are configured by the validator, so embedding them
                typically does nothing in a typical validation process.
                Therefore they can be safely omitted in most cases.
                Nonetheless, embedding the roots can be useful for documentation
                purposes.

            .. warning::
                This only applies to paths, not the ``certs`` parameter.

        :return:
            a :class:`DocumentSecurityStore` object containing both the new
            and existing contents of the DSS (if any).
        """
        try:
            dss = cls.read_dss(pdf_out)
            created = False
        except ValidationInfoReadingError:
            created = True
            dss = cls(writer=pdf_out)

        if sig_contents is not None:
            identifier = DocumentSecurityStore.sig_content_identifier(
                sig_contents
            )
        else:
            identifier = None

        def _certs() -> Iterable[x509.Certificate]:
            yield from certs or ()
            path: ValidationPath
            for path in paths or ():
                path_parts = iter(path)
                if not embed_roots:
                    # skip the first cert (i.e. the root)
                    next(path_parts)
                yield from path_parts

        def _ocsps():
            yield from ocsps or ()
            if validation_context is not None:
                yield from validation_context.ocsps

        def _crls():
            yield from crls or ()
            if validation_context is not None:
                yield from validation_context.crls

        dss.register_vri(
            identifier, certs=_certs(), ocsps=_ocsps(), crls=_crls()
        )
        dss_dict = dss.as_pdf_object()
        # if we're updating the DSS, this is all we need to do.
        # if we're adding a fresh DSS, we need to register it.

        if created:
            dss_ref = pdf_out.add_object(dss_dict)
            pdf_out.root[pdf_name('/DSS')] = dss_ref
            pdf_out.update_root()
        return dss

    @classmethod
    def add_dss(
        cls,
        output_stream,
        sig_contents,
        *,
        certs=None,
        ocsps=None,
        crls=None,
        paths=None,
        validation_context=None,
        force_write: bool = False,
        embed_roots: bool = True,
        file_credential: Optional[SerialisedCredential] = None,
    ):
        """
        Wrapper around :meth:`supply_dss_in_writer`.

        The result is applied to the output stream as an incremental update.

        :param output_stream:
            Output stream to write to.
        :param sig_contents:
            Contents of the new signature (used to compute the VRI hash), as
            a hexadecimal string, including any padding.
            If ``None``, the information will not be added to any VRI
            dictionary.
        :param certs:
            Certificates to include in the VRI entry.
        :param ocsps:
            OCSP responses to include in the VRI entry.
        :param crls:
            CRLs to include in the VRI entry.
        :param paths:
            Validation paths that have been established, and need to be added
            to the DSS.
        :param force_write:
            Force a write even if the DSS doesn't have any new content.
        :param validation_context:
            Validation context from which to draw OCSP responses and CRLs.
        :param embed_roots:
            .. versionadded:: 0.9.0

            Option that controls whether the root certificate of each validation
            path should be embedded into the DSS. The default is ``True``.

            .. note::
                Trust roots are configured by the validator, so embedding them
                typically does nothing in a typical validation process.
                Therefore they can be safely omitted in most cases.
                Nonetheless, embedding the roots can be useful for documentation
                purposes.

            .. warning::
                This only applies to paths, not the ``certs`` parameter.
        :param file_credential:
            .. versionadded:: 0.13.0

            Serialised file credential, to update encrypted files.
        """
        pdf_out = IncrementalPdfFileWriter(output_stream)
        if pdf_out.security_handler is not None and file_credential is not None:
            pdf_out.security_handler.authenticate(file_credential)
        dss = cls.supply_dss_in_writer(
            pdf_out,
            sig_contents,
            certs=certs,
            ocsps=ocsps,
            crls=crls,
            paths=paths,
            validation_context=validation_context,
            embed_roots=embed_roots,
        )
        if force_write or dss.modified:
            pdf_out.write_in_place()
