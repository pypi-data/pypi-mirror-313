from typing import List, Optional
from enum import Enum
from dataclasses import dataclass, field

from .base import BaseExecutor


@dataclass
class PueueExecutor(BaseExecutor):
    executable: List[str] = field(default_factory=lambda: ["puv", "python"])
    gpus: Optional[int] = field(default=None)

    class Env(str, Enum):
        GPUS = "GPUS"

    def __post_init__(self):
        if self.gpus is not None:
            self.env[self.Env.GPUS.value] = self.gpus
