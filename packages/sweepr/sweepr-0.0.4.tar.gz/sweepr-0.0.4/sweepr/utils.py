from typing import Iterator
import itertools

from .types import ArgsMatrix, ArgsDict


def iter_dict(inputs: ArgsMatrix) -> Iterator[ArgsDict]:
    consts = {k: v for k, v in inputs.items() if not isinstance(v, list)}
    inputs = {k: v for k, v in inputs.items() if isinstance(v, list)}

    for values in itertools.product(*inputs.values()):
        yield {**consts, **dict(zip(inputs.keys(), values))}
