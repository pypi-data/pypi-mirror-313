"""在docx文件中添加图片"""

import os
import shutil
import uuid
from pathlib import Path as _p

from .utils import check


@check()
def append_two_docs(original_docx_name: _p, append_docx_name: _p, output_path: _p):
    """合并两个 docx 文件"""
    result = os.system(
        f"pandoc {original_docx_name} {append_docx_name} -o {output_path}"
    )
    if result != 0:
        raise RuntimeError(
            f"Failed to merge {original_docx_name} and {append_docx_name}"
        )


def append_doclist_to_docx(
    original_docx_name: _p, append_docx_list: list[_p], output_path: _p
):
    if len(append_docx_list) == 0:
        raise ValueError("append_docx_list is empty")

    tmp_folder = original_docx_name.parent / "tmp"
    tmp_folder.mkdir(exist_ok=True)
    midfile = tmp_folder / f"{uuid.uuid4()}.docx"

    append_two_docs(original_docx_name, append_docx_list[0], midfile)

    for append_docx_name in append_docx_list[1:]:
        append_two_docs(midfile, append_docx_name, midfile)

    shutil.move(midfile, output_path)
