from typing import Optional, List
import dataclasses
from dataclasses import dataclass, field, asdict as dataclassasdict
import uuid

from .types import (
    ArgsDict,
    EnvDict,
)


@dataclass
class Run:
    program: List[str]
    args: Optional[ArgsDict] = field(default_factory=lambda: {})
    env: Optional[EnvDict] = field(default_factory=lambda: {})

    @property
    def argv(self):
        return (
            [f"{k}={v}" for k, v in self.env.items()]
            + self.program
            + [f"--{k}={v}" for k, v in self.args.items()]
        )

    def todict(self):
        return {k: v for k, v in dataclassasdict(self).items()}

    def __str__(self):
        return " ".join(self.argv)

    def __hash__(self):
        return self.id

    @property
    def id(self):
        dict_str = (
            str({k: getattr(self, k) for k in self.fields})
            .encode("utf-8")
            .decode("utf-8")
        )

        return str(uuid.uuid5(uuid.NAMESPACE_DNS, dict_str))[:8]

    @property
    def fields(self):
        return [f.name for f in dataclasses.fields(Run) if not f.name.startswith("_")]
