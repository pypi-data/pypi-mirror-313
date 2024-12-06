
"""
Utilities for stamping PDF files.

Here 'stamping' loosely refers to adding small overlays (QR codes, text boxes,
etc.) on top of already existing content in PDF files.

The code in this module is also used by the :mod:`.sign` module to render
signature appearances.
"""

import uuid
from binascii import hexlify
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import tzlocal

from .config.api import ConfigurableMixin
from .config.errors import ConfigurationError
from .pdf_utils.layout import LayoutError
from .pdf_utils import content, generic, layout
from .pdf_utils.generic import IndirectObject, pdf_name
from .pdf_utils.misc import rd
from .pdf_utils.writer import BasePdfFileWriter
from .pdf_utils.text import TextBoxStyle, TextBox, DEFAULT_BOX_LAYOUT


__all__ = [
    "AnnotAppearances",
    "BaseStampStyle",
    "BaseStamp",
]

class AnnotAppearances:
    """
    Convenience abstraction to set up an appearance dictionary for a PDF
    annotation.

    Annotations can have three appearance streams, which can be roughly
    characterised as follows:

    * *normal*: the only required one, and the default one;
    * *rollover*: used when mousing over the annotation;
    * *down*: used when clicking the annotation.

    These are given as references to form XObjects.

    .. note::
        This class only covers the simple case of an appearance dictionary
        for an annotation with only one appearance state.

    See § 12.5.5 in ISO 32000-1 for further information.
    """

    def __init__(
        self,
        normal: generic.IndirectObject,
        rollover: Optional[generic.IndirectObject] = None,
        down: Optional[generic.IndirectObject] = None,
    ):
        self.normal = normal
        self.rollover = rollover
        self.down = down

    def as_pdf_object(self) -> generic.DictionaryObject:
        """
        Convert the :class:`.AnnotationAppearances` instance to a PDF
        dictionary.

        :return:
            A :class:`~.pdf_utils.generic.DictionaryObject` that can be plugged
            into the ``/AP`` entry of an annotation dictionary.
        """

        res = generic.DictionaryObject({pdf_name('/N'): self.normal})
        if self.rollover is not None:
            res[pdf_name('/R')] = self.rollover
        if self.down is not None:
            res[pdf_name('/D')] = self.down
        return res

def _get_background_content(bg_spec) -> content.PdfContent:
    if not isinstance(bg_spec, str):
        raise ConfigurationError("Background specification must be a string")
    # 'special' value to use the stamp vector image baked into
    # the module
    if bg_spec == '__stamp__':
        return STAMP_ART_CONTENT
    elif bg_spec.endswith('.pdf'):
        # import first page of PDF as background
        return content.ImportedPdfPage(bg_spec)
    else:
        from PIL import Image

        from .pdf_utils.images import PdfImage

        img = Image.open(bg_spec)
        # Setting the writer can be delayed
        return PdfImage(img, writer=None)


@dataclass(frozen=True)
class BaseStampStyle(ConfigurableMixin):
    """
    Base class for stamp styles.
    """

    border_width: int = 3
    """
    Border width in user units (for the stamp, not the text box).
    """

    background: Optional[content.PdfContent] = None
    """
    :class:`~.pdf_utils.content.PdfContent` instance that will be used to render
    the stamp's background.
    """

    background_layout: layout.SimpleBoxLayoutRule = layout.SimpleBoxLayoutRule(
        x_align=layout.AxisAlignment.ALIGN_MID,
        y_align=layout.AxisAlignment.ALIGN_MID,
        margins=layout.Margins.uniform(5),
    )
    """
    Layout rule to render the background inside the stamp's bounding box.
    Only used if the background has a fully specified :attr:`PdfContent.box`.

    Otherwise, the renderer will position the cursor at
    ``(left_margin, bottom_margin)`` and render the content as-is.
    """

    background_opacity: float = 0.6
    """
    Opacity value to render the background at. This should be a floating-point
    number between `0` and `1`.
    """

    @classmethod
    def process_entries(cls, config_dict):
        """
        This implementation of :meth:`process_entries` processes the
        :attr:`background` configuration value.
        This can either be a path to an image file, in which case it will
        be turned into an instance of :class:`~.pdf_utils.images.PdfImage`,
        or the special value ``__stamp__``, which is an alias for
        :const:`~paperlogic_signature.stamp.STAMP_ART_CONTENT`.
        """

        super().process_entries(config_dict)
        bg_spec = None
        try:
            bg_spec = config_dict['background']
        except KeyError:
            pass
        if bg_spec is not None:
            config_dict['background'] = _get_background_content(bg_spec)

    def create_stamp(
        self,
        writer: BasePdfFileWriter,
        box: layout.BoxConstraints,
        text_params: dict,
    ) -> 'BaseStamp':
        raise NotImplementedError

@dataclass(frozen=True)
class TextStampStyle(BaseStampStyle):
    """
    Style for text-based stamps.

    Roughly speaking, this stamp type renders some predefined (but parametrised)
    piece of text inside a text box, and possibly applies a background to it.
    """

    text_box_style: TextBoxStyle = TextBoxStyle()
    """
    The text box style for the internal text box used.
    """

    inner_content_layout: Optional[layout.SimpleBoxLayoutRule] = None
    """
    Rule determining the position and alignment of the inner text box within
    the stamp.
    
    .. warning::
        This only affects the position of the box, not the alignment of the
        text within.
    """

    stamp_text: str = '%(ts)s'
    """
    Text template for the stamp. The template can contain an interpolation
    parameter ``ts`` that will be replaced by the stamping time.
    
    Additional parameters may be added if necessary. Values for these must be
    passed to the :meth:`~.TextStamp.__init__` method of the 
    :class:`.TextStamp` class in the ``text_params`` argument.
    """

    timestamp_format: str = '%Y-%m-%d %H:%M:%S %Z'
    """
    Datetime format used to render the timestamp.
    """

    def create_stamp(
        self,
        writer: BasePdfFileWriter,
        box: layout.BoxConstraints,
        text_params: dict,
    ) -> 'TextStamp':
        return TextStamp(
            writer=writer, style=self, box=box, text_params=text_params
        )

class BaseStamp(content.PdfContent):
    def __init__(
        self,
        writer: BasePdfFileWriter,
        style,
        box: Optional[layout.BoxConstraints] = None,
    ):
        super().__init__(box=box, writer=writer)
        self.style = style
        self._resources_ready = False
        self._stamp_ref: Optional[IndirectObject] = None

    def _render_background(self):
        bg = self.style.background
        bg.set_writer(self.writer)
        bg_content = bg.render()  # render first, in case the BBox is lazy

        bg_box = bg.box
        if bg_box.width_defined and bg_box.height_defined:
            # apply layout rule
            positioning = self.style.background_layout.fit(
                self.box, bg_box.width, bg_box.height
            )
        else:
            # No idea about the background dimensions, so just use
            # the left/bottom margins and hope for the best
            margins = self.style.background_layout.margins
            positioning = layout.Positioning(
                x_scale=1, y_scale=1, x_pos=margins.left, y_pos=margins.bottom
            )

        # set opacity in graphics state
        opacity = generic.FloatObject(self.style.background_opacity)
        self.set_resource(
            category=content.ResourceType.EXT_G_STATE,
            name=pdf_name('/BackgroundGS'),
            value=generic.DictionaryObject(
                {pdf_name('/CA'): opacity, pdf_name('/ca'): opacity}
            ),
        )

        # Position & render the background
        command = b'q /BackgroundGS gs %s %s Q' % (
            positioning.as_cm(),
            bg_content,
        )
        # we do this after render(), just in case our background resource
        # decides to pull in extra stuff during rendering
        self.import_resources(bg.resources)
        return command

    def _render_inner_content(self):
        raise NotImplementedError

    def render(self):
        command_stream = [b'q']

        inner_content = self._render_inner_content()

        # Now that the inner layout is done, the dimensions of our bounding
        # box should all have been reified. Let's put in the background,
        # if there is one
        if self.style.background:
            command_stream.append(self._render_background())

        # put in the inner content
        if inner_content:
            command_stream.extend(inner_content)

        # draw the border around the stamp
        bbox = self.box
        border_width = self.style.border_width
        if border_width:
            command_stream.append(
                b'%g w 0 0 %g %g re S' % (border_width, bbox.width, bbox.height)
            )
        command_stream.append(b'Q')
        return b' '.join(command_stream)

    def register(self) -> generic.IndirectObject:
        """
        Register the stamp with the writer coupled to this instance, and
        cache the returned reference.

        This works by calling :meth:`.PdfContent.as_form_xobject`.

        :return:
            An indirect reference to the form XObject containing the stamp.
        """
        stamp_ref = self._stamp_ref
        if stamp_ref is None:
            wr = self._ensure_writer
            form_xobj = self.as_form_xobject()
            self._stamp_ref = stamp_ref = wr.add_object(form_xobj)
        return stamp_ref

    def apply(self, dest_page: int, x: int, y: int):
        """
        Apply a stamp to a particular page in the PDF writer attached to this
        :class:`.BaseStamp` instance.

        :param dest_page:
            Index of the page to which the stamp is to be applied
            (starting at `0`).
        :param x:
            Horizontal position of the stamp's lower left corner on the page.
        :param y:
            Vertical position of the stamp's lower left corner on the page.
        :return:
            A reference to the affected page object, together with
            a ``(width, height)`` tuple describing the dimensions of the stamp.
        """
        stamp_ref = self.register()
        resource_name = b'/Stamp' + hexlify(uuid.uuid4().bytes)
        stamp_paint = b'q 1 0 0 1 %g %g cm %s Do Q' % (
            rd(x),
            rd(y),
            resource_name,
        )
        stamp_wrapper_stream = generic.StreamObject(stream_data=stamp_paint)
        resources = generic.DictionaryObject(
            {
                pdf_name('/XObject'): generic.DictionaryObject(
                    {pdf_name(resource_name.decode('ascii')): stamp_ref}
                )
            }
        )
        wr = self.writer
        assert wr is not None
        page_ref = wr.add_stream_to_page(
            dest_page, wr.add_object(stamp_wrapper_stream), resources
        )
        dims = (self.box.width, self.box.height)
        return page_ref, dims

    def as_appearances(self) -> AnnotAppearances:
        """
        Turn this stamp into an appearance dictionary for an annotation
        (or a form field widget), after rendering it.
        Only the normal appearance will be defined.

        :return:
            An instance of :class:`.AnnotAppearances`.
        """
        # TODO support defining overrides/extra's for the rollover/down
        #  appearances in some form
        stamp_ref = self.register()
        return AnnotAppearances(normal=stamp_ref)

class TextStamp(BaseStamp):
    """
    Class that renders a text stamp as specified by an instance
    of :class:`.TextStampStyle`.
    """

    def __init__(
        self,
        writer: BasePdfFileWriter,
        style,
        text_params=None,
        box: Optional[layout.BoxConstraints] = None,
    ):
        super().__init__(box=box, style=style, writer=writer)
        self.text_params = text_params

        self.text_box: Optional[TextBox] = None

    def get_default_text_params(self):
        """
        Compute values for the default string interpolation parameters
        to be applied to the template string specified in the stamp
        style. This method does not take into account the ``text_params``
        init parameter yet.

        :return:
            A dictionary containing the parameters and their values.
        """
        ts = datetime.now(tz=tzlocal.get_localzone())
        return {
            'ts': ts.strftime(self.style.timestamp_format),
        }

    def _text_layout(self):
        # Set the contents of the text box
        self.text_box = tb = TextBox(
            self.style.text_box_style,
            writer=self.writer,
            resources=self.resources,
            box=None,
        )
        _text_params = self.get_default_text_params()
        if self.text_params is not None:
            _text_params.update(self.text_params)
        try:
            text = self.style.stamp_text % _text_params
        except KeyError as e:
            raise LayoutError(f"Stamp text parameter '{e.args[0]}' is missing")
        tb.content = text

        # Render the text box in its natural size, we'll deal with
        # the minutiae later
        return tb.render()

    def _inner_layout_natural_size(self):
        # render text
        text_commands = self._text_layout()

        inn_box = self.text_box.box
        return [text_commands], (inn_box.width, inn_box.height)

    def _inner_content_layout_rule(self):
        return self.style.inner_content_layout or DEFAULT_BOX_LAYOUT

    def _render_inner_content(self):
        command_stream = [b'q']

        # compute the inner bounding box
        inn_commands, (
            inn_width,
            inn_height,
        ) = self._inner_layout_natural_size()

        inner_layout = self._inner_content_layout_rule()

        bbox = self.box

        # position the inner box
        inn_position = inner_layout.fit(bbox, inn_width, inn_height)

        command_stream.append(inn_position.as_cm())
        command_stream.extend(inn_commands)
        command_stream.append(b'Q')

        return command_stream

STAMP_ART_CONTENT = content.RawContent(
    box=layout.BoxConstraints(width=100, height=100),
    data=b'''
q 1 0 0 -1 0 100 cm 
0.603922 0.345098 0.54902 rg
3.699 65.215 m 3.699 65.215 2.375 57.277 7.668 51.984 c 12.957 46.695 27.512
 49.34 39.418 41.402 c 39.418 41.402 31.48 40.078 32.801 33.465 c 34.125
 26.852 39.418 28.172 39.418 24.203 c 39.418 20.234 30.156 17.59 30.156
14.945 c 30.156 12.297 28.465 1.715 50 1.715 c 71.535 1.715 69.844 12.297
 69.844 14.945 c 69.844 17.59 60.582 20.234 60.582 24.203 c 60.582 28.172
 65.875 26.852 67.199 33.465 c 68.52 40.078 60.582 41.402 60.582 41.402
c 72.488 49.34 87.043 46.695 92.332 51.984 c 97.625 57.277 96.301 65.215
 96.301 65.215 c h f
3.801 68.734 92.398 7.391 re f
3.801 79.512 92.398 7.391 re f
3.801 90.289 92.398 7.391 re f
Q
''',
)
"""
Hardcoded stamp background that will render a stylised image of a stamp using 
PDF graphics operators (see below).

.. image:: images/stamp-background.svg
   :alt: Standard stamp background
   :align: center
   
"""