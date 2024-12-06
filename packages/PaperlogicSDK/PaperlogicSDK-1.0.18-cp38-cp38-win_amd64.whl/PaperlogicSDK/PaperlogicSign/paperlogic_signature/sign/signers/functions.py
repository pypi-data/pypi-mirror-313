"""
This module defines aurora's high-level API entry points.
"""

from typing import Optional

from ...pdf_utils.writer import BasePdfFileWriter
from ...sign.fields import SigFieldSpec
from ...sign.general import SigningError
from ...sign.timestamps import TimeStamper

from .pdf_cms import Signer
from .pdf_signer import PdfSignatureMetadata, PdfSigner

__all__ = ['sign_pdf', 'async_sign_pdf']

def sign_pdf(
    pdf_out: BasePdfFileWriter,
    signature_meta: PdfSignatureMetadata,
    signer: Signer,
    timestamper: Optional[TimeStamper] = None,
    new_field_spec: Optional[SigFieldSpec] = None,
    existing_fields_only=False,
    bytes_reserved=None,
    in_place=False,
    output=None,
):
    """
    Thin convenience wrapper around :meth:`.PdfSigner.sign_pdf`.

    :param pdf_out:
        An :class:`.IncrementalPdfFileWriter`.
    :param bytes_reserved:
        Bytes to reserve for the CMS object in the PDF file.
        If not specified, make an estimate based on a dummy signature.
    :param signature_meta:
        The specification of the signature to add.
    :param signer:
        :class:`.Signer` object to use to produce the signature object.
    :param timestamper:
        :class:`.TimeStamper` object to use to produce any time stamp tokens
        that might be required.
    :param in_place:
        Sign the input in-place. If ``False``, write output to a
        :class:`.BytesIO` object.
    :param existing_fields_only:
        If ``True``, never create a new empty signature field to contain
        the signature.
        If ``False``, a new field may be created if no field matching
        :attr:`~.PdfSignatureMetadata.field_name` exists.
    :param new_field_spec:
        If a new field is to be created, this parameter allows the caller
        to specify the field's properties in the form of a
        :class:`.SigFieldSpec`. This parameter is only meaningful if
        ``existing_fields_only`` is ``False``.
    :param output:
        Write the output to the specified output stream.
        If ``None``, write to a new :class:`.BytesIO` object.
        Default is ``None``.
    :return:
        The output stream containing the signed output.
    """

    if new_field_spec is not None and existing_fields_only:
        raise SigningError(
            "Specifying a signature field spec is not meaningful when "
            "existing_fields_only=True."
        )

    pdf_signer = PdfSigner(
        signature_meta,
        signer,
        timestamper=timestamper,
        new_field_spec=new_field_spec,
    )
    return pdf_signer.sign_pdf(
        pdf_out,
        existing_fields_only=existing_fields_only,
        bytes_reserved=bytes_reserved,
        in_place=in_place,
        output=output,
    )


async def async_sign_pdf(
    pdf_out: BasePdfFileWriter,
    signature_meta: PdfSignatureMetadata,
    signer: Signer,
    timestamper: Optional[TimeStamper] = None,
    new_field_spec: Optional[SigFieldSpec] = None,
    existing_fields_only=False,
    bytes_reserved=None,
    in_place=False,
    output=None,
):
    """
    Thin convenience wrapper around :meth:`.PdfSigner.async_sign_pdf`.

    :param pdf_out:
        An :class:`.IncrementalPdfFileWriter`.
    :param bytes_reserved:
        Bytes to reserve for the CMS object in the PDF file.
        If not specified, make an estimate based on a dummy signature.
    :param signature_meta:
        The specification of the signature to add.
    :param signer:
        :class:`.Signer` object to use to produce the signature object.
    :param timestamper:
        :class:`.TimeStamper` object to use to produce any time stamp tokens
        that might be required.
    :param in_place:
        Sign the input in-place. If ``False``, write output to a
        :class:`.BytesIO` object.
    :param existing_fields_only:
        If ``True``, never create a new empty signature field to contain
        the signature.
        If ``False``, a new field may be created if no field matching
        :attr:`~.PdfSignatureMetadata.field_name` exists.
    :param new_field_spec:
        If a new field is to be created, this parameter allows the caller
        to specify the field's properties in the form of a
        :class:`.SigFieldSpec`. This parameter is only meaningful if
        ``existing_fields_only`` is ``False``.
    :param output:
        Write the output to the specified output stream.
        If ``None``, write to a new :class:`.BytesIO` object.
        Default is ``None``.
    :return:
        The output stream containing the signed output.
    """

    if new_field_spec is not None and existing_fields_only:
        raise SigningError(
            "Specifying a signature field spec is not meaningful when "
            "existing_fields_only=True."
        )

    pdf_signer = PdfSigner(
        signature_meta,
        signer,
        timestamper=timestamper,
        new_field_spec=new_field_spec,
    )
    return await pdf_signer.async_sign_pdf(
        pdf_out,
        existing_fields_only=existing_fields_only,
        bytes_reserved=bytes_reserved,
        in_place=in_place,
        output=output,
    )