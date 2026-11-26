"""Explicit, non-destructive DataFrame transformation helpers.

These functions do not assume the meaning or units of KNKT Data Logger fields.
Callers must select columns and conversion rules based on the verified data
dictionary. Every transformation returns a new DataFrame.
"""
from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


def _validate_columns(df: pd.DataFrame, columns: Sequence[str]) -> None:
    """Raise a clear error when one or more requested columns are absent."""
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise KeyError(f"Column(s) not found: {missing}")


def convert_numeric_columns(
    df: pd.DataFrame,
    columns: Sequence[str],
    *,
    errors: str = "raise",
) -> pd.DataFrame:
    """Convert selected columns to numeric values on a copy.

    Args:
        df: Source DataFrame.
        columns: Explicit column names to convert.
        errors: 'raise' to stop on invalid values, or 'coerce' to mark them
            as missing. Coercion must be an intentional analytical decision.

    Returns:
        A new DataFrame with the selected columns converted.
    """
    if errors not in {"raise", "coerce"}:
        raise ValueError("errors must be either 'raise' or 'coerce'.")
    selected = list(columns)
    _validate_columns(df, selected)

    result = df.copy()
    for column in selected:
        result[column] = pd.to_numeric(result[column], errors=errors)
    return result


def convert_datetime_columns(
    df: pd.DataFrame,
    columns: Sequence[str],
    *,
    format: str | None = None,
    errors: str = "raise",
) -> pd.DataFrame:
    """Parse explicitly selected columns as datetimes on a copy.

    No timezone, date order, or event-time interpretation is inferred.
    Supply an explicit format when the source representation is known.
    """
    if errors not in {"raise", "coerce"}:
        raise ValueError("errors must be either 'raise' or 'coerce'.")
    selected = list(columns)
    _validate_columns(df, selected)

    result = df.copy()
    for column in selected:
        result[column] = pd.to_datetime(
            result[column],
            format=format,
            errors=errors,
        )
    return result


def sort_dataframe(
    df: pd.DataFrame,
    by: str | Sequence[str],
    *,
    ascending: bool | Sequence[bool] = True,
) -> pd.DataFrame:
    """Return a sorted copy without changing the source DataFrame."""
    selected = [by] if isinstance(by, str) else list(by)
    if not selected:
        raise ValueError("'by' must contain at least one column.")
    _validate_columns(df, selected)
    return df.sort_values(by=selected, ascending=ascending).copy()


def select_columns(
    df: pd.DataFrame,
    columns: Sequence[str],
) -> pd.DataFrame:
    """Return a copy containing only the explicitly requested columns."""
    selected = list(columns)
    if not selected:
        raise ValueError("'columns' must contain at least one column.")
    _validate_columns(df, selected)
    return df.loc[:, selected].copy()



def add_distance_to_stop_feature(
    df: pd.DataFrame,
    *,
    km_column: str = "km",
    meter_column: str = "m",
    output_column: str = "distance_to_stop_m",
) -> pd.DataFrame:
    """Add remaining distance to final stop in metres from source km/metre parts.

    The source columns are preserved. This transformation is valid only for the
    KNKT table semantics documented in docs/02_data_understanding/
    source_validation_distance.md; the result is not absolute track chainage.
    """
    _validate_columns(df, [km_column, meter_column])
    result = df.copy()
    km = pd.to_numeric(result[km_column], errors="raise")
    metres = pd.to_numeric(result[meter_column], errors="raise")
    if (km.dropna() < 0).any() or (metres.dropna() < 0).any():
        raise ValueError("Distance components must be non-negative.")
    if (metres.dropna() >= 1000).any():
        raise ValueError("Meter component must be below 1000.")
    result[output_column] = km * 1000 + metres
    return result
