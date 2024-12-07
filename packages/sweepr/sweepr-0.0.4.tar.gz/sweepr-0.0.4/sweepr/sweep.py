from typing import Iterator, Optional, List, Union, TextIO
import sys
from enum import Enum
from contextlib import nullcontext
from tqdm.auto import tqdm
from pathlib import Path
import dataclasses
from dataclasses import dataclass, field
import uuid
import polars as pl
from functools import reduce
from operator import iand, ior

from .types import (
    Arg,
    ArgsDict,
    EnvDict,
    ArgsMatrix,
    Includes,
    Excludes,
)
from .utils import iter_dict
from .executors import BaseExecutor


@dataclass
class Run:
    program: List[str]
    args: Optional[ArgsDict] = field(default_factory=lambda: {})
    env: Optional[EnvDict] = field(default_factory=lambda: {})
    tags: List[str] = field(default_factory=lambda: [])

    class Env(str, Enum):
        HASH = "RUN_HASH"
        TAGS = "RUN_TAGS"

    @property
    def argv(self):
        return (
            [f"{self.Env.HASH.value}={self.hash}"]
            + ([f"{self.Env.TAGS.value}={','.join(self.tags)}"] if self.tags else [])
            + [f"{k}={v}" for k, v in self.env.items()]
            + self.program
            + [f"--{k}={v}" for k, v in self.args.items()]
        )

    def __str__(self):
        return " ".join(self.argv)

    def __hash__(self):
        return self.hash

    @property
    def hash(self):
        dict_str = (
            str({k: getattr(self, k) for k in self.fields})
            .encode("utf-8")
            .decode("utf-8")
        )

        return str(uuid.uuid5(uuid.NAMESPACE_DNS, dict_str))[:8]

    @property
    def fields(self):
        return [f.name for f in dataclasses.fields(Run) if not f.name.startswith("_")]


class Sweep:
    def __init__(self):
        self._executor: BaseExecutor = None

        self._args: pl.DataFrame = None

    def __len__(self):
        return len(self._args)

    @property
    def tags(self):
        assert self._args is not None, "Did you set .args(...) first?"

        return list(
            filter(
                None,
                [
                    f"arg:{k}"
                    for k, v in next(
                        self._args.select(
                            [pl.col(c).n_unique() for c in self._args.columns]
                        ).iter_rows(named=True)
                    ).items()
                    if v > 1
                ],
            )
        )

    def __iter__(self) -> Iterator[Run]:
        assert self._args is not None, "Did you run .args(...)?"
        assert self._executor is not None, "Did you run .executor(...)?"

        run_tags = self.tags

        for row in self._args.iter_rows(named=True):
            run = Run(
                program=self._executor.exec,
                args={k: v for k, v in row.items() if v is not None},
                env=self._executor.env,
                tags=run_tags,
            )

            yield run

    def args(self, matrix: ArgsMatrix):
        all_args = iter_dict(matrix)

        new_df = pl.DataFrame(all_args)

        if self._args is None:
            self._args = new_df
        else:
            self._check_cols_exist(new_df.columns, add_missing=True)
            self._check_cols_exist(self._args.columns, add_missing=True, df=new_df)

            self._args = pl.concat([self._args, new_df], how="align", rechunk=True)

        self._args = self._args.unique()

        return self

    def include(self, includes: Includes):
        assert self._args is not None, "Did you set .args(...) first?"

        if not isinstance(includes, list):
            includes = [includes]

        for match_dict, include_dict in tqdm(includes, leave=False):
            self._check_cols_exist(match_dict.keys())

            self._check_cols_exist(include_dict.keys(), add_missing=True)

            self._args = self._args.with_columns(
                pl.when(self._prepare_match_conditions(match_dict))
                .then(pl.struct(**{k: pl.lit(v) for k, v in include_dict.items()}))
                .otherwise(pl.struct(*include_dict.keys()))
                .struct.unnest()
            )

        self._args = self._args.unique()

        return self

    def exclude(self, excludes: Excludes):
        assert self._args is not None, "Did you set .args(...) first?"

        if not isinstance(excludes, list):
            excludes = [excludes]

        for match_dict in tqdm(excludes, leave=False):
            self._check_cols_exist(match_dict.keys())

            self._args = self._args.filter(~self._prepare_match_conditions(match_dict))

        return self

    def executor(self, executor: BaseExecutor):
        self._executor = executor

        return self

    def write_bash(self, file: Union[str, Path, TextIO] = None, delay: int = 3):
        with (
            open(file, "w")
            if isinstance(file, (str, Path))
            else nullcontext(file or sys.stdout) as file
        ):
            print("#!/usr/bin/env -S bash -l", file=file, end="\n\n")
            print(file=file)

            for run in self:
                print(str(run), file=file)
                print(f"sleep $(( RANDOM % {delay} ))", file=file, end="\n\n")

        return self

    def _check_cols_exist(self, exist_cols, add_missing=False, df=None):
        if df is None:
            df = self._args

        exist_cols = set(exist_cols)
        cols = set(df.columns)

        missing_cols = exist_cols - cols
        if missing_cols:
            if add_missing:
                df = df.with_columns(**{k: pl.lit(None) for k in missing_cols})
            else:
                msg = ", ".join([f'"{c}"' for c in missing_cols])
                raise ValueError(f"{len(missing_cols)} column(s) missing: {msg}.")

    def _prepare_match_conditions(self, match_dict: ArgsMatrix):
        def _expr(k: str, v: Arg):
            if isinstance(v, str):
                ## NOTE: Regex syntax at https://docs.rs/regex/latest/regex/#syntax
                return pl.col(k).str.contains(v, literal=False)
            return pl.col(k) == v

        return reduce(
            ior,
            [
                reduce(iand, [_expr(k, v) for k, v in md.items()])
                for md in iter_dict(match_dict)
            ],
        )
