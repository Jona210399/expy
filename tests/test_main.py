from experiment_handling.experiment import Experiment
from experiment_handling.enivronment_loader import EnvironmentLoader
from experiment_handling.io import IOConfiguration
from experiment_handling.wandb.manager import WandbManager, WandbConfiguration
from experiment_handling.config_loader import ConfigLoader
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


def main():
    config: Config = ConfigLoader(
        "experiment_handling/config.yaml"
    ).get_config_as_dataclass(dataclass=Config)
    print(config)

    wandb_manager = WandbManager(config)
    wandb_manager.inititialize_wandb()

    print(config.io.output_dir)


if __name__ == "__main__":
    main()
