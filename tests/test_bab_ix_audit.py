from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "data_logger_knkt_tabel_6_10.csv"
IQR = ROOT / "outputs" / "bab_viii" / "ringkasan_iqr.csv"
REPORT = ROOT / "reports" / "Laporan_EDA_KNKT_Bekasi_Timur.md"


def load_data():
    return pd.read_csv(DATA, dtype=str, keep_default_na=False)


def test_chapter_ix_timestamp_values_match_source_transcription():
    df = load_data().set_index("Time")
    expected = {
        "20.51.18": {"Speed (km/h)": "108", "EAB BP (psi)": "71", "EAB BC (psi)": "0"},
        "20.51.27": {"Speed (km/h)": "107", "EAB BP (psi)": "65"},
        "20.51.43": {"Speed (km/h)": "95", "EAB BP (psi)": "49"},
        "20.51.55": {"Speed (km/h)": "79", "EAB BP (psi)": "49"},
        "20.51.56": {"Speed (km/h)": "78", "EAB BP (psi)": "43", "PCS Open": "Open"},
        "20.52.00": {"Speed (km/h)": "70", "EAB BP (psi)": "0", "EAB BC (psi)": "70"},
        "20.52.03": {"Speed (km/h)": "65", "IBS": "Appl"},
        "20.52.12": {"Speed (km/h)": "40", "EAB BP (psi)": "0", "EAB BC (psi)": "73", "Throttle": "Off"},
        "20.52.19": {"Speed (km/h)": "0", "EAB BC (psi)": "55"},
    }
    for timestamp, fields in expected.items():
        for column, value in fields.items():
            assert df.loc[timestamp, column] == value


def test_chapter_ix_frequency_counts_match_dataset():
    df = load_data()
    assert df["Throttle"].value_counts().to_dict() == {
        "T5": 17, "Idle": 13, "T7": 11, "Off": 10, "T4": 4, "T6": 2, "T1": 1
    }
    assert df["PCS Open"].value_counts().to_dict() == {"Closed": 32, "Open": 26}
    assert df["IBS"].value_counts().to_dict() == {"Rel": 39, "Appl": 19}
    for column, category in {
        "DB Excit": "Off", "Dir Call": "For", "DB Set": "No", "DB Star": "No"
    }.items():
        assert (df[column] == category).sum() == 32
        assert (df[column] == "").sum() == 26


def test_chapter_ix_descriptive_statistics_match_dataset():
    df = load_data()
    for column in [
        "km", "m", "Speed (km/h)", "Acceleration (m/sec²)",
        "Load (amps)", "EAB BP (psi)", "EAB BC (psi)"
    ]:
        df[column] = pd.to_numeric(df[column].replace("", pd.NA).replace("---", pd.NA))
    df["distance_to_stop_m"] = df["km"] * 1000 + df["m"]
    assert df["Acceleration (m/sec²)"].notna().sum() == 51
    assert df["distance_to_stop_m"].iloc[0] == 1341
    assert round(df["distance_to_stop_m"].mean(), 3) == 472.897
    assert round(df["distance_to_stop_m"].median(), 3) == 378.5
    assert round(df["distance_to_stop_m"].std(), 3) == 421.531
    assert df.loc[df["Time"] == "20.52.12", "distance_to_stop_m"].iloc[0] == 26
    assert df.loc[df["Time"] == "20.52.19", "distance_to_stop_m"].iloc[0] == 0
    assert round(df["Speed (km/h)"].mean(), 3) == 73.638
    assert round(df["EAB BC (psi)"].max(), 3) == 73


def test_chapter_ix_iqr_summary_matches_recalculation():
    df = load_data()
    variables = [
        "distance_to_stop_m", "Speed (km/h)", "Acceleration (m/sec²)",
        "Load (amps)", "EAB BP (psi)", "EAB BC (psi)"
    ]
    for column in ["km", "m", "Speed (km/h)", "Acceleration (m/sec²)", "Load (amps)", "EAB BP (psi)", "EAB BC (psi)"]:
        df[column] = pd.to_numeric(df[column].replace("", pd.NA).replace("---", pd.NA))
    df["distance_to_stop_m"] = df["km"] * 1000 + df["m"]
    expected = pd.read_csv(IQR).set_index("variable")
    assert set(expected.index) == set(variables)
    assert "km" not in expected.index and "m" not in expected.index
    for column in variables:
        values = df[column].dropna()
        q1, q3 = values.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        count = int(((values < lower) | (values > upper)).sum())
        row = expected.loc[column]
        assert int(row["n_valid"]) == len(values)
        assert int(row["iqr_outlier_count"]) == count
        assert round(row["lower_fence"], 3) == round(lower, 3)
        assert round(row["upper_fence"], 3) == round(upper, 3)


def test_chapter_ix_reports_master_time_adjustment_and_separate_collision_stop():
    report = REPORT.read_text(encoding="utf-8")
    assert "20:52:10 disesuaikan menjadi 20:52:12" in report
    assert "koreksi +2 detik" in report
    assert "tabrakan dan berhenti merupakan dua peristiwa berbeda" in report.lower()
    assert "20:52:12" in report and "40" in report
    assert "20:52:19" in report and "55" in report
    assert "20:51:28–20:51:33" in report
    assert "distance_to_stop_m" in report
