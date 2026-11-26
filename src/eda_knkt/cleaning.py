"""Explicit, non-destructive data-cleaning helpers.

These helpers always return a new DataFrame and never infer domain meaning.
In particular, placeholder values are converted to missing values, not zero.
"""
from __future__ import annotations

import re
from collections.abc import Iterable

import pandas as pd


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with column labels normalized to lowercase snake_case.

    Raises:
        ValueError: If normalization would create duplicate column names.
    """
    result = df.copy()
    normalized = [
        re.sub(r"_+", "_", re.sub(r"[^0-9a-zA-Z]+", "_", str(column))).strip("_").lower()
        for column in result.columns
    ]
    if len(normalized) != len(set(normalized)):
        raise ValueError("Column normalization would create duplicate names.")
    result.columns = normalized
    return result


def replace_placeholders(
    df: pd.DataFrame,
    placeholders: Iterable[str] = ("---",),
) -> pd.DataFrame:
    """Replace explicitly supplied placeholder strings with pandas missing values."""
    result = df.copy()
    values = list(placeholders)
    if values:
        result = result.replace(values, pd.NA)
    return result


def missing_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return per-column missing counts and percentages without changing the input."""
    counts = df.isna().sum()
    total = len(df)
    percentages = (counts / total * 100) if total else counts.astype(float)
    return pd.DataFrame(
        {
            "missing_count": counts.astype("int64"),
            "missing_percent": percentages.astype(float),
        }
    )


def remove_duplicate_rows(
    df: pd.DataFrame,
    subset: list[str] | None = None,
) -> pd.DataFrame:
    """Return a copy with exact duplicate rows removed.

    This operation is explicit and does not decide whether repeated events are
    erroneous; callers must establish the domain rule before using it.
    """
    return df.drop_duplicates(subset=subset).copy()
