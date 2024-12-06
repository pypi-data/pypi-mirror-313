from typing import Iterator

from ...pdf_utils.reader import PdfFileReader

from .pdf_embedded import EmbeddedPdfSignature

__all__ = [
    'get_timestamp_chain'
]

def get_timestamp_chain(
    reader: PdfFileReader,
) -> Iterator[EmbeddedPdfSignature]:
    """
    Get the document timestamp chain of the associated reader, ordered
    from new to old.

    :param reader:
        A :class:`.PdfFileReader`.
    :return:
        An iterable of
        :class:`~paperlogic.sign.validation.pdf_embedded.EmbeddedPdfSignature`
        objects representing document timestamps.
    """
    return filter(
        lambda sig: sig.sig_object.get('/Type', None) == '/DocTimeStamp',
        reversed(reader.embedded_signatures),
    )
