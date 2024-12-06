from asn1crypto import core, algos, cms

__all__ = [
    'CommitmentTypeIndication',
    'SignaturePolicyIdentifier'
    'SignerAttributesV2',
    'CertifiedAttributeChoices'
]


class CommitmentTypeIdentifier(core.ObjectIdentifier):
    _map = {
        # from ETSI TS 119 172-1 Annex B, RFC 5126
        '1.2.840.113549.1.9.16.6.1': 'proof_of_origin',
        '1.2.840.113549.1.9.16.6.2': 'proof_of_receipt',
        '1.2.840.113549.1.9.16.6.3': 'proof_of_delivery',
        '1.2.840.113549.1.9.16.6.4': 'proof_of_sender',
        '1.2.840.113549.1.9.16.6.5': 'proof_of_approval',
        '1.2.840.113549.1.9.16.6.6': 'proof_of_creation',
    }

class CommitmentTypeQualifier(core.Sequence):
    _fields = [
        ('commitment_type_identifier', CommitmentTypeIdentifier),
        ('qualifier', core.Any),
    ]

    _oid_pair = ('commitment_type_identifier', 'qualifier')
    # CAdES generic commitment types don't use qualifiers, so this is reserved
    # for more advanced uses
    _oid_specs = {}


class CommitmentTypeQualifiers(core.SequenceOf):
    _child_spec = CommitmentTypeQualifier


class CommitmentTypeIndication(core.Sequence):
    _fields = [
        ('commitment_type_id', CommitmentTypeIdentifier),
        (
            'commitment_type_qualifier',
            CommitmentTypeQualifiers,
            {'optional': True},
        ),
    ]


class SigPolicyQualifierId(core.ObjectIdentifier):
    _map = {
        # RFC 5126
        '1.2.840.113549.1.9.16.5.1': 'sp_uri',
        '1.2.840.113549.1.9.16.5.2': 'sp_unotice',
        # ETSI EN 319 122-1
        '0.4.0.19122.2.1': 'sp_doc_specification',
    }


class DisplayText(core.Choice):
    # TODO does asn1crypto support length limitations?
    #  These strings have a length limit of 200 characters
    _alternatives = [
        ('visible_string', core.VisibleString),
        ('bmp_string', core.BMPString),
        ('utf8_string', core.UTF8String),
    ]


class NoticeNumbers(core.SequenceOf):
    _child_spec = core.Integer


class NoticeReference(core.Sequence):
    _fields = [('organization', DisplayText), ('notice_numbers', NoticeNumbers)]


class SPUserNotice(core.Sequence):
    _fields = [
        ('notice_ref', NoticeReference, {'optional': True}),
        ('explicit_text', DisplayText, {'optional': True}),
    ]


class SPDocSpecification(core.Sequence):
    _fields = [('oid', core.ObjectIdentifier), ('uri', core.IA5String)]


class SigPolicyQualifierInfo(core.Sequence):
    _fields = [
        ('sig_policy_qualifier_id', SigPolicyQualifierId),
        ('sig_qualifier', core.Any),
    ]

    _oid_pair = ('sig_policy_qualifier_id', 'sig_qualifier')
    _oid_specs = {
        # RFC 5126
        'sp_uri': core.IA5String,
        'sp_unotice': SPUserNotice,
        # ETSI EN 319 122-1
        'sp_doc_specification': SPDocSpecification,
    }


class SigPolicyQualifierInfos(core.SequenceOf):
    _child_spec = SigPolicyQualifierInfo


class SignaturePolicyId(core.Sequence):
    _fields = [
        ('sig_policy_id', core.ObjectIdentifier),
        ('sig_policy_hash', algos.DigestInfo),
        ('sig_policy_qualifiers', SigPolicyQualifierInfos, {'optional': True}),
    ]


class SignaturePolicyIdentifier(core.Choice):
    _alternatives = [
        ('signature_policy_id', SignaturePolicyId),
        ('signature_policy_implied', core.Null),
    ]


class OtherAttrCertId(core.ObjectIdentifier):
    _map = {}  # empty map


class OtherAttrCert(core.Sequence):
    _fields = [
        ('other_attr_cert_id', OtherAttrCertId),
        ('other_attr_cert', core.Any),
    ]

    _oid_pair = ('other_attr_cert_id', 'other_attr_cert')
    _oid_specs = {}  # empty map


class CertifiedAttributeChoices(core.Choice):
    _alternatives = [
        ('attr_cert', cms.AttributeCertificateV2, {'explicit': 0}),
        ('other_attr_cert', OtherAttrCert, {'explicit': 1}),
    ]


class CertifiedAttributesV2(core.SequenceOf):
    _child_spec = CertifiedAttributeChoices


class SignedAssertionId(core.ObjectIdentifier):
    _map = {}  # empty map


class SignedAssertion(core.Sequence):
    _fields = [
        ('signed_assertion_id', SignedAssertionId),
        ('signed_assertion', core.Any),
    ]

    _oid_pair = ('signed_assertion_id', 'signed_assertion')
    _oid_specs = {}  # empty map


class SignedAssertions(core.SequenceOf):
    _child_spec = SignedAssertion


class SignerAttributesV2(core.Sequence):
    _fields = [
        # CAdES says that the definition of Attribute is as in X.509.
        # asn1crypto defines this in two different places, but the "canonical"
        # one in x509.Attribute doesn't supply any concrete attribute
        # definitions, so we use the definition in cms.AttCertAttribute instead
        (
            'claimed_attributes',
            cms.AttCertAttributes,
            {'optional': True, 'explicit': 0},
        ),
        (
            'certified_attributes_v2',
            CertifiedAttributesV2,
            {'optional': True, 'explicit': 1},
        ),
        (
            'signed_assertions',
            SignedAssertions,
            {'optional': True, 'explicit': 2},
        ),
    ]