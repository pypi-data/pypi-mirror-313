from typing import Iterator, Union, TextIO, List, Optional
import sys
from contextlib import nullcontext
from tqdm.auto import tqdm
import json
from pathlib import Path
import polars as pl

from .types import (
    EnvDict,
    ArgsMatrix,
    Includes,
    Excludes,
)
from .utils import (
    iter_dict,
    ensure_df_columns,
    ensure_df_compat,
    prepare_df_match_expr,
)
from .executors import BaseExecutor
from .providers import BaseProvider
from .run import Run


class Sweep:
    def __init__(self):
        self._executor: BaseExecutor = None

        self._args: pl.DataFrame = None

        self._provider: BaseProvider = None

    def __len__(self):
        return len(self._args)

    @property
    def tags(self) -> List[str]:
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

        for row in self._args.iter_rows(named=True):
            run = Run(
                program=self._executor.exec,
                args={k: v for k, v in row.items() if v is not None},
                env=self._executor.env,
            )

            if self._provider:
                run = self._provider(run, self)

            yield run

    def args(self, matrix: ArgsMatrix):
        all_args = iter_dict(matrix)

        new_df = pl.DataFrame(all_args)

        if self._args is None:
            self._args = new_df
        else:
            self._args, new_df = ensure_df_compat(self._args, new_df, update=True)

            self._args = pl.concat([self._args, new_df], how="align", rechunk=True)

        self._args = self._args.unique()

        return self

    def include(self, includes: Includes):
        assert self._args is not None, "Did you set .args(...) first?"

        if not isinstance(includes, list):
            includes = [includes]

        for match_dict, include_dict in tqdm(includes, leave=False):
            ensure_df_columns(self._args, match_dict.keys())
            self._args = ensure_df_columns(self._args, include_dict.keys(), update=True)

            self._args = self._args.with_columns(
                pl.when(prepare_df_match_expr(self._args, match_dict))
                .then(pl.struct(**{k: pl.lit(v) for k, v in include_dict.items()}))
                .otherwise(pl.struct(*include_dict.keys()))
                .struct.unnest()
            )

        self._args = self._args.unique()

        return self

    def exclude(self, excludes: Excludes):
        assert self._args is not None, "Did you set .args(...) first?"

        if isinstance(excludes, dict):
            excludes = [excludes]

        for match_dict in tqdm(excludes, leave=False):
            ensure_df_columns(self._args, match_dict.keys())

            self._args = self._args.filter(
                ~prepare_df_match_expr(self._args, match_dict)
            )

        return self

    def provider(self, provider: BaseProvider):
        if self._provider is not None:
            raise ValueError(".provider() can only be set once.")

        self._provider = provider

        self.exclude(self._provider.runs(self._args.columns))

        return self

    def executor(self, executor: BaseExecutor):
        self._executor = executor

        return self

    def env(self, env_dict: EnvDict):
        assert self._executor is not None, "Did you set .executor(...) first?"

        self._executor.env = {**self._executor.env, **env_dict}

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

    def write_json(
        self,
        file: Union[str, Path, TextIO] = None,
        indent: Optional[int] = None,
        jsonl: bool = False,
    ):
        with (
            open(file, "w")
            if isinstance(file, (str, Path))
            else nullcontext(file or sys.stdout) as file
        ):
            if jsonl:
                for run in self:
                    print(json.dumps(run.todict()), file=file)
            else:
                print(
                    json.dumps([run.todict() for run in self], indent=indent), file=file
                )
