from typing import List, Dict
from dataclasses import dataclass, field


@dataclass
class BaseExecutor:
    executable: List[str] = None
    file: str = None
    env: Dict[str, str] = field(default_factory=lambda: {})

    @property
    def exec(self):
        return self.executable + [self.file]
