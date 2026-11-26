"""Data preparation helpers for the optional Streamlit dashboard.

The dashboard follows the same verified variable semantics as the EDA pipeline.
"""
from __future__ import annotations

from pathlib import Path
from typing import Sequence

import pandas as pd

from eda_knkt.transformation import add_distance_to_stop_feature

SOURCE_NUMERIC_COLUMNS = [
    "km",
    "m",
    "Speed (km/h)",
    "Acceleration (m/sec²)",
    "Load (amps)",
    "EAB BP (psi)",
    "EAB BC (psi)",
]

DASHBOARD_NUMERIC_COLUMNS = [
    "distance_to_stop_m",
    "Speed (km/h)",
    "Acceleration (m/sec²)",
    "Load (amps)",
    "EAB BP (psi)",
    "EAB BC (psi)",
]


def load_dashboard_data(path: str | Path) -> pd.DataFrame:
    """Load the selected Tables 6–10 dataset with explicit, non-destructive semantics."""
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    required = {"Date", "Time", *SOURCE_NUMERIC_COLUMNS}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Required dashboard columns are missing: {missing}")

    df["Timestamp"] = pd.to_datetime(
        df["Date"].astype(str) + " " + df["Time"].astype(str),
        format="%d/%m/%Y %H.%M.%S",
        errors="raise",
    )
    for column in SOURCE_NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(
            df[column].replace({"": pd.NA, "---": pd.NA}),
            errors="raise",
        )

    df = add_distance_to_stop_feature(df)
    for column in ["Throttle", "PCS Open", "IBS"]:
        if column in df.columns:
            df[column] = df[column].replace("", pd.NA)

    df = df.sort_values("Timestamp").reset_index(drop=True)
    df["Interval (s)"] = df["Timestamp"].diff().dt.total_seconds()
    return df


def prepare_timeseries_plot_data(
    frame: pd.DataFrame,
    columns: Sequence[str],
) -> pd.DataFrame:
    """Return long-form series with NaN separators across gaps over one second."""
    selected = list(columns)
    if not selected:
        raise ValueError("Select at least one numeric variable.")
    invalid = [column for column in selected if column not in DASHBOARD_NUMERIC_COLUMNS]
    if invalid:
        raise ValueError(f"Unsupported dashboard variable(s): {invalid}")

    required = {"Timestamp", *selected}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise KeyError(f"Column(s) not found: {missing}")

    ordered = frame.sort_values("Timestamp").reset_index(drop=True)
    rows: list[dict[str, object]] = []
    previous_timestamp = None
    for row in ordered.itertuples(index=False):
        values = row._asdict()
        timestamp = values["Timestamp"]
        if previous_timestamp is not None:
            interval = (timestamp - previous_timestamp).total_seconds()
            if interval > 1:
                separator_time = timestamp - pd.Timedelta(microseconds=1)
                for column in selected:
                    rows.append(
                        {
                            "Timestamp": separator_time,
                            "Variabel": column,
                            "Nilai": float("nan"),
                        }
                    )
        for column in selected:
            value = values[column]
            rows.append(
                {
                    "Timestamp": timestamp,
                    "Variabel": column,
                    "Nilai": value,
                }
            )
        previous_timestamp = timestamp

    return pd.DataFrame(rows, columns=["Timestamp", "Variabel", "Nilai"])
