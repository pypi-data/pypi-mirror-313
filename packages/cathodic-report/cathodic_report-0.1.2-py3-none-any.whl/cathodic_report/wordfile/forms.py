import datetime
import typing as t

from pydantic import BaseModel, Field

from .. import graph


class ReportForm(BaseModel):
    class ReportHeader(BaseModel):
        project_name: str
        file_num: int

    header: ReportHeader
    summary_table: list["SummaryForm"] = Field(..., min_length=1)
    graph_data: graph.GraphData
    device_info: list["DeviceInfo"] = Field(..., min_length=1)


class TableForm(BaseModel):
    id: int
    table_data: graph.DeviceTable


class DeviceForm(BaseModel):
    id: int
    device_id: str
    distance: float
    piece_area: float
    resistivity: float
    judge_metric: float
    protect_status: t.Literal["有", "无"]


class TimeSeries(BaseModel):
    name: str
    time: list[datetime.datetime]
    value: list[float]


class DeviceTimeSeries(BaseModel):
    id: int
    poweron: TimeSeries
    poweroff: TimeSeries
    ac_density: TimeSeries
    dc_density: TimeSeries
    ac_voltage: TimeSeries


class DeviceInfo(BaseModel):
    device_form: DeviceForm
    table_forms: list[TableForm] = Field(..., min_length=1)
    graph_data: DeviceTimeSeries


class SummaryForm(BaseModel):
    id: int
    device_id: str
    distance: float
    piece_area: float
    resistivity: float
    ac_judge_result: t.Literal["高", "中", "低"]
    dc_judge_result: t.Literal["高", "中", "低"]


class TotalImageContext(BaseModel):
    circle_graph_ac: str
    circle_graph_dc: str
    line_graph_1: str
    line_graph_2: str
    line_graph_3: str
    line_graph_4: str
    line_graph_5: str
    line_graph_6: str


class DeviceImageContext(BaseModel):
    poweron_off: str
    ac_density: str
    dc_density: str
    ac_voltage: str
