from typing import Optional, Union
from asn1crypto import cms, x509, tsp
from datetime import datetime
from cryptography.hazmat.primitives import hashes

from ....paperlogic_signature.sign.general import (
    find_unique_cms_attribute,
    get_pyca_cryptography_hash,
    extract_certificate_info,
    extract_signer_info,
    check_ess_certid,
    SignedDataCerts,
    NonexistentAttributeError,
    MultivaluedAttributeError,
    CMSExtractionError
)
from . import errors
from ..ades.report import AdESIndeterminate

__all__ = [
    'compute_signature_tst_digest',
    'extract_certs_for_validation',
    'extract_self_reported_ts',
    'extract_tst_data'
]

def get_signing_cert_attr(
    signed_attrs: cms.CMSAttributes,
) -> Union[tsp.SigningCertificate, tsp.SigningCertificateV2, None]:
    """
    Retrieve the ``signingCertificate`` or ``signingCertificateV2`` attribute
    (giving preference to the latter) from a signature's signed attributes.

    :param signed_attrs:
        Signed attributes.
    :return:
        The value of the attribute, if present, else ``None``.
    """
    attr = _grab_signing_cert_attr(signed_attrs, v2=True)
    if attr is None:
        attr = _grab_signing_cert_attr(signed_attrs, v2=False)
    return attr

def _grab_signing_cert_attr(signed_attrs, v2: bool):
    # TODO check certificate policies, enforce restrictions on chain of trust
    # TODO document and/or mark as internal API explicitly
    attr_name = 'signing_certificate_v2' if v2 else 'signing_certificate'
    cls = tsp.SigningCertificateV2 if v2 else tsp.SigningCertificate
    try:
        value = find_unique_cms_attribute(signed_attrs, attr_name)
        # reencode the attribute to avoid accidentally tripping the
        # _is_mutated logic on the parent object (is important to preserve
        # the state of the signed attributes)
        return cls.load(value.dump())
    except NonexistentAttributeError:
        return None
    except MultivaluedAttributeError as e:
        # Banned by RFCs -> error
        err = AdESIndeterminate.NO_SIGNING_CERTIFICATE_FOUND
        raise errors.SignatureValidationError(
            "Wrong cardinality for signing certificate attribute",
            ades_subindication=err,
        ) from e

def extract_self_reported_ts(signer_info: cms.SignerInfo) -> Optional[datetime]:
    """
    Extract self-reported timestamp (from the ``signingTime`` attribute)

    Internal API.

    :param signer_info:
        A ``SignerInfo`` value.
    :return:
        The value of the ``signingTime`` attribute as a ``datetime``, or
        ``None``.
    """
    try:
        sa = signer_info['signed_attrs']
        st = find_unique_cms_attribute(sa, 'signing_time')
        return st.native
    except (NonexistentAttributeError, MultivaluedAttributeError):
        return None

def extract_tst_data(
    signer_info: cms.SignerInfo, signed: bool = False
) -> Optional[cms.SignedData]:
    """
    Extract signed data associated with a timestamp token.

    Internal API.

    :param signer_info:
        A ``SignerInfo`` value.
    :param signed:
        If ``True``, look for a content timestamp (among the signed
        attributes), else look for a signature timestamp (among the unsigned
        attributes).
    :return:
        The ``SignedData`` value found, or ``None``.
    """
    try:
        if signed:
            sa = signer_info['signed_attrs']
            tst = find_unique_cms_attribute(sa, 'content_time_stamp')
        else:
            ua = signer_info['unsigned_attrs']
            tst = find_unique_cms_attribute(ua, 'signature_time_stamp_token')
        tst_signed_data = tst['content']
        return tst_signed_data
    except (NonexistentAttributeError, MultivaluedAttributeError):
        return None


def compute_signature_tst_digest(
    signer_info: cms.SignerInfo,
) -> Optional[bytes]:
    """
    Compute the digest of the signature according to the message imprint
    algorithm information in a signature timestamp token.

    Internal API.

    :param signer_info:
        A ``SignerInfo`` value.
    :return:
        The computed digest, or ``None`` if there is no signature timestamp.
    """

    tst_data = extract_tst_data(signer_info)
    if tst_data is None:
        return None

    eci = tst_data['encap_content_info']
    mi = eci['content'].parsed['message_imprint']
    tst_md_algorithm = mi['hash_algorithm']['algorithm'].native

    signature_bytes = signer_info['signature'].native
    tst_md_spec = get_pyca_cryptography_hash(tst_md_algorithm)
    md = hashes.Hash(tst_md_spec)
    md.update(signature_bytes)
    return md.finalize()

def _check_signing_certificate(
    cert: x509.Certificate, signed_attrs: cms.CMSAttributes
):
    # TODO check certificate policies, enforce restrictions on chain of trust
    # TODO document and/or mark as internal API explicitly

    attr = get_signing_cert_attr(signed_attrs)
    if attr is None:
        # if not present -> no constraints
        return

    # For the main signer cert, we only care about the first value, the others
    # limit the set of applicable CA certs
    certid = attr['certs'][0]

    if not check_ess_certid(cert, certid):
        err = AdESIndeterminate.NO_SIGNING_CERTIFICATE_FOUND
        raise errors.SignatureValidationError(
            f"Signing certificate attribute does not match selected "
            f"signer's certificate for subject"
            f"\"{cert.subject.human_friendly}\".",
            ades_subindication=err,
        )

def extract_certs_for_validation(
    signed_data: cms.SignedData,
) -> SignedDataCerts:
    """
    Extract certificates from a CMS signed data object for validation purposes,
    identifying the signer's certificate in accordance with ETSI EN 319 102-1,
    5.2.3.4.

    :param signed_data:
        The CMS payload.
    :return:
        The extracted certificates.
    """

    # TODO allow signer certificate to be obtained from elsewhere?

    try:
        cert_info = extract_certificate_info(signed_data)
        cert = cert_info.signer_cert
    except CMSExtractionError:
        raise errors.SignatureValidationError(
            'signer certificate not included in signature',
            ades_subindication=AdESIndeterminate.NO_SIGNING_CERTIFICATE_FOUND,
        )
    signer_info = extract_signer_info(signed_data)
    signed_attrs = signer_info['signed_attrs']
    # check the signing-certificate or signing-certificate-v2 attr
    _check_signing_certificate(cert, signed_attrs)
    return cert_info
