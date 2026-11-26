from pathlib import Path

import pandas as pd
import pytest

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



def test_all_58_unique_source_timestamps_are_preserved_in_order():
    df = load_data()
    expected_times = [
        "20.51.18", "20.51.19", "20.51.20", "20.51.21", "20.51.22",
        "20.51.23", "20.51.24", "20.51.25", "20.51.26", "20.51.27",
        "20.51.34", "20.51.35", "20.51.36", "20.51.37", "20.51.38",
        "20.51.39", "20.51.40", "20.51.41", "20.51.42", "20.51.43",
        "20.51.44", "20.51.45", "20.51.46", "20.51.47", "20.51.48",
        "20.51.49", "20.51.50", "20.51.51", "20.51.52", "20.51.53",
        "20.51.54", "20.51.55", "20.51.56", "20.51.57", "20.51.58",
        "20.51.59", "20.52.00", "20.52.01", "20.52.02", "20.52.03",
        "20.52.04", "20.52.05", "20.52.06", "20.52.07", "20.52.08",
        "20.52.09", "20.52.10", "20.52.11", "20.52.12", "20.52.13",
        "20.52.14", "20.52.15", "20.52.16", "20.52.17", "20.52.18",
        "20.52.19", "20.52.20", "20.52.21",
    ]
    assert len(df) == 58
    assert df["Time"].tolist() == expected_times
    assert df["Time"].is_unique
    assert "20.51.28" not in expected_times
    assert "20.51.33" not in expected_times


def test_zero_distance_precedes_zero_speed_by_one_record():
    df = load_data().set_index("Time")
    assert df.loc["20.52.18", ["km", "m", "Speed (km/h)"]].tolist() == [
        "0", "0", "3"
    ]
    assert df.loc["20.52.19", ["km", "m", "Speed (km/h)"]].tolist() == [
        "0", "0", "0"
    ]


def test_distribution_moments_match_published_output():
    df = load_data()
    numeric = [
        "km", "m", "Speed (km/h)", "Acceleration (m/sec²)",
        "Load (amps)", "EAB BP (psi)", "EAB BC (psi)",
    ]
    for column in numeric:
        df[column] = pd.to_numeric(
            df[column].replace("", pd.NA).replace("---", pd.NA)
        )
    df["distance_to_stop_m"] = df["km"] * 1000 + df["m"]
    columns = [
        "distance_to_stop_m", "Speed (km/h)", "Acceleration (m/sec²)",
        "Load (amps)", "EAB BP (psi)", "EAB BC (psi)",
    ]
    expected = {
        "distance_to_stop_m": (0.6582033736854108, -0.7673799562465446),
        "Speed (km/h)": (-0.9580197770958286, -0.08418926925952261),
        "Acceleration (m/sec²)": (0.2895281268899046, -0.44347894765805285),
        "Load (amps)": (-0.216174252475948, -1.9370293635641485),
        "EAB BP (psi)": (-0.12995015466864968, -1.8299244312426293),
        "EAB BC (psi)": (0.5025565657528722, -1.6594257479596688),
    }
    from eda_knkt.statistics import distribution_shape

    actual = distribution_shape(df, columns)
    for column, (skewness, kurtosis) in expected.items():
        assert actual.loc[column, "skewness"] == pytest.approx(
            skewness, abs=1e-10
        )
        assert actual.loc[column, "kurtosis"] == pytest.approx(
            kurtosis, abs=1e-10
        )


def test_spearman_correlations_match_published_analysis():
    df = load_data()
    numeric = [
        "km", "m", "Speed (km/h)", "Acceleration (m/sec²)",
        "Load (amps)", "EAB BP (psi)", "EAB BC (psi)",
    ]
    for column in numeric:
        df[column] = pd.to_numeric(
            df[column].replace("", pd.NA).replace("---", pd.NA)
        )
    df["distance_to_stop_m"] = df["km"] * 1000 + df["m"]
    columns = [
        "distance_to_stop_m", "Speed (km/h)", "Acceleration (m/sec²)",
        "Load (amps)", "EAB BP (psi)", "EAB BC (psi)",
    ]
    from eda_knkt.statistics import correlation_matrix

    actual = correlation_matrix(df, columns, method="spearman")
    expected = {
        ("distance_to_stop_m", "Speed (km/h)"): 0.998044454992,
        ("distance_to_stop_m", "Acceleration (m/sec²)"): 0.874479858902,
        ("distance_to_stop_m", "Load (amps)"): 0.899597031099,
        ("distance_to_stop_m", "EAB BP (psi)"): 0.959702738438,
        ("distance_to_stop_m", "EAB BC (psi)"): -0.762476324185,
        ("Speed (km/h)", "Acceleration (m/sec²)"): 0.872783051546,
        ("Speed (km/h)", "Load (amps)"): 0.900692418576,
        ("Speed (km/h)", "EAB BP (psi)"): 0.958158316416,
        ("Speed (km/h)", "EAB BC (psi)"): -0.763650695210,
        ("Acceleration (m/sec²)", "Load (amps)"): 0.893520079225,
        ("Acceleration (m/sec²)", "EAB BP (psi)"): 0.881916511610,
        ("Acceleration (m/sec²)", "EAB BC (psi)"): -0.765023891937,
        ("Load (amps)", "EAB BP (psi)"): 0.928986464931,
        ("Load (amps)", "EAB BC (psi)"): -0.880768528741,
        ("EAB BP (psi)", "EAB BC (psi)"): -0.798406546896,
    }
    for (left, right), value in expected.items():
        assert actual.loc[left, right] == pytest.approx(value, abs=1e-10)
        assert actual.loc[right, left] == pytest.approx(value, abs=1e-10)


def test_report_labels_timestamp_table_as_key_timestamps_and_notes_zero_distance():
    report = REPORT.read_text(encoding="utf-8")
    assert "Audit kronologi parameter pada timestamp kunci" in report
    assert "bukan daftar lengkap seluruh 58 rekaman" in report
    assert "20:52:18" in report and "kecepatan masih 3 km/jam" in report
    assert "Pengereman hingga Tabrakan" in report


def test_all_58_by_16_transcribed_cells_match_golden_snapshot():
    """Lock every source cell, including empty strings and '---' placeholders.

    The fixture is a regression baseline for the checked-in transcription;
    its provenance still requires independent comparison with KNKT Tables 6–10.
    """
    expected_path = (
        ROOT / "tests" / "fixtures" / "data_logger_knkt_tabel_6_10_expected.csv"
    )
    actual = pd.read_csv(DATA, dtype=str, keep_default_na=False)
    expected = pd.read_csv(expected_path, dtype=str, keep_default_na=False)

    assert actual.shape == (58, 16)
    assert expected.shape == (58, 16)
    assert actual.columns.tolist() == expected.columns.tolist()
    # DataFrame.equals compares every cell and preserves distinctions among
    # empty strings, literal placeholders, numeric text, and categorical text.
    assert actual.equals(expected)



def test_source_pdf_audit_corrects_load_amps_at_205136():
    """The PDF's Table 7 row 20:51:36 reports 160 A, not 168 A."""
    df = load_data().set_index("Time")
    assert df.loc["20.51.36", "Load (amps)"] == "160"
