# render word file

import pathlib as pl
import typing as t

from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage

from . import forms

get_template_fn = t.Callable[[], pl.Path]


def base_render(
    template_fn: get_template_fn,
    context: forms.BaseModel,
    output_path: pl.Path,
):
    doc = DocxTemplate(template_fn())
    doc.render(context.model_dump())
    doc.save(output_path)


def gen_template_fn(
    template_folder_fn: get_template_fn, filename: str
) -> t.Callable[[], pl.Path]:
    def template_fn():
        return template_folder_fn() / filename

    return template_fn


def generate_render_fn(filename: str, form_cls: t.Type[forms.BaseModel]):
    """渲染文件"""

    def render_fn(
        template_folder_fn: get_template_fn,
        context: form_cls,
        output_path: pl.Path,
    ):
        template_fn = gen_template_fn(template_folder_fn, filename)
        return base_render(template_fn, context, output_path)

    return render_fn


def render_graph(
    name,
    image_context: forms.TotalImageContext | forms.DeviceImageContext,
    output_path,
):
    doc = DocxTemplate(name)

    images = image_context.model_dump()
    for k, v in images.items():
        images[k] = InlineImage(doc, v, width=Mm(50))

    doc.render(images)
    doc.save(output_path)


render_beginning = generate_render_fn("beginning.docx", forms.ReportForm)
render_device = generate_render_fn("device-template.docx", forms.DeviceForm)
