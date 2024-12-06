"""使用 python-docx 生成 word 表格"""

import pathlib as pl

from docx import Document
from docx.shared import Cm
from docxtpl import DocxTemplate

from cathodic_report.wordfile.forms import SummaryForm

from . import graph
from .types import StrayCurrentJudge

_p = pl.Path


def gen_table(data: list[SummaryForm], output_path) -> None:
    """生成表格并保存到文件

    Args:
        data: 杂散电流判断数据列表
        output_path: 输出文件路径
    """
    # 创建文档对象
    doc = Document()

    # 表格标题
    headers = [
        "序号",
        "测试桩编号",
        "里程",
        "试片面积",
        "土壤电阻率",
        "直流干扰评价结果",
        "交流干扰评价结果",
    ]

    # 创建表格
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"

    # 设置表头
    header_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        header_cells[i].text = header

    # 填充数据
    for idx, item in enumerate(data, 1):
        row_cells = table.add_row().cells
        row_cells[0].text = str(idx)
        row_cells[1].text = item.device_id
        row_cells[2].text = f"{item.distance:.3f}"
        row_cells[3].text = f"{item.piece_area:.2f}"
        row_cells[4].text = f"{item.resistivity:.2f}"
        row_cells[5].text = item.dc_judge_result
        row_cells[6].text = item.ac_judge_result

    # 设置列宽
    for column in table.columns:
        for cell in column.cells:
            cell.width = Cm(3)

    # 保存文档
    doc.save(output_path)


def render_device_table(template_folder, data: graph.DeviceTable, output_path) -> None:
    doc = DocxTemplate(template_folder / "table-template.docx")
    doc.render(data.get_data())
    doc.save(output_path)


def gen_table_md(data: list[StrayCurrentJudge]) -> str:
    """generate markdown table for report"""
    header = "| 序号 | 测试桩编号 | 里程 | 试片面积 | 土壤电阻率 | 直流干扰评价结果 | 交流干扰评价结果 |\n"

    header += "| ---- | ---------- | ---- | ---------- | ------------ | ---------------- | ---------------- |\n"
    rows = []
    for i, item in enumerate(data):
        rows.append(
            f"| {i+1} | {item.device_id} | {item.distance} | {item.area} | {item.resistivity} | {item.ac_judge_result} | {item.dc_judge_result} |\n"
        )

    return header + "".join(rows)
