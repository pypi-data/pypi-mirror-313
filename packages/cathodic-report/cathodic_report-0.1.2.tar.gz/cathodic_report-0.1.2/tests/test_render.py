import os
import pathlib as pl

from cathodic_report.wordfile import forms, render


def get_template_fn() -> pl.Path:
    return pl.Path("./src/notebooks/templates")


def test_render_device():
    context = {
        "id": 2,
        "device_id": "Device Test No.1",
        "distance": 1,
        "piece_area": 1,
        "resistivity": 1,
        "judge_metric": -0.85,
        "protect_status": "有",
    }

    render.render_device(
        get_template_fn,
        forms.DeviceForm.model_validate(context),
        "./tmp/generated_device.docx",
    )

    assert os.path.exists("./tmp/generated_device.docx")
    # os.remove("./tmp/generated_device.docx")


def test_render_graph():
    template_file = get_template_fn() / "graph-template.docx"
    pic_dir = pl.Path("./src/notebooks/pics")
    render.render_graph(
        template_file,
        forms.TotalImageContext(
            circle_graph_ac=str(pic_dir / "circle_graph.png"),
            circle_graph_dc=str(pic_dir / "circle_graph.png"),
            line_graph_1=str(pic_dir / "circle_graph.png"),
            line_graph_2=str(pic_dir / "circle_graph.png"),
            line_graph_3=str(pic_dir / "circle_graph.png"),
            line_graph_4=str(pic_dir / "circle_graph.png"),
            line_graph_5=str(pic_dir / "circle_graph.png"),
            line_graph_6=str(pic_dir / "circle_graph.png"),
        ),
        "./tmp/generated_graph.docx",
    )
