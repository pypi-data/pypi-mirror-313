from typing import List
from dataclasses import dataclass, field

from .base import BaseExecutor


@dataclass
class PythonExecutor(BaseExecutor):
    executable: List[str] = field(default_factory=lambda: ["python"])
