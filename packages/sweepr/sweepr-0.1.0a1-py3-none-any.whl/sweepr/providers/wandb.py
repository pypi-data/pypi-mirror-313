from typing import Iterable, Iterator
from tqdm.auto import tqdm
import os
from dataclasses import dataclass, field
from enum import Enum

try:
    import wandb
    import wandb.apis
except ImportError:
    raise ImportError("Missing wandb. Install using `pip install wandb`.")

from .base import BaseProvider
from ..types import ArgsDict
from ..run import Run


@dataclass
class WandBProvider(BaseProvider):
    api_key: str = field(default=os.getenv(wandb.env.API_KEY))
    entity: str = field(default=os.getenv(wandb.env.ENTITY))
    project: str = field(default=os.getenv(wandb.env.PROJECT))
    sweep_id: str = field(default=os.getenv(wandb.env.SWEEP_ID))

    class State(str, Enum):
        FINISHED = "finished"
        FAILED = "failed"
        CRASHED = "crashed"
        RUNNING = "running"

    def __post_init__(self):
        self.api = wandb.Api(
            api_key=self.api_key,
            overrides={
                "entity": self.entity,
                "project": self.project,
            },
        )

    def runs(self, config_keys: Iterable[str]) -> Iterator[ArgsDict]:
        yield from self._get_run_configs(filter_keys=config_keys)

    def process(self, run: Run, sweep=None):
        if self.entity:
            run.env[wandb.env.ENTITY] = self.entity

        if self.project:
            run.env[wandb.env.PROJECT] = self.project

        if self.sweep_id:
            run.env[wandb.env.SWEEP_ID] = self.sweep_id

        if sweep:
            run.env[wandb.env.TAGS] = ",".join(sweep.tags)

        run.env[wandb.env.RESUME] = "allow"

        run.env[wandb.env.RUN_ID] = run.id

        return run

    def _get_runs(
        self, filters: dict = None, per_page: int = 1000, **kwargs
    ) -> Iterator[wandb.apis.public.Run]:
        filters = filters or {}
        if self.sweep_id:
            filters["sweep"] = self.sweep_id

        return self.api.runs(filters=filters, per_page=per_page, **kwargs)

    def _get_unfinished_runs(
        self, filters: dict = None, **kwargs
    ) -> Iterator[wandb.apis.public.Run]:
        filters = {
            **(filters or {}),
            "state": {
                "$nin": [
                    self.State.FINISHED,
                    self.State.RUNNING,
                ]
            },
        }

        return self._get_runs(filters=filters, **kwargs)

    def _get_run_configs(
        self, filter_keys: Iterable[str] = None, **kwargs
    ) -> Iterator[ArgsDict]:
        filter_keys = set(filter_keys or [])
        for run in tqdm(self._get_runs(**kwargs), leave=False):
            yield {k: v for k, v in run.config.items() if k in filter_keys}
