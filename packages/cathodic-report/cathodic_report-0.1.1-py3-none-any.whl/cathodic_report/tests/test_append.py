import os
import pathlib as pl

from cathodic_report.wordfile import append


def test_append_two_docs():
    os.makedirs("./tmp/docs", exist_ok=True)
    append.append_two_docs(
        original_docx_name=pl.Path("./src/notebooks/templates/beginning.docx"),
        append_docx_name=pl.Path("./src/notebooks/templates/graph-template.docx"),
        output_path=pl.Path("./tmp/docs/merged.docx"),
    )
