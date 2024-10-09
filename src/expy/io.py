from pathlib import Path
from dataclasses import dataclass, field


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

    def create_output_dir(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
