from typing import Optional

from asn1crypto import cms, core, x509


__all__ = [
    'AAControls',
    'Target'
]

class TargetCert(core.Sequence):
    _fields = [
        ('target_certificate', cms.IssuerSerial),
        ('target_name', x509.GeneralName, {'optional': True}),
        ('cert_digest_info', cms.ObjectDigestInfo, {'optional': True}),
    ]


class Target(core.Choice):
    _alternatives = [
        ('target_name', x509.GeneralName, {'explicit': 0}),
        ('target_group', x509.GeneralName, {'explicit': 1}),
        ('target_cert', TargetCert, {'explicit': 2}),
    ]


class AttrSpec(core.SequenceOf):
    _child_spec = cms.AttCertAttributeType


class AAControls(core.Sequence):
    _fields = [
        ('path_len_constraint', core.Integer, {'optional': True}),
        ('permitted_attrs', AttrSpec, {'optional': True, 'implicit': 0}),
        ('excluded_attrs', AttrSpec, {'optional': True, 'implicit': 1}),
        ('permit_unspecified', core.Boolean, {'default': True}),
    ]

    def accept(self, attr_id: cms.AttCertAttributeType):
        attr_id_str = attr_id.native
        excluded = self['excluded_attrs'].native
        if excluded is not None:
            excluded = frozenset(excluded)
        if excluded is not None and attr_id_str in excluded:
            return False
        permitted = self['permitted_attrs'].native
        if permitted is not None:
            permitted = frozenset(permitted)
        if permitted is not None and attr_id_str in permitted:
            return True
        return bool(self['permit_unspecified'])

    @classmethod
    def read_extension_value(
        cls, cert: x509.Certificate
    ) -> Optional['AAControls']:
        # handle AA controls (not natively supported by asn1crypto, so
        # not available as an attribute).
        try:
            return next(
                ext['extn_value'].parsed
                for ext in cert['tbs_certificate']['extensions']
                if ext['extn_id'].native == 'aa_controls'
            )
        except StopIteration:
            return None
