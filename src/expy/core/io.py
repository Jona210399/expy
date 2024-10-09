from dataclasses import dataclass, field
from pathlib import Path

from expy.distributed.rank_zero import rank_zero_only


@dataclass
class IOConfiguration:
    root_output_dir: Path
    root_input_dir: Path
    output_dir: Path = field(init=False, default=Path())

    def __post_init__(self):
        self.root_output_dir = Path(self.root_output_dir)
        self.root_input_dir = Path(self.root_input_dir)

    def set_output_dir(self, output_dir_name: Path):
        self.output_dir = self.root_output_dir.joinpath(output_dir_name)

    @rank_zero_only
    def create_output_dir(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
