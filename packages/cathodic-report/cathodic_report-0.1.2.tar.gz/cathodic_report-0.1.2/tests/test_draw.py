import datetime
import os

import pytest

from cathodic_report import draw, graph, utils
from cathodic_report.graph import CircleGraph, JudgeLevel
from cathodic_report.wordfile import forms


def set_tmp_folder(path: str):
    os.makedirs("./tmp/", exist_ok=True)
    return os.path.join("./tmp/", path)


_t = set_tmp_folder


# random data
def test_draw_circle_graph():
    def create_fake():
        judge_result_data = [
            JudgeLevel.high,
            JudgeLevel.mid,
            JudgeLevel.low,
            JudgeLevel.high,
            JudgeLevel.mid,
        ]

        circle_graph = CircleGraph(types="ac", judge_result_data=judge_result_data)
        return circle_graph

    def load_from_tmp():
        filename = _t("ac.json")
        return utils.load_from_file(filename, CircleGraph)

    # Call the function to display the graph
    circle_graph = create_fake()
    output_file = _t("pics/circle_graph.png")
    draw.draw_circle_graph(circle_graph, output_file, is_show=False)

    # remove the file
    def remove_temp_file():
        if os.path.exists(output_file):
            os.remove(output_file)

    remove_temp_file()


def test_draw_line_elec():
    # 画出折线图, 只显示几个测试桩即可，将里程数据作为横坐标数据
    # 多行数据

    example_data: graph.ElecData = graph.ElecData(
        device_id=["device1", "device2", "device3"],
        distance=[1, 2, 3],
        elec_potential_avg=[-0.5, 2.3, 4.8],
        elec_potential_min=[-1.2, 1.5, 3.9],
        elec_potential_max=[0.8, 3.2, 5.7],
        v_off_avg=[-0.8, 1.5, 3.2],
        v_off_min=[-1.5, 0.7, 2.4],
        v_off_max=[0.2, 2.8, 4.5],
    )

    output_file = _t("pics/line_graph1.png")
    draw.draw_line_potential(example_data, output_file, is_show=False)

    if os.path.exists(output_file):
        os.remove(output_file)


def test_draw_device_graph():
    time_series = forms.TimeSeries(
        id=1,
        name="通电电位",
        time=[
            datetime.datetime(2024, 1, 1, 0, 0),
            datetime.datetime(2024, 1, 1, 1, 0),
            datetime.datetime(2024, 1, 1, 2, 0),
        ],
        value=[1, 2, 3],
    )
    output_file = _t("pics/time_series_graph.png")
    draw.draw_time_series_graph(time_series, output_file)

    # if os.path.exists(output_file):
    #     os.remove(output_file)
