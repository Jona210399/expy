from dataclasses import dataclass

from expy.core import ConfigLoader, Experiment, IOConfiguration, parse_config_path
from expy.wandb import WandbConfiguration, WandbManager


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
    experiment: Experiment
    wandb: WandbConfiguration
    io: IOConfiguration
    environment: EnvironmentParameters
    training_parameters: TrainingParameters


def training_process(training_params: TrainingParameters):
    pass


def main():
    config_path = parse_config_path()
    config = ConfigLoader(config_path).get_config_as_dataclass(dataclass=Config)
    print(config)

    wandb_manager = WandbManager(config)
    run = wandb_manager.initialize()

    print(run.config)
    config.io.create_output_dir()

    training_process(config.training_parameters)

    print(config.io.output_dir)


if __name__ == "__main__":
    main()
