from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DATASET = REPO_ROOT / "data" / "processed" / "data_logger_knkt_tabel_6_10.csv"

EXPECTED_COLUMNS = [
    "Date",
    "Time",
    "km",
    "m",
    "Speed (km/h)",
    "Acceleration (m/sec²)",
    "Load (amps)",
    "EAB BP (psi)",
    "EAB BC (psi)",
    "DB Excit",
    "Throttle",
    "PCS Open",
    "Dir Call",
    "DB Set",
    "DB Star",
    "IBS",
]


def test_merged_dataset_has_expected_shape_and_schema():
    df = pd.read_csv(DATASET)
    assert df.shape == (58, 16)
    assert df.columns.tolist() == EXPECTED_COLUMNS


def test_merged_dataset_preserves_source_missing_markers():
    df = pd.read_csv(DATASET)
    assert df["Acceleration (m/sec²)"].astype(str).eq("---").sum() == 7
    for column in ["DB Excit", "Dir Call", "DB Set", "DB Star"]:
        assert df[column].isna().sum() == 26


def test_merged_dataset_has_no_duplicate_rows():
    df = pd.read_csv(DATASET)
    assert df.duplicated().sum() == 0


def test_merged_dataset_retains_known_time_gap_without_interpolation():
    df = pd.read_csv(DATASET)
    timestamps = pd.to_datetime(
        df["Date"] + " " + df["Time"].str.replace(".", ":", regex=False),
        format="%d/%m/%Y %H:%M:%S",
    )
    gaps = timestamps.diff().dt.total_seconds()
    assert gaps.max() == 7
    assert (timestamps == pd.Timestamp("2026-04-27 20:51:28")).sum() == 0
    assert (timestamps == pd.Timestamp("2026-04-27 20:51:33")).sum() == 0
