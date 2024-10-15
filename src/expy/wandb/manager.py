import os
from dataclasses import asdict, dataclass, field
from typing import Protocol, runtime_checkable

import wandb
from wandb.util import generate_id

from expy.core import Experiment, IOConfiguration
from expy.distributed.rank_zero import rank_zero_only
from expy.wandb.dummy_run import WandbDummyRun


@dataclass
class WandbConfiguration:
    enabled: bool
    run_id: str | None
    resume: bool = field(init=False, default=False)

    def __post_init__(self):
        if not self.run_id:
            self.resume = False
            self.run_id = generate_id()
            return
        self.run_id = str(self.run_id)
        self.resume = True


@runtime_checkable
@dataclass
class Configuration(Protocol):
    experiment: Experiment
    wandb: WandbConfiguration
    io: IOConfiguration


class WandbManager:
    def __init__(
        self,
        config: Configuration,
    ) -> None:

        self.config = config
        self.experiment = config.experiment
        self.wandb_config = config.wandb
        self.io_config = config.io

    def initialize(self) -> wandb.sdk.wandb_run.Run | WandbDummyRun:
        run = self._initialize_wandb()
        return run or WandbDummyRun()

    @rank_zero_only
    def _initialize_wandb(
        self,
    ) -> wandb.sdk.wandb_run.Run | WandbDummyRun | None:
        if not self.wandb_config.enabled:
            return WandbDummyRun()

        os.environ["WANDB_SERVICE_WAIT"] = "300"
        # We set this environment variable to avoid connection issues with wandb.

        if self.wandb_config.resume:
            return self._resume_run()

        return self._initialize_new_run()

    def _resume_run(self) -> wandb.sdk.wandb_run.Run:
        config: dict = (
            wandb.Api()
            .run(
                self.experiment.to_project_root_path()
                .joinpath(self.wandb_config.run_id)
                .as_posix()
            )
            .config
        )

        # Resumed runs should have the same output directory as the original run.
        experiment: dict = config.get("experiment")
        self.experiment.set_date_time(experiment.get("date_time"))
        self.io_config.set_output_dir(self.experiment.to_path())

        run = wandb.init(
            project=self.experiment.project_name,
            entity=self.experiment.team_name,
            id=self.wandb_config.run_id,
            resume="must",
            settings=wandb.Settings(_service_wait=300),
            config=asdict(self.config),
            dir=self.io_config.output_dir,
        )
        return run

    def _initialize_new_run(self) -> wandb.sdk.wandb_run.Run:
        self.io_config.set_output_dir(self.experiment.to_path())
        self.io_config.create_output_dir()

        return wandb.init(
            project=self.experiment.project_name,
            entity=self.experiment.team_name,
            id=self.wandb_config.run_id,
            config=asdict(self.config),
            name="_".join([self.experiment.experiment_name, self.experiment.date_time]),
            dir=self.io_config.output_dir,
        )
