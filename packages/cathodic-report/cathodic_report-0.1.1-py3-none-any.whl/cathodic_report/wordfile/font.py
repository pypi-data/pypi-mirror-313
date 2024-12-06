from __future__ import annotations

import os
import pathlib

from docx import Document
from docx.oxml.ns import qn


def change_font(doc: Document | pathlib.Path, font_name: str = "宋体"):
    if isinstance(doc, pathlib.Path):
        doc = Document(doc)

    # 修改预定义样式的字体
    styles_to_change = ["Normal", "Title"] + [f"Heading {i}" for i in range(1, 10)]
    for style_name in styles_to_change:
        if style_name in doc.styles:
            style = doc.styles[style_name]
            style.font.name = font_name
            style._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)

    # 遍历所有段落并修改字体
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.font.name = font_name
            run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)

    return doc


def update_doc(doc: Document | pathlib.Path, template: pathlib.Path):
    result = os.system(f"pandoc {doc} --reference-doc {template} -o {doc}")
    if result != 0:
        raise RuntimeError(f"pandoc failed with code {result}")
