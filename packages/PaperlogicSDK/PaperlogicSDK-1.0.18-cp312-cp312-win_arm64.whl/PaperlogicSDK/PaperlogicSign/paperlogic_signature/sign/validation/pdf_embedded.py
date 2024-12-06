import os
from typing import Optional, List, Union
from collections import namedtuple
from datetime import datetime
from asn1crypto import cms, x509

from ...pdf_utils import generic, misc
from ...pdf_utils.generic import pdf_name, TextStringObject
from ...pdf_utils.reader import PdfFileReader, process_data_at_eof
from ...sign.fields import (
    MDPPerm,
)

from .generic_cms import (
    compute_signature_tst_digest,
    extract_certs_for_validation,
    extract_self_reported_ts,
    extract_tst_data
)
from ....paperlogic_signature.sign.fields import (
    FieldMDPSpec,
    MDPPerm,
    SigSeedValueSpec,
)
from ....paperlogic_signature.sign.general import (
    SignedDataCerts,
    byte_range_digest,
    extract_signer_info,
)
from ....paperlogic_signature.sign.diff_analysis import (
    DEFAULT_DIFF_POLICY,
    DiffPolicy,
    DiffResult,
    ModificationLevel,
    SuspiciousModification,
)
from .status import (
    SignatureCoverageLevel,
)

from .errors import (
    SignatureValidationError,
)

__all__ = [
    'DocMDPInfo',
    'read_certification_data',
    'extract_contents'
]


DocMDPInfo = namedtuple('DocMDPInfo', ['permission', 'author_sig'])

def extract_contents(sig_object: generic.DictionaryObject):
    """
    Internal function to extract the (DER-encoded) signature bytes from a PDF
    signature dictionary.

    :param sig_object:
        A signature dictionary.
    :return:
        The extracted contents as a byte string.
    """

    try:
        cms_content = sig_object.raw_get(
            '/Contents', decrypt=generic.EncryptedObjAccess.RAW
        )
    except KeyError:
        raise misc.PdfReadError('Could not read /Contents entry in signature')

    if not isinstance(
        cms_content, (generic.TextStringObject, generic.ByteStringObject)
    ):
        raise misc.PdfReadError('/Contents must be string-like')
    return cms_content.original_bytes

class EmbeddedPdfSignature:
    """
    Class modelling a signature embedded in a PDF document.
    """

    sig_field: generic.DictionaryObject
    """
    The field dictionary of the form field containing the signature.
    """

    sig_object: generic.DictionaryObject
    """
    The signature dictionary.
    """

    signed_data: cms.SignedData
    """
    CMS signed data in the signature.
    """

    def __init__(
        self,
        reader: PdfFileReader,
        sig_field: generic.DictionaryObject,
        fq_name: Union[str, TextStringObject],
    ):
        self.reader = reader
        if isinstance(sig_field, generic.IndirectObject):
            sig_field = sig_field.get_object()
        self.sig_field = sig_field
        sig_object_ref = sig_field.raw_get('/V')
        self.sig_object = sig_object = sig_object_ref.get_object()
        assert isinstance(sig_object, generic.DictionaryObject)
        try:
            self.byte_range = sig_object.raw_get('/ByteRange')
        except KeyError:
            raise misc.PdfReadError(
                'Could not read /ByteRange entry in signature'
            )
        self.pkcs7_content = cms_content = extract_contents(sig_object)

        message = cms.ContentInfo.load(cms_content)
        signed_data = message['content']
        self.signed_data: cms.SignedData = signed_data

        self.signer_info = extract_signer_info(signed_data)
        self._sd_cert_info: Optional[SignedDataCerts] = None

        # The PDF standard does not define a way to specify the digest algorithm
        # used other than this one.
        # However, RFC 5652 § 11.2 states that the message_digest attribute
        # (which in our case is the PDF's ByteRange digest) is to be computed
        # using the signer's digest algorithm. This can only refer
        # to the corresponding SignerInfo entry.
        digest_algo = self.signer_info['digest_algorithm']
        self.md_algorithm = digest_algo['algorithm'].native.lower()
        eci = signed_data['encap_content_info']
        content_type = eci['content_type'].native
        if content_type == 'data':
            # Case of a normal signature
            self.external_md_algorithm = self.md_algorithm
        elif content_type == 'tst_info':
            # for timestamps, the hash algorithm in the messageImprint
            # need not be the same as the one to digest the encapsulated data!
            # RFC 8933 recommends to unify them, but it's not a given.
            mi = eci['content'].parsed['message_imprint']
            self.external_md_algorithm = mi['hash_algorithm'][
                'algorithm'
            ].native

        # grab the revision to which the signature applies
        # NOTE: We're using get_last_change here as opposed to
        # get_introducing_revision. The distinction won't be relevant in most
        # legitimate use cases, but get_last_change is more likely to be correct
        # in cases where the signature obj was created by overriding an existing
        # object (which is weird, but technically possible, I guess).
        # Important note: the coverage checker will validate whether the
        # xref table for that revision is actually covered by the signature,
        # and raise the alarm if that's not the case.
        # Therefore shenanigans with updating signature objects will be detected
        # even before the diff checker runs.
        self.signed_revision = self.reader.xrefs.get_last_change(
            sig_object_ref.reference
        )
        self.coverage = None
        self.external_digest: Optional[bytes] = None
        self.total_len: Optional[int] = None
        self._docmdp: Optional[MDPPerm] = None
        self._fieldmdp: Optional[FieldMDPSpec] = None
        self._docmdp_queried = self._fieldmdp_queried = False
        self.tst_signature_digest: Optional[bytes] = None

        self.diff_result = None
        self._integrity_checked = False
        self.fq_name = fq_name

    def _init_cert_info(self) -> SignedDataCerts:
        if self._sd_cert_info is None:
            self._sd_cert_info = extract_certs_for_validation(self.signed_data)
        return self._sd_cert_info

    @property
    def embedded_attr_certs(self) -> List[cms.AttributeCertificateV2]:
        """
        Embedded attribute certificates.
        """
        return list(self._init_cert_info().attribute_certs)

    @property
    def other_embedded_certs(self) -> List[x509.Certificate]:
        """
        Embedded X.509 certificates, excluding than that of the signer.
        """
        return list(self._init_cert_info().other_certs)

    @property
    def signer_cert(self) -> x509.Certificate:
        """
        Certificate of the signer.
        """
        return self._init_cert_info().signer_cert

    @property
    def sig_object_type(self) -> generic.NameObject:
        """
        Returns the type of the embedded signature object.
        For ordinary signatures, this will be ``/Sig``.
        In the case of a document timestamp, ``/DocTimeStamp`` is returned.

        :return:
            A PDF name object describing the type of signature.
        """
        return self.sig_object.get('/Type', pdf_name('/Sig'))

    @property
    def field_name(self):
        """
        :return:
            Name of the signature field.
        """
        return self.fq_name

    @property
    def self_reported_timestamp(self) -> Optional[datetime]:
        """
        :return:
            The signing time as reported by the signer, if embedded in the
            signature's signed attributes or provided as part of the signature
            object in the PDF document.
        """
        ts = extract_self_reported_ts(self.signer_info)
        if ts is not None:
            return ts

        try:
            st_as_pdf_date = self.sig_object['/M']
            return generic.parse_pdf_date(
                st_as_pdf_date, strict=self.reader.strict
            )
        except KeyError:  # pragma: nocover
            return None

    @property
    def attached_timestamp_data(self) -> Optional[cms.SignedData]:
        """
        :return:
            The signed data component of the timestamp token embedded in this
            signature, if present.
        """
        return extract_tst_data(self.signer_info)

    def compute_integrity_info(self, diff_policy=None, skip_diff=False):
        """
        Compute the various integrity indicators of this signature.

        :param diff_policy:
            Policy to evaluate potential incremental updates that were appended
            to the signed revision of the document.
            Defaults to
            :const:`~paperlogic.sign.diff_analysis.DEFAULT_DIFF_POLICY`.
        :param skip_diff:
            If ``True``, skip the difference analysis step entirely.
        """
        self._enforce_hybrid_xref_policy()
        self.compute_digest()
        self.compute_tst_digest()

        # TODO in scenarios where we have to verify multiple signatures, we're
        #  doing a lot of double work here. This could be improved.
        self.coverage = self.evaluate_signature_coverage()
        diff_policy = diff_policy or DEFAULT_DIFF_POLICY
        if not skip_diff:
            self.diff_result = self.evaluate_modifications(diff_policy)

        self._integrity_checked = True

    def summarise_integrity_info(self) -> dict:
        """
        Compile the integrity information for this signature into a dictionary
        that can later be passed to :class:`.PdfSignatureStatus` as kwargs.

        This method is only available after calling
        :meth:`.EmbeddedPdfSignature.compute_integrity_info`.
        """

        if not self._integrity_checked:
            raise SignatureValidationError(
                "Call compute_integrity_info() before invoking"
                "summarise_integrity_info()"
            )  # pragma: nocover

        docmdp = self.docmdp_level
        diff_result = self.diff_result
        coverage = self.coverage
        docmdp_ok = None

        # attempt to set docmdp_ok based on the diff analysis results
        if diff_result is not None:
            mod_level = (
                diff_result.modification_level
                if isinstance(diff_result, DiffResult)
                else ModificationLevel.OTHER
            )
            docmdp_ok = not (
                mod_level == ModificationLevel.OTHER
                or (docmdp is not None and mod_level.value > docmdp.value)
            )
        elif coverage != SignatureCoverageLevel.ENTIRE_REVISION:
            # if the diff analysis didn't run, we can still do something
            # meaningful if coverage is not ENTIRE_REVISION:
            #  - if the signature covers the entire file, we're good.
            #  - if the coverage level is anything else, not so much
            docmdp_ok = coverage == SignatureCoverageLevel.ENTIRE_FILE

        status_kwargs = {
            'coverage': coverage,
            'docmdp_ok': docmdp_ok,
            'diff_result': diff_result,
        }
        return status_kwargs

    @property
    def seed_value_spec(self) -> Optional[SigSeedValueSpec]:
        try:
            sig_sv_dict = self.sig_field['/SV']
        except KeyError:
            return None
        return SigSeedValueSpec.from_pdf_object(sig_sv_dict)

    @property
    def docmdp_level(self) -> Optional[MDPPerm]:
        """
        :return:
            The document modification policy required by this signature or
            its Lock dictionary.

            .. warning::
                This does not take into account the DocMDP requirements of
                earlier signatures (if present).

                The specification forbids signing with a more lenient DocMDP
                than the one currently in force, so this should not happen
                in a compliant document.
                That being said, any potential violations will still invalidate
                the earlier signature with the stricter DocMDP policy.

        """
        if self._docmdp_queried:
            return self._docmdp
        docmdp = _extract_docmdp_for_sig(signature_obj=self.sig_object)

        if docmdp is None:
            try:
                lock_dict = self.sig_field['/Lock']
                docmdp = MDPPerm(lock_dict['/P'])
            except KeyError:
                pass
        self._docmdp = docmdp
        self._docmdp_queried = True
        return docmdp

    @property
    def fieldmdp(self) -> Optional[FieldMDPSpec]:
        """
        :return:
            Read the field locking policy of this signature, if applicable.
            See also :class:`~.paperlogic.sign.fields.FieldMDPSpec`.
        """
        # TODO as above, fall back to /Lock
        if self._fieldmdp_queried:
            return self._fieldmdp
        ref_dict = _extract_reference_dict(self.sig_object, '/FieldMDP')
        self._fieldmdp_queried = True
        if ref_dict is None:
            return None
        try:
            sp = FieldMDPSpec.from_pdf_object(ref_dict['/TransformParams'])
        except (ValueError, KeyError) as e:  # pragma: nocover
            raise SignatureValidationError(
                "Failed to read /FieldMDP settings"
            ) from e
        self._fieldmdp = sp
        return sp

    def compute_digest(self):
        """
        Compute the ``/ByteRange`` digest of this signature.
        The result will be cached.

        :return:
            The digest value.
        """
        if self.external_digest is not None:
            return self.external_digest

        self.total_len, digest = byte_range_digest(
            self.reader.stream,
            byte_range=self.byte_range,
            md_algorithm=self.external_md_algorithm,
        )
        self.external_digest = digest
        return digest

    def compute_tst_digest(self) -> Optional[bytes]:
        """
        Compute the digest of the signature needed to validate its timestamp
        token (if present).

        .. warning::
            This computation is only relevant for timestamp tokens embedded
            inside a regular signature.
            If the signature in question is a document timestamp (where the
            entire signature object is a timestamp token), this method
            does not apply.

        :return:
            The digest value, or ``None`` if there is no timestamp token.
        """

        if self.tst_signature_digest is not None:
            return self.tst_signature_digest
        self.tst_signature_digest = digest = compute_signature_tst_digest(
            self.signer_info
        )
        return digest

    def evaluate_signature_coverage(self) -> SignatureCoverageLevel:
        """
        Internal method used to evaluate the coverage level of a signature.

        :return:
            The coverage level of the signature.
        """

        xref_cache = self.reader.xrefs
        # for the coverage check, we're more strict with regards to the byte
        #  range
        stream = self.reader.stream

        # nonstandard byte range -> insta-fail
        if len(self.byte_range) != 4 or self.byte_range[0] != 0:
            return SignatureCoverageLevel.UNCLEAR

        _, len1, start2, len2 = self.byte_range

        # first check: check if the signature covers the entire file.
        #  (from a cryptographic point of view)
        # In this case, there are no changes at all, so we're good.

        # compute file size
        stream.seek(0, os.SEEK_END)
        # the * 2 is because of the ASCII hex encoding, and the + 2
        # is the wrapping <>
        embedded_sig_content = len(self.pkcs7_content) * 2 + 2
        signed_zone_len = len1 + len2 + embedded_sig_content
        file_covered = stream.tell() == signed_zone_len
        if file_covered:
            return SignatureCoverageLevel.ENTIRE_FILE

        # Now we're in the mixed case: the byte range is a standard one
        #  starting at the beginning of the document, but it doesn't go all
        #  the way to the end of the file. This can be for legitimate reasons,
        #  not all of which we can evaluate right now.

        # First, check if the signature is a contiguous one.
        # In other words, we need to check if the interruption in the byte
        # range is "fully explained" by the signature content.
        contiguous = start2 == len1 + embedded_sig_content
        if not contiguous:
            return SignatureCoverageLevel.UNCLEAR

        # next, we verify that the revision this signature belongs to
        #  is completely covered. This requires a few separate checks.
        # (1) Verify that the xref container (table or stream) is covered
        # (2) Verify the presence of the EOF and startxref markers at the
        #     end of the signed region, and compare them with the values
        #     in the xref cache to make sure we are reading the right revision.

        # Check (2) first, since it's the quickest
        stream.seek(signed_zone_len)
        signed_rev = self.signed_revision
        try:
            startxref = process_data_at_eof(stream)
            expected = xref_cache.get_startxref_for_revision(signed_rev)
            if startxref != expected:
                return SignatureCoverageLevel.CONTIGUOUS_BLOCK_FROM_START
        except misc.PdfReadError:
            return SignatureCoverageLevel.CONTIGUOUS_BLOCK_FROM_START

        # ... then check (1) for all revisions up to and including
        # signed_revision
        for revision in range(signed_rev + 1):
            xref_meta = xref_cache.get_xref_container_info(revision)
            if xref_meta.end_location > signed_zone_len:
                return SignatureCoverageLevel.CONTIGUOUS_BLOCK_FROM_START

        return SignatureCoverageLevel.ENTIRE_REVISION

    def _enforce_hybrid_xref_policy(self):
        reader = self.reader
        if reader.strict and reader.xrefs.hybrid_xrefs_present:
            raise SignatureValidationError(
                "Settings do not permit validation of signatures in "
                "hybrid-reference files."
            )

    def evaluate_modifications(
        self, diff_policy: DiffPolicy
    ) -> Union[DiffResult, SuspiciousModification]:
        """
        Internal method used to evaluate the modification level of a signature.
        """

        if self.coverage < SignatureCoverageLevel.ENTIRE_REVISION:
            return SuspiciousModification(
                'Nonstandard signature coverage level'
            )
        elif self.coverage == SignatureCoverageLevel.ENTIRE_FILE:
            return DiffResult(ModificationLevel.NONE, set())

        return diff_policy.review_file(
            self.reader,
            self.signed_revision,
            field_mdp_spec=self.fieldmdp,
            doc_mdp=self.docmdp_level,
        )

def _extract_reference_dict(
    signature_obj, method
) -> Optional[generic.DictionaryObject]:
    try:
        sig_refs = signature_obj['/Reference']
    except KeyError:
        return None
    for ref in sig_refs:
        ref = ref.get_object()
        if ref['/TransformMethod'] == method:
            return ref
    return None

def _extract_docmdp_for_sig(signature_obj) -> Optional[MDPPerm]:
    ref = _extract_reference_dict(signature_obj, '/DocMDP')
    if ref is None:
        return None
    try:
        raw_perms = ref['/TransformParams'].raw_get('/P')
        return MDPPerm(raw_perms)
    except (ValueError, KeyError) as e:  # pragma: nocover
        raise SignatureValidationError(
            "Failed to read document permissions"
        ) from e

def read_certification_data(reader: PdfFileReader) -> Optional[DocMDPInfo]:
    """
    Read the certification information for a PDF document, if present.

    :param reader:
        Reader representing the input document.
    :return:
        A :class:`.DocMDPInfo` object containing the relevant data, or ``None``.
    """
    try:
        certification_sig = reader.root['/Perms']['/DocMDP']
    except KeyError:
        return None

    perm = _extract_docmdp_for_sig(certification_sig)
    return DocMDPInfo(perm, certification_sig)
