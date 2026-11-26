import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from eda_knkt.reporting import (
    export_dataframe_csv,
    save_figure,
    write_markdown_report,
)


def test_export_dataframe_csv_creates_parent_and_round_trips(tmp_path):
    df = pd.DataFrame({"speed": [10, 20]})
    destination = export_dataframe_csv(df, tmp_path / "nested" / "data.csv")
    loaded = pd.read_csv(destination)
    pd.testing.assert_frame_equal(loaded, df)


def test_export_dataframe_csv_index_is_opt_in(tmp_path):
    df = pd.DataFrame({"speed": [10, 20]})
    destination = export_dataframe_csv(df, tmp_path / "data.csv", index=True)
    loaded = pd.read_csv(destination)
    assert "Unnamed: 0" in loaded.columns


def test_save_figure_and_validate_dpi(tmp_path):
    figure, ax = plt.subplots()
    ax.plot([1, 2], [3, 4])
    destination = save_figure(figure, tmp_path / "figures" / "plot.png")
    assert destination.exists()
    assert destination.stat().st_size > 0
    plt.close(figure)
    with pytest.raises(ValueError):
        save_figure(plt.figure(), tmp_path / "bad.png", dpi=0)


def test_write_markdown_report_preserves_content(tmp_path):
    content = "# Findings\n\n- First observation\n"
    destination = write_markdown_report(content, tmp_path / "reports" / "findings.md")
    assert destination.read_text(encoding="utf-8") == content


def test_write_markdown_report_rejects_non_string(tmp_path):
    with pytest.raises(TypeError):
        write_markdown_report(123, tmp_path / "report.md")
