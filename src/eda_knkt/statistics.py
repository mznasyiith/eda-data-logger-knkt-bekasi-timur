"""Descriptive statistics helpers for exploratory data analysis.

The functions summarize observed values only. They do not infer domain meaning,
impute missing values, or treat missing markers as numeric values.
"""
from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


def _selected_columns(
    df: pd.DataFrame,
    columns: Sequence[str] | None,
) -> list[str]:
    selected = list(columns) if columns is not None else list(df.columns)
    if not selected:
        raise ValueError("At least one column must be selected.")
    missing = [column for column in selected if column not in df.columns]
    if missing:
        raise KeyError(f"Column(s) not found: {missing}")
    return selected


def numeric_summary(
    df: pd.DataFrame,
    columns: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Return count, mean, std, min, quartiles, and max for numeric columns."""
    selected = _selected_columns(df, columns)
    non_numeric = [
        column for column in selected
        if not pd.api.types.is_numeric_dtype(df[column])
    ]
    if non_numeric:
        raise TypeError(f"Non-numeric column(s) selected: {non_numeric}")
    return df.loc[:, selected].describe().T.copy()


def categorical_summary(
    df: pd.DataFrame,
    columns: Sequence[str],
) -> pd.DataFrame:
    """Summarize non-null count, unique count, mode, and mode frequency."""
    selected = _selected_columns(df, columns)
    rows: list[dict[str, object]] = []
    for column in selected:
        values = df[column].dropna()
        counts = values.value_counts()
        rows.append(
            {
                "column": column,
                "count": int(values.size),
                "unique": int(values.nunique()),
                "top": counts.index[0] if not counts.empty else pd.NA,
                "freq": int(counts.iloc[0]) if not counts.empty else 0,
            }
        )
    return pd.DataFrame(rows).set_index("column")


def distribution_shape(
    df: pd.DataFrame,
    columns: Sequence[str],
) -> pd.DataFrame:
    """Return skewness and excess kurtosis for explicitly selected numeric columns."""
    selected = _selected_columns(df, columns)
    non_numeric = [
        column for column in selected
        if not pd.api.types.is_numeric_dtype(df[column])
    ]
    if non_numeric:
        raise TypeError(f"Non-numeric column(s) selected: {non_numeric}")
    result = pd.DataFrame(
        {
            "skewness": df.loc[:, selected].skew(),
            "kurtosis": df.loc[:, selected].kurt(),
        }
    )
    return result


def correlation_matrix(
    df: pd.DataFrame,
    columns: Sequence[str],
    *,
    method: str = "pearson",
) -> pd.DataFrame:
    """Return pairwise correlations for selected numeric columns."""
    if method not in {"pearson", "spearman", "kendall"}:
        raise ValueError("method must be 'pearson', 'spearman', or 'kendall'.")
    selected = _selected_columns(df, columns)
    non_numeric = [
        column for column in selected
        if not pd.api.types.is_numeric_dtype(df[column])
    ]
    if non_numeric:
        raise TypeError(f"Non-numeric column(s) selected: {non_numeric}")
    return df.loc[:, selected].corr(method=method)
