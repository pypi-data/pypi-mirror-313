from enum import IntEnum
from typing import Literal

from pydantic import BaseModel, Field


# Circle Graph
class CircleGraph(BaseModel):
    types: Literal["ac", "dc"]
    judge_result_data: list["JudgeLevel"]

    def judge_result_data_validate(self):
        if len(self.judge_result_data) == 0:
            raise ValueError("judge_result_data is empty")


class JudgeLevel(IntEnum):
    unknown = -1
    high = 1
    mid = 2
    low = 3


class DistanceBase(BaseModel):
    distance: list[float]
    device_id: list[str]

    def get_data(self):
        raise NotImplementedError("This method must be implemented in the subclass.")


# Plot Graph
class ElecData(DistanceBase):
    elec_potential_avg: list[float]
    elec_potential_min: list[float]
    elec_potential_max: list[float]
    v_off_avg: list[float]
    v_off_min: list[float]
    v_off_max: list[float]

    def get_data(self):
        return self.elec_potential_avg, self.v_off_avg


class LineGraph2(DistanceBase):
    avg_value: list[float]
    min_value: list[float]
    max_value: list[float]

    def get_data(self):
        return self.avg_value


class ResisData(DistanceBase):
    resistivity: list[float]

    def get_data(self):
        return self.resistivity


class GraphData(BaseModel):
    circle_graph: list[CircleGraph] = Field(default_factory=list, min_length=1)
    potential: ElecData
    dc_density: LineGraph2
    ac_density: LineGraph2
    dc_voltage: LineGraph2
    ac_voltage: LineGraph2
    resistivity: ResisData


class StaticValue(BaseModel):
    min: float
    max: float
    mean: float
    median: float
    var: float


class DeviceTable(BaseModel):
    table_name: str
    c_type: Literal["交流", "直流"]
    start_time: str
    end_time: str
    total_time: int

    po: StaticValue
    pf: StaticValue
    dc_density: StaticValue
    ac_density: StaticValue
    ac_voltage: StaticValue
    judge_result: str

    def get_data(self):
        return {
            "table_name": self.table_name,
            "c_type": self.c_type,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_time": self.total_time,
            "po_min": round(self.po.min, 3),
            "po_max": round(self.po.max, 3),
            "po_mean": round(self.po.mean, 3),
            "po_median": round(self.po.median, 3),
            "po_var": round(self.po.var, 3),
            "pf_min": round(self.pf.min, 3),
            "pf_max": round(self.pf.max, 3),
            "pf_mean": round(self.pf.mean, 3),
            "pf_median": round(self.pf.median, 3),
            "pf_var": round(self.pf.var, 3),
            "dc_min": round(self.dc_density.min, 3),
            "dc_max": round(self.dc_density.max, 3),
            "dc_mean": round(self.dc_density.mean, 3),
            "dc_median": round(self.dc_density.median, 3),
            "dc_var": round(self.dc_density.var, 3),
            "ac_min": round(self.ac_density.min, 3),
            "ac_max": round(self.ac_density.max, 3),
            "ac_mean": round(self.ac_density.mean, 3),
            "ac_median": round(self.ac_density.median, 3),
            "ac_var": round(self.ac_density.var, 3),
            "vo_min": round(self.ac_voltage.min, 3),
            "vo_max": round(self.ac_voltage.max, 3),
            "vo_mean": round(self.ac_voltage.mean, 3),
            "vo_median": round(self.ac_voltage.median, 3),
            "vo_var": round(self.ac_voltage.var, 3),
            "judge_result": self.judge_result,
        }
