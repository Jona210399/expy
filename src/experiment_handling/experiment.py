from datetime import datetime
from dataclasses import dataclass, field
from pathlib import PurePath, Path


@dataclass
class Experiment:
    team_name: str | None
    project_name: str
    experiment_name: str
    date_time: str = field(init=False)

    def __post_init__(self):
        date_time = datetime.now()
        self.date_time = date_time.strftime("%d-%m-%Y_%H-%M")

    def set_date_time(self, date_time: str):
        self.date_time = date_time

    def to_path(self) -> Path:
        return PurePath(
            self.team_name or "",
            self.project_name,
            self.experiment_name,
            self.date_time,
        )
