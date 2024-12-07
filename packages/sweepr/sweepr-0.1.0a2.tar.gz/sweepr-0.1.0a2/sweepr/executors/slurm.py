from typing import List, Optional, Union
from enum import Enum
from dataclasses import dataclass, field

from .base import BaseExecutor


@dataclass
class SlurmExecutor(BaseExecutor):
    executable: List[str] = field(default_factory=lambda: ["sdocker", "python"])
    account: Optional[str] = field(default=None)
    timelimit: Optional[int] = field(default=None)
    gpus: Optional[Union[int, str]] = field(default=None)

    class Env(str, Enum):
        ACCOUNT = "SBATCH_ACCOUNT"
        TIMELIMIT = "HH"
        GPUS = "GPUS"

    def __post_init__(self):
        if self.account is not None:
            self.env[self.Env.ACCOUNT.value] = self.account

        if self.timelimit is not None:
            self.env[self.Env.TIMELIMIT.value] = self.timelimit

        if self.gpus is not None:
            self.env[self.Env.GPUS.value] = self.gpus
