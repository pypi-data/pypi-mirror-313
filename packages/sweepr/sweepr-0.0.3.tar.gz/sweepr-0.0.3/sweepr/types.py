from typing import Dict, List, Union, Tuple, TypeAlias


Arg: TypeAlias = Union[str, int, float]

ArgsDict: TypeAlias = Dict[str, Arg]

EnvDict: TypeAlias = Dict[str, str]

ArgsMatrix: TypeAlias = Dict[str, Union[Arg, List[Arg]]]

IncludeTuple: TypeAlias = Tuple[ArgsMatrix, ArgsDict]

Includes: TypeAlias = Union[IncludeTuple, List[IncludeTuple]]

Excludes: TypeAlias = Union[ArgsMatrix, List[ArgsMatrix]]
