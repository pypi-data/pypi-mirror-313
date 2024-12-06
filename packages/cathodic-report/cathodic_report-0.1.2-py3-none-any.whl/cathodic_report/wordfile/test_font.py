from docx import Document

from cathodic_report.wordfile.font import change_font


def test_change_font():
    doc = Document()
    doc.add_paragraph("test")
    doc.save("./tmp/test.docx")
    change_font(doc)
    doc.save("./tmp/test-changed.docx")
