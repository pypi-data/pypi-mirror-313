# data types for report

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from . import graph


# for input data
class Report(BaseModel):
    title: str
    project_name: str
    file_nums: int

    summary: list["StrayCurrentJudge"]
    analysis_results: list["AnalysisData"]

    def get_circle_graph(self, types: Literal["ac", "dc"]) -> graph.CircleGraph:
        """compute judge result for circle graph"""
        judge_results = [i.get_result(types) for i in self.summary]
        return graph.CircleGraph(judge_result_data=judge_results, types=types)

    def get_line_graph(self, types: Literal["ac", "dc"]) -> graph.ElecData:
        """compute judge result for line graph"""
        distances = [i.distance for i in self.summary]
        device_ids = [i.device_id for i in self.summary]
        elec_potentials = [i.elec_potential for i in self.summary]
        v_offs = [i.v_off for i in self.summary]
        return graph.ElecData(
            distance=distances,
            device_id=device_ids,
            elec_potential=elec_potentials,
            v_off=v_offs,
        )

    def gen_table(self) -> str:
        from .table import gen_table

        return gen_table(self.summary)


class StrayCurrentJudge(BaseModel):
    id: str
    device_id: str
    distance: float
    area: float
    resistivity: float

    # all of them are average value
    elec_potential: float
    v_off: float
    dc_density: float
    ac_density: float
    ac_voltage: float

    ac_judge_result: Literal["mid", "high", "low"]
    dc_judge_result: Literal["mid", "high", "low"]

    def get_result(self, types: Literal["ac", "dc"]) -> graph.JudgeLevel:
        mapping = {
            "mid": graph.JudgeLevel.mid,
            "high": graph.JudgeLevel.high,
            "low": graph.JudgeLevel.low,
        }
        return (
            mapping[self.ac_judge_result]
            if types == "ac"
            else mapping[self.dc_judge_result]
        )


class AnalysisData(BaseModel):
    device_id: str
    distance: float
    area: float
    resistivity: float
    judge_metric: float
    ac_result: "CurrentResult"
    dc_result: "CurrentResult"


class CurrentResult(BaseModel):
    start_time: datetime
    end_time: datetime
    elec_potential: "RowData"
    v_off: "RowData"
    ac_density: "RowData"
    dc_density: "RowData"
    ac_voltage: "RowData"
    judge_result: str

    def total_time(self):
        # get total time in hours
        return (self.end_time - self.start_time).total_seconds() / 60 / 60


class RowData(BaseModel):
    max_v: float
    min_v: float
    avg_v: float
    mid_v: float
    var_v: float
