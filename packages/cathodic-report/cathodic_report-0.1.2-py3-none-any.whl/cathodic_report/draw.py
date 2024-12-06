"""根据图像数据绘制"""

import pathlib as pl

import matplotlib.pyplot as plt

from . import graph
from .wordfile import forms

# 添加以下字体设置代码
# Need to enable docker image.
plt.rcParams["font.sans-serif"] = [
    "WenQuanYi Micro Hei",
    "SimHei",
]  # 首选文泉驛微米黑，备选黑体
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号


def show_and_save_fig(output_path: str, is_show=False):
    # create if parent not exists
    if not pl.Path(output_path).parent.exists():
        pl.Path(output_path).parent.mkdir(parents=True)

    plt.savefig(output_path)
    if is_show:
        plt.show()


def draw_circle_graph(circle_graph: graph.CircleGraph, output_path, is_show=False):
    # Calculate percentages
    total = len(circle_graph.judge_result_data)
    percentages = {
        level: circle_graph.judge_result_data.count(level) / total * 100
        for level in graph.JudgeLevel
    }

    # Create pie chart
    labels = [level.name for level in graph.JudgeLevel]
    sizes = [percentages[level] for level in graph.JudgeLevel]
    colors = ["#FF9999", "#66B2FF", "#99FF99"]  # You can customize colors

    plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    plt.axis("equal")
    plt.title(f"{circle_graph.types.upper()} Judge Level Distribution")
    show_and_save_fig(output_path, is_show)
    return output_path


def draw_line_potential(line_graph: graph.ElecData, output_path, is_show=False):
    plt.figure(figsize=(10, 6))

    # Plot elec_potential
    plt.plot(
        line_graph.distance,
        line_graph.elec_potential_avg,
        label="通电电位平均值",
        marker="o",
    )

    plt.plot(
        line_graph.distance,
        line_graph.elec_potential_min,
        label="通电电位最小值",
        marker="v",
    )

    plt.plot(
        line_graph.distance,
        line_graph.elec_potential_max,
        label="通电电位最大值",
        marker="^",
    )

    plt.plot(
        line_graph.distance,
        line_graph.v_off_avg,
        label="断电电位平均值",
        marker="o",
    )

    plt.plot(
        line_graph.distance,
        line_graph.v_off_min,
        label="断电电位最小值",
        marker="v",
    )

    plt.plot(
        line_graph.distance,
        line_graph.v_off_max,
        label="断电电位最大值",
        marker="^",
    )

    plt.xlabel("里程/km")
    plt.ylabel("电位数值/V")
    plt.title("通电电位和断电点位与里程关系")
    plt.legend()

    # Add device_id labels to x-axis
    plt.xticks(line_graph.distance, line_graph.device_id, rotation=45, ha="right")

    plt.grid(True)
    plt.tight_layout()
    show_and_save_fig(output_path, is_show)


def _draw_three_line_graph(
    line_graph, y_label, label_unit, title, output_path, is_show=False
):
    """绘制三行数据图
    line_graph: 数据图
    y_label: y轴标签
    label_unit: y轴单位
    title: 图表标题
    output_path: 输出路径
    is_show: 是否显示
    """
    plt.figure(figsize=(10, 6))

    # Plot elec_potential
    plt.plot(
        line_graph.distance,
        line_graph.avg_value,
        label="平均值",
        marker="o",
    )

    plt.plot(
        line_graph.distance,
        line_graph.min_value,
        label="最小值",
        marker="o",
    )

    plt.plot(
        line_graph.distance,
        line_graph.max_value,
        label="最大值",
        marker="o",
    )

    plt.xlabel("里程/km")
    plt.ylabel(f"{y_label}{label_unit}")
    plt.title(title)
    plt.legend()

    # Add device_id labels to x-axis
    plt.xticks(line_graph.distance, line_graph.device_id, rotation=45, ha="right")

    plt.grid(True)
    plt.tight_layout()
    show_and_save_fig(output_path, is_show)


def _draw_single_line_graph(
    line_graph, y_data, y_label, title, output_path, is_show=False
):
    plt.figure(figsize=(10, 6))
    plt.plot(line_graph.distance, y_data, label=y_label, marker="o")

    plt.xlabel("里程/km")
    plt.ylabel(y_label)
    plt.title(f"{title}与里程关系")
    plt.legend()
    plt.xticks(line_graph.distance, line_graph.device_id, rotation=45, ha="right")
    plt.grid(True)
    plt.tight_layout()
    show_and_save_fig(output_path, is_show)


def draw_line_density_dc(line_graph: graph.LineGraph2, output_path, is_show=False):
    return _draw_three_line_graph(
        line_graph,
        y_label="直流密度",
        label_unit="(A/m²)",
        title="直流密度与里程关系",
        output_path=output_path,
        is_show=is_show,
    )


def draw_line_density_ac(line_graph: graph.LineGraph2, output_path, is_show=False):
    return _draw_three_line_graph(
        line_graph,
        y_label="交流密度",
        label_unit="(A/m²)",
        title="交流密度与里程关系",
        output_path=output_path,
        is_show=is_show,
    )


def draw_line_voltage_ac(line_graph: graph.LineGraph2, output_path, is_show=False):
    return _draw_three_line_graph(
        line_graph,
        y_label="交流电压",
        label_unit="(V)",
        title="交流电压与里程关系",
        output_path=output_path,
        is_show=is_show,
    )


def draw_line_voltage_dc(line_graph: graph.LineGraph2, output_path, is_show=False):
    return _draw_three_line_graph(
        line_graph,
        y_label="直流电流",
        label_unit="(A)",
        title="直流电流与里程关系",
        output_path=output_path,
        is_show=is_show,
    )


def draw_line_resistivity(line_graph: graph.ResisData, output_path, is_show=False):
    return _draw_single_line_graph(
        line_graph,
        line_graph.resistivity,
        y_label="电阻率(Ω·m)",
        title="电阻率与里程关系",
        output_path=output_path,
        is_show=is_show,
    )


def draw_2_time_series_graph(
    time_series_1: forms.TimeSeries,
    time_series_2: forms.TimeSeries,
    output_path,
    is_show=False,
):
    plt.figure(figsize=(10, 6))

    plt.plot(
        time_series_1.time, time_series_1.value, marker="o", label=time_series_1.name
    )
    plt.plot(
        time_series_2.time, time_series_2.value, marker="^", label=time_series_2.name
    )

    plt.xlabel("时间 (h)")
    plt.ylabel(f"{time_series_1.name}和{time_series_2.name}")
    plt.title(f"{time_series_1.name}和{time_series_2.name}与时间关系")

    integer_hours = [t for t in time_series_1.time if t.minute == 0 and t.second == 0]
    hour_labels = [t.strftime("%H:%M") for t in integer_hours]
    plt.xticks(integer_hours, hour_labels)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    show_and_save_fig(output_path, is_show)


def draw_time_series_graph(time_series: forms.TimeSeries, output_path, is_show=False):
    plt.figure(figsize=(10, 6))

    plt.plot(time_series.time, time_series.value, marker="o", label=time_series.name)

    plt.xlabel("时间 (h)")
    plt.ylabel(time_series.name)
    plt.title(f"{time_series.name}与时间关系")
    plt.legend()

    # 修改标签格式为 HH:MM
    integer_hours = [t for t in time_series.time if t.minute == 0 and t.second == 0]
    hour_labels = [t.strftime("%H:%M") for t in integer_hours]
    plt.xticks(integer_hours, hour_labels)

    plt.grid(True)
    plt.tight_layout()

    show_and_save_fig(output_path, is_show)
