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

    @rank_zero_only(default=lambda: WandbDummyRun())
    def inititialize_wandb(self) -> wandb.wandb_sdk.wandb_run.Run | WandbDummyRun:
        if not self.wandb_config.enabled:
            return WandbDummyRun()

        os.environ["WANDB_SERVICE_WAIT"] = "300"
        # We set this environment variable to avoid connection issues with wandb.

        if self.wandb_config.resume:
            return self._resume_run()

        return self._initialize_new_run()

    def _resume_run(self) -> wandb.wandb_sdk.wandb_run.Run:
        run = wandb.init(
            project=self.experiment.project_name,
            entity=self.experiment.team_name,
            id=self.wandb_config.run_id,
            resume="must",
            settings=wandb.Settings(_service_wait=300),
        )

        # Resumed runs should have the same output directory as the original run.
        experiment: dict = run.config.get("experiment")
        self.experiment.set_date_time(experiment.get("date_time"))
        self.io_config.set_output_dir(self.experiment.to_path())

        # Sync configuration changes to the resumed run.
        run.config.update(asdict(self.config), allow_val_change=True)

        return run

    def _initialize_new_run(self) -> wandb.wandb_sdk.wandb_run.Run:
        self.io_config.set_output_dir(self.experiment.to_path())

        return wandb.init(
            project=self.experiment.project_name,
            entity=self.experiment.team_name,
            id=self.wandb_config.run_id,
            config=asdict(self.config),
            name="_".join([self.experiment.experiment_name, self.experiment.date_time]),
        )
