from typing import Dict, Iterable, Union, Tuple, TypeAlias


Arg: TypeAlias = Union[str, int, float]

ArgsDict: TypeAlias = Dict[str, Arg]

EnvDict: TypeAlias = Dict[str, str]

ArgsMatrix: TypeAlias = Dict[str, Union[Arg, Iterable[Arg]]]

IncludeTuple: TypeAlias = Tuple[ArgsMatrix, ArgsDict]

Includes: TypeAlias = Union[IncludeTuple, Iterable[IncludeTuple]]

Excludes: TypeAlias = Union[ArgsMatrix, Iterable[ArgsMatrix]]
