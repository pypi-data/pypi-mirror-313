from dataclasses import dataclass
from datetime import datetime
from enum import unique
from typing import (
    ClassVar,
    Optional,
    Set,
)

from asn1crypto import crl, x509

from ....paperlogic_certvalidator.path import ValidationPath

from ..ades.report import AdESSubIndic
from .settings import KeyUsageConstraints
from ...pdf_utils.misc import OrderedEnum


__all__ = [
    'RevocationDetails',
    'SignatureStatus',
    'TimestampSignatureStatus',
    'SignatureCoverageLevel'
]

@dataclass(frozen=True)
class RevocationDetails:
    """
    Contains details about a certificate revocation related to a signature.
    """

    ca_revoked: bool
    """
    If ``False``, the revoked certificate is the signer's. If ``True``, there's
    a revoked CA certificate higher up the chain.
    """

    revocation_date: datetime
    """
    The date and time of revocation.
    """

    revocation_reason: crl.CRLReason
    """
    The reason why the certificate was revoked.
    """

@dataclass(frozen=True)
class SignatureStatus:
    """
    Class describing the validity of a (general) CMS signature.
    """

    intact: bool
    """
    Reports whether the signature is *intact*, i.e. whether the hash of the
    message content (which may or may not be embedded inside the CMS object
    itself) matches the hash value that was signed.

    If there are no signed attributes, this is equal to :attr:`valid`.
    """

    valid: bool
    """
    Reports whether the signature is *valid*, i.e. whether the signature
    in the CMS object itself (usually computed over a hash of the signed
    attributes) is cryptographically valid.
    """

    trust_problem_indic: Optional[AdESSubIndic]
    """
    If not ``None``, provides the AdES subindication indication what went
    wrong when validating the signer's certificate.
    """

    signing_cert: x509.Certificate
    """
    Contains the certificate of the signer, as embedded in the CMS object.
    """

    pkcs7_signature_mechanism: str
    """
    CMS signature mechanism used.
    """

    # TODO: also here some ambiguity analysis is in order
    md_algorithm: str
    """
    Message digest algorithm used.
    """

    validation_path: Optional[ValidationPath]
    """
    Validation path providing a valid chain of trust from the signer's
    certificate to a trusted root certificate.
    """

    revocation_details: Optional[RevocationDetails]
    """
    Details on why and when the signer's certificate (or another certificate
    in the chain) was revoked.
    """

    error_time_horizon: Optional[datetime]
    """
    Informational timestamp indicating a point in time where the validation
    behaviour potentially changed (e.g. expiration, revocation, etc.).

    The presence of this value by itself should not be taken as an assertion
    that validation would have succeeded if executed before that point in time.
    """

    # XXX frozenset makes more sense here, but asn1crypto doesn't allow that
    #  (probably legacy behaviour)
    key_usage: ClassVar[Set[str]] = {'non_repudiation'}
    """
    Class property indicating which key usages are accepted on the signer's
    certificate. The default is ``non_repudiation`` only.
    """

    extd_key_usage: ClassVar[Optional[Set[str]]] = None
    """
    Class property indicating which extended key usage key purposes are accepted
    to be present on the signer's certificate.

    See :attr:`.KeyUsageConstraints.extd_key_usage`.
    """

    validation_time: Optional[datetime]
    """
    Reference time for validation purposes.
    """

    def summary_fields(self):
        if self.trusted:
            cert_status = 'TRUSTED'
        elif self.revoked:
            cert_status = 'REVOKED'
        else:
            cert_status = 'UNTRUSTED'
        yield cert_status

    @property
    def revoked(self):
        """
        Reports whether the signer's certificate has been revoked or not.
        If this field is ``True``, then obviously :attr:`trusted` will be
        ``False``.
        """
        return self.revocation_details is not None

    @property
    def trusted(self):
        """
        Reports whether the signer's certificate is trusted w.r.t. the currently
        relevant validation context and key usage requirements.
        """
        return (
            self.valid
            and self.intact
            and self.trust_problem_indic is None
            and self.validation_path is not None
        )

    # TODO explain in more detail.
    def summary(self, delimiter=',') :
        """
        Provide a textual but machine-parsable summary of the validity.
        """
        if self.intact and self.valid:
            return 'INTACT:' + delimiter.join(self.summary_fields())
        else:
            return 'INVALID'

    @classmethod
    def default_usage_constraints(
        cls, key_usage_settings: Optional[KeyUsageConstraints] = None
    ) -> KeyUsageConstraints:
        key_usage_settings = key_usage_settings or KeyUsageConstraints()
        key_usage_settings = KeyUsageConstraints(
            key_usage=(
                cls.key_usage
                if key_usage_settings.key_usage is None
                else key_usage_settings.key_usage
            ),
            extd_key_usage=(
                cls.extd_key_usage
                if key_usage_settings.extd_key_usage is None
                else key_usage_settings.extd_key_usage
            ),
        )
        return key_usage_settings

    @property
    def _trust_anchor(self) :
        if self.validation_path is not None:
            trust_anchor: x509.Certificate = self.validation_path[0]
            return trust_anchor.subject.human_friendly
        else:
            return "No path to trust anchor found."

@dataclass(frozen=True)
class TimestampSignatureStatus(SignatureStatus):
    """
    Signature status class used when validating timestamp tokens.
    """

    key_usage: ClassVar[Set[str]] = set()
    """
    There are no (non-extended) key usage requirements for TSA certificates.
    """

    extd_key_usage = {'time_stamping'}
    """
    TSA certificates must have the ``time_stamping`` extended key usage
    extension (OID 1.3.6.1.5.5.7.3.8).
    """

    timestamp: datetime
    """
    Value of the timestamp token as a datetime object.
    """

    def describe_timestamp_trust(self):
        tsa = self.signing_cert

        return (
            "This timestamp is backed by a time stamping authority.\n"
            "The timestamp token is cryptographically "
            f"{'' if self.intact and self.valid else 'un'}sound.\n"
            f"TSA certificate subject: \"{tsa.subject.human_friendly}\"\n"
            f"TSA certificate SHA1 fingerprint: {tsa.sha1.hex()}\n"
            f"TSA certificate SHA256 fingerprint: {tsa.sha256.hex()}\n"
            f"TSA cert trust anchor: \"{self._trust_anchor}\"\n"
            "The TSA certificate is "
            f"{'' if self.trusted else 'un'}trusted."
        )

@unique
class SignatureCoverageLevel(OrderedEnum):
    """
    Indicate the extent to which a PDF signature (cryptographically) covers
    a document. Note that this does *not* pass judgment on whether uncovered
    updates are legitimate or not, but as a general rule, a legitimate signature
    will satisfy at least :attr:`ENTIRE_REVISION`.
    """

    UNCLEAR = 0
    """
    The signature's coverage is unclear and/or disconnected.
    In standard PDF signatures, this is usually a bad sign.
    """

    CONTIGUOUS_BLOCK_FROM_START = 1
    """
    The signature covers a contiguous block in the PDF file stretching from
    the first byte of the file to the last byte in the indicated ``/ByteRange``.
    In other words, the only interruption in the byte range is fully occupied
    by the signature data itself.
    """

    ENTIRE_REVISION = 2
    """
    The signature covers the entire revision in which it occurs, but incremental
    updates may have been added later. This is not necessarily evidence of
    tampering. In particular, it is expected when a file contains multiple
    signatures. Nonetheless, caution is required.
    """

    ENTIRE_FILE = 3
    """
    The entire file is covered by the signature.
    """
