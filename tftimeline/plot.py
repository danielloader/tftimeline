"""Terraform Apply JSON log parser and plotter"""

import json
import sys
from datetime import datetime, timedelta
from typing import Generator, Optional

import pandas as pd
import plotly.express as px

from tftimeline.models import OutputTypes


class InfrastructureResource:
    def __init__(self, log: dict):
        self.raw: dict = log
        self.resource_id: Optional[str] = log["hook"].get("id_value")
        self.resource_name: str = log["hook"]["resource"]["resource_name"]
        self.resource_type: str = log["hook"]["resource"]["resource_type"]
        self.resource: str = log["hook"]["resource"]["resource"]
        self.finished: datetime = datetime.fromisoformat(
            log["@timestamp"][:-1])
        self.elapsed_time: int = log["hook"]["elapsed_seconds"]

    @property
    def started(self) -> datetime:
        if self.elapsed_time == 0:  # force rendering, zero = no bar
            self.elapsed_time = 1
        return self.finished - timedelta(seconds=self.elapsed_time)


class LogParser:
    def __init__(self):
        self.resources = list(self.parse_stdin())

    @property
    def cumulative_elapsed_time(self) -> int:
        return sum(log.elapsed_time for log in self.resources)

    @property
    def dataframes(self):
        return pd.DataFrame([
            dict(
                Type=record.resource_type,
                Name=record.resource_name,
                ResourceId=record.resource_id,
                Start=record.started,
                Finish=record.finished,
                Duration=record.elapsed_time,
            )
            for record in self.resources
        ])

    def parse_stdin(self) -> Generator[InfrastructureResource, None, None]:
        for line in sys.stdin:
            log_dict: dict = json.loads(line)
            if log_dict.get("type") == "apply_complete":
                yield InfrastructureResource(log_dict)
            if log_dict.get("type") == "destroy_complete":
                yield InfrastructureResource(log_dict)

    def plot(self, filepath: str, filetype: OutputTypes, height: int, width: int):
        fig = px.timeline(
            self.dataframes,
            title="Terraform Timeline",
            x_start="Start",
            x_end="Finish",
            y="Name",
            color="Type",
            hover_name="ResourceId",
            hover_data={
                "Type": True,
                "Name": True,
                "Duration": True,
                "Start": True,
                "Finish": True
            }
        )
        fig.update_yaxes(autorange="reversed")
        if filepath is None:
            fig.show()
            return
        if filetype is OutputTypes.html:
            fig.write_html(filepath)
        if filetype is OutputTypes.json:
            fig.write_json(filepath)
        if filetype is OutputTypes.png:
            fig.write_image(filepath, width=width, height=height)
        if filetype is OutputTypes.svg:
            fig.write_image(filepath, width=width, height=height)
