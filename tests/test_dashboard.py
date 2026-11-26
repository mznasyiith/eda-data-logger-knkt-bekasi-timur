from pathlib import Path

import pytest

from eda_knkt.dashboard import (
    DASHBOARD_NUMERIC_COLUMNS,
    load_dashboard_data,
    prepare_timeseries_plot_data,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "data_logger_knkt_tabel_6_10.csv"


def test_dashboard_uses_combined_distance_and_excludes_source_components():
    df = load_dashboard_data(DATA)
    assert "distance_to_stop_m" in df.columns
    assert df.loc[df["Time"] == "20.51.18", "distance_to_stop_m"].iloc[0] == 1341
    assert df.loc[df["Time"] == "20.52.12", "distance_to_stop_m"].iloc[0] == 26
    assert "km" not in DASHBOARD_NUMERIC_COLUMNS
    assert "m" not in DASHBOARD_NUMERIC_COLUMNS
    assert "Acceleration (m/sec²)" in DASHBOARD_NUMERIC_COLUMNS


def test_dashboard_preserves_the_selected_table_gap_and_breaks_plot_lines():
    df = load_dashboard_data(DATA)
    plot_data = prepare_timeseries_plot_data(
        df, ["Speed (km/h)", "distance_to_stop_m"]
    )
    separators = plot_data[plot_data["Nilai"].isna()]
    assert len(separators) == 2
    assert set(separators["Variabel"]) == {
        "Speed (km/h)",
        "distance_to_stop_m",
    }
    assert separators["Timestamp"].dt.strftime("%H:%M:%S").eq("20:51:33").all()


def test_dashboard_rejects_source_distance_components_as_plot_variables():
    df = load_dashboard_data(DATA)
    with pytest.raises(ValueError, match="Unsupported dashboard variable"):
        prepare_timeseries_plot_data(df, ["km"])


def test_dashboard_breaks_lines_after_filtered_timestamp_gaps():
    df = load_dashboard_data(DATA)
    filtered = df[df["Time"].isin(["20.51.27", "20.51.34"])]
    plot_data = prepare_timeseries_plot_data(filtered, ["Speed (km/h)"])
    assert plot_data["Nilai"].isna().sum() == 1
