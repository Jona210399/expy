from dataclasses import dataclass
from experiment_handling.config_loader import ConfigLoader


@dataclass
class TrainingParameters:
    epochs: int
    batch_size: int
    lr: float


@dataclass
class EnvironmentParameters:
    num_workers: int
    seed: int
    mylist: list[int]


@dataclass
class Config:
    training_parameters: TrainingParameters
    environment: EnvironmentParameters


config: Config = ConfigLoader("config.yaml").get_config_as_dataclass(Config)
config: Config = ConfigLoader("config.yaml").get_config_as_dataclass(
    Config, strict=True
)
