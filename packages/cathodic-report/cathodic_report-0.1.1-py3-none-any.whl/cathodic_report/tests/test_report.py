import json

from cathodic_report.report import Report
from cathodic_report.wordfile import forms


def test_report():
    with open("./src/resources/report_form.json", "r", encoding="utf-8") as f:
        report_form = forms.ReportForm.model_validate(json.load(f))

    report = Report(workdir="./tmp/")
    report.render_all(report_form)
