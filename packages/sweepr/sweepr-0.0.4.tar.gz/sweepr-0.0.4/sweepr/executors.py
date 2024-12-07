from typing import List, Dict, Optional, Union
from enum import Enum
from dataclasses import dataclass, field


@dataclass
class BaseExecutor:
    executable: List[str] = None
    file: str = None
    env: Dict[str, str] = field(default_factory=lambda: {})

    @property
    def exec(self):
        return self.executable + [self.file]


@dataclass
class Python(BaseExecutor):
    executable: List[str] = field(default_factory=lambda: ["python"])


@dataclass
class Pueue(BaseExecutor):
    executable: List[str] = field(default_factory=lambda: ["puv", "python"])
    gpus: Optional[int] = field(default=None)

    class Env(str, Enum):
        GPUS = "GPUS"

    def __post_init__(self):
        if self.gpus is not None:
            self.env[self.Env.GPUS.value] = self.gpus


@dataclass
class Slurm(BaseExecutor):
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
