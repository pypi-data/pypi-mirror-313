from typing import Iterator, Iterable
import itertools
from functools import reduce
from operator import ior, iand
import polars as pl

from .types import Arg, ArgsMatrix, ArgsDict


def iter_dict(inputs: ArgsMatrix) -> Iterator[ArgsDict]:
    consts = {k: v for k, v in inputs.items() if not isinstance(v, list)}
    inputs = {k: v for k, v in inputs.items() if isinstance(v, list)}

    for values in itertools.product(*inputs.values()):
        yield {**consts, **dict(zip(inputs.keys(), values))}


def ensure_df_columns(
    df: pl.DataFrame, exist_cols: Iterable[str], update: bool = False
) -> pl.DataFrame:
    exist_cols = set(exist_cols)
    cols = set(df.columns)

    missing_cols = exist_cols - cols
    if missing_cols:
        if update:
            df = df.with_columns(**{k: pl.lit(None) for k in missing_cols})
        else:
            msg = ", ".join([f'"{c}"' for c in missing_cols])
            raise ValueError(f"{len(missing_cols)} column(s) missing: {msg}.")

    return df


def ensure_df_compat(*dfs: pl.DataFrame, update: bool = False):
    schemas = tuple(dict(df.schema) for df in dfs)
    cols = set([k for s in schemas for k in s.keys()])

    merged_schema = {}
    for c in cols:
        dtypes = set(
            filter(
                lambda dtype: dtype != pl.datatypes.classes.Null,
                set(s.get(c, pl.datatypes.classes.Null) for s in schemas),
            )
        )

        if len(dtypes) > 1:
            raise ValueError(f'Incompatible dtypes for column "{c}": {dtypes}')

        merged_schema[c] = list(dtypes)[0]

    if update:
        return (
            ensure_df_columns(df, merged_schema.keys(), update=update).cast(
                merged_schema
            )
            for df in dfs
        )

    return dfs


def prepare_df_match_expr(df: pl.DataFrame, match_dict: ArgsMatrix):
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
