"""测试表格生成功能"""

import os

import pytest  # noqa

from cathodic_report.table import gen_table
from cathodic_report.wordfile.forms import SummaryForm


def test_gen_table():
    """测试生成表格功能"""
    # 准备测试数据
    test_data = [
        SummaryForm(
            id=1,
            device_id="TP-001",
            distance=12.345,
            piece_area=10.0,
            resistivity=100.0,
            dc_judge_result="高",
            ac_judge_result="低",
        ),
        SummaryForm(
            id=2,
            device_id="TP-002",
            distance=13.567,
            piece_area=12.0,
            resistivity=150.0,
            dc_judge_result="高",
            ac_judge_result="中",
        ),
    ]

    # 设置测试文件路径
    output_path = "test_table_output.docx"

    try:
        # 生成表格
        gen_table(test_data, output_path)

        # 验证文件是否创建成功
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0

    finally:
        # 清理测试文件
        if os.path.exists(output_path):
            os.remove(output_path)
