
from ...pdf_utils import generic
from ..extensions import DeveloperExtension, DevExtensionMultivalued

__all__ = [
    'ISO32004',
]

ISO32004 = DeveloperExtension(
    prefix_name=generic.pdf_name('/ISO_'),
    base_version=generic.pdf_name('/2.0'),
    extension_level=32004,
    extension_revision=':2024',
    url='https://www.iso.org/standard/45877.html',
    compare_by_level=False,
    multivalued=DevExtensionMultivalued.ALWAYS,
)