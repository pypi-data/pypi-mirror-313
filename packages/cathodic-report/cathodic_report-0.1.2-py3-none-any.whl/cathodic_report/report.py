"""
用于创建报告的总入口, 用户通过这个类来创建报告文件

{{p beginning_doc}}
{{p summary_table_doc}}
{{p graph_doc}}

{{p device_header}}
{{p device_table}}
{{p device_graph}}
"""

import datetime
import pathlib as pl
import uuid

from cathodic_report.funcs import get_date_name
from cathodic_report.wordfile import append, font, forms, render

from . import draw, graph, table
from .checker import UniqueChecker

_p = pl.Path


class Report(object):
    def __init__(self, workdir: str | None = None):
        if workdir is None:
            self.workdir = get_date_name(_p("."))
        else:
            self.workdir = pl.Path(workdir)

        # 创建一个唯一的文件夹
        self.workdir = self.workdir / (
            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            + "-"
            + self.unique_id()
        )
        self.workdir.mkdir(exist_ok=True)
        self.checker = UniqueChecker()

    def template_folder_fn(self) -> _p:
        return _p("./src/notebooks/templates")

    def unique_id(self) -> str:
        return str(uuid.uuid4())

    def create_new_output(self, name: str) -> _p:
        output_path = self.workdir / _p(f"{name}")
        self.checker.add(output_path)
        return output_path

    def render_all(self, report: forms.ReportForm):
        o1 = self.render_beginning_doc(report.header)
        o2 = self.render_summary_table_doc(report.summary_table)

        summary_output = self.create_new_output("summary.docx")

        # using new append function
        append.append_two_docs(o1, o2, summary_output)

        graph_output = self.render_graph_doc(report.graph_data)

        summary_final = self.create_new_output("summary-final.docx")
        append.append_two_docs(summary_output, graph_output, summary_final)

        output_list = []
        for item in report.device_info:
            output_list.append(self.render_device(item))

        final_output = self.create_new_output("final.docx")
        append.append_doclist_to_docx(summary_final, output_list, final_output)

        # change font to SimSun
        # font.change_font(final_output)
        font.update_doc(final_output, self.template_folder_fn() / "reference.docx")

    def render_beginning_doc(self, report: forms.ReportForm.ReportHeader):
        output_path = self.create_new_output("beginning.docx")
        render.render_beginning(
            self.template_folder_fn, context=report, output_path=output_path
        )
        return output_path

    def render_summary_table_doc(self, data: list[forms.SummaryForm]):
        output_path = self.create_new_output("summary_table.docx")
        table.gen_table(data, output_path)
        return output_path

    def render_graph_doc(self, data: graph.GraphData):
        # draw ac and dc data.
        # circle graph.
        assert len(data.circle_graph) == 2, "must be ac and dc"
        circle_output_list = []
        graph_dict = {}
        for item in data.circle_graph:
            output_path = self.create_new_output(f"circle_graph_{item.types}.png")
            graph_dict[item.types] = output_path
            circle_output_list.append(draw.draw_circle_graph(item, output_path))

        line_output_list = [
            self.create_new_output("potential.png"),
            self.create_new_output("dc_density.png"),
            self.create_new_output("ac_density.png"),
            self.create_new_output("dc_voltage.png"),
            self.create_new_output("ac_voltage.png"),
            self.create_new_output("resistivity.png"),
        ]
        image_context = forms.TotalImageContext(
            circle_graph_ac=str(graph_dict["ac"]),
            circle_graph_dc=str(graph_dict["dc"]),
            line_graph_1=str(line_output_list[0]),
            line_graph_2=str(line_output_list[1]),
            line_graph_3=str(line_output_list[2]),
            line_graph_4=str(line_output_list[3]),
            line_graph_5=str(line_output_list[4]),
            line_graph_6=str(line_output_list[5]),
        )

        # line graph
        draw.draw_line_potential(data.potential, line_output_list[0])
        draw.draw_line_density_dc(data.dc_density, line_output_list[1])
        draw.draw_line_density_ac(data.ac_density, line_output_list[2])
        draw.draw_line_voltage_dc(
            data.dc_voltage,
            line_output_list[3],
        )
        draw.draw_line_voltage_ac(data.ac_voltage, line_output_list[4])
        draw.draw_line_resistivity(data.resistivity, line_output_list[5])

        graph_output = self.create_new_output("graph-final.docx")
        render.render_graph(
            self.template_folder_fn() / "graph-template.docx",
            image_context=image_context,
            output_path=graph_output,
        )

        return graph_output

    def render_device(self, device_info: forms.DeviceInfo):
        header_path = self._render_device_header(device_info.device_form)
        table_path = self._render_device_table(device_info.table_forms)
        graph_path = self._render_device_graph(device_info.graph_data)

        device_part = self.create_new_output(
            f"device-{device_info.device_form.id}.docx"
        )
        append.append_doclist_to_docx(
            header_path, [*table_path, graph_path], device_part
        )
        return device_part

    def _render_device_table(self, data: list[forms.TableForm]) -> list:
        output_list = []
        for item in data:
            output_path = self.create_new_output(f"device-table-{item.id}.docx")
            table.render_device_table(
                self.template_folder_fn(),
                item.table_data,
                output_path,
            )
            output_list.append(output_path)
        return output_list

    def _render_device_header(self, data: forms.DeviceForm):
        output_path = self.create_new_output(f"device-header-{data.id}.docx")
        render.render_device(
            self.template_folder_fn,
            forms.DeviceForm.model_validate(data),
            output_path=output_path,
        )
        return output_path

    def _render_device_graph(self, data: forms.DeviceTimeSeries):
        output_list = [
            self.create_new_output(f"poweron-off-{data.id}.png"),
            self.create_new_output(f"ac_density-{data.id}.png"),
            self.create_new_output(f"dc_density-{data.id}.png"),
            self.create_new_output(f"ac_voltage-{data.id}.png"),
        ]
        image_context = forms.DeviceImageContext(
            poweron_off=str(output_list[0]),
            ac_density=str(output_list[1]),
            dc_density=str(output_list[2]),
            ac_voltage=str(output_list[3]),
        )
        draw.draw_2_time_series_graph(data.poweron, data.poweroff, output_list[0])
        draw.draw_time_series_graph(data.ac_density, output_list[1])
        draw.draw_time_series_graph(data.dc_density, output_list[2])
        draw.draw_time_series_graph(data.ac_voltage, output_list[3])

        output_path = self.create_new_output(f"device_graph_{data.id}.docx")
        render.render_graph(
            self.template_folder_fn() / "device-graph-template.docx",
            image_context=image_context,
            output_path=output_path,
        )
        return output_path
