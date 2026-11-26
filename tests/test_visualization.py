import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from eda_knkt.config import OUTPUTS_DIR
from eda_knkt.visualization import (
    plot_categorical_counts,
    plot_correlation_heatmap,
    plot_numeric_distribution,
    plot_scatter,
)


def test_plot_numeric_distribution_returns_axes():
    df = pd.DataFrame({"speed": [10, 20, 30, None]})
    ax = plot_numeric_distribution(df, "speed", bins=3)
    assert ax.get_xlabel() == "speed"
    plt.close(ax.figure)


def test_plot_categorical_counts_returns_axes():
    df = pd.DataFrame({"status": ["A", "B", "A"]})
    ax = plot_categorical_counts(df, "status")
    assert ax.get_ylabel() == "Frequency"
    plt.close(ax.figure)


def test_plot_scatter_drops_missing_pairs():
    df = pd.DataFrame({"x": [1, 2, None], "y": [2, 4, 6]})
    ax = plot_scatter(df, "x", "y")
    assert len(ax.collections[0].get_offsets()) == 2
    plt.close(ax.figure)


def test_plot_heatmap_and_validate_empty_matrix():
    matrix = pd.DataFrame([[1.0, 0.5], [0.5, 1.0]], columns=["x", "y"], index=["x", "y"])
    ax = plot_correlation_heatmap(matrix)
    assert ax.get_title() == "Correlation matrix"
    plt.close(ax.figure)
    with pytest.raises(ValueError):
        plot_correlation_heatmap(pd.DataFrame())


def test_plot_rejects_invalid_column_type_or_name():
    df = pd.DataFrame({"category": ["a", "b"]})
    with pytest.raises(TypeError):
        plot_numeric_distribution(df, "category")
    with pytest.raises(KeyError):
        plot_scatter(df, "missing", "category")


def test_interactive_html_uses_stable_plotly_div_ids():
    expected = {
        "bab_vii/deret_waktu_interaktif.html": "eda-deret-waktu-interaktif",
        "bab_vii/tekanan_bp_bc_interaktif.html": "eda-tekanan-bp-bc-interaktif",
        "bab_vii/heatmap_spearman_interaktif.html": "eda-heatmap-spearman-interaktif",
    }
    for relative_path, div_id in expected.items():
        html = (OUTPUTS_DIR / relative_path).read_text(encoding="utf-8")
        assert f'id="{div_id}"' in html
