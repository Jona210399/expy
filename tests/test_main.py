from expy.experiment import Experiment
from expy.enivronment_loader import EnvironmentLoader
from expy.io import IOConfiguration
from expy.wandb.manager import WandbConfiguration, WandbManager
from expy.config_loader import ConfigLoader
from dataclasses import dataclass


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
    config = ConfigLoader("experiment_handling/config.yaml").get_config_as_dataclass(
        dataclass=Config
    )
    print(config)

    wandb_manager = WandbManager(config)
    wandb_manager.inititialize_wandb()

    training_process(config.training_parameters)

    print(config.io.output_dir)


if __name__ == "__main__":
    main()
