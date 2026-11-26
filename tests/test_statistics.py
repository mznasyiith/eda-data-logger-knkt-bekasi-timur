import pandas as pd
import pytest

from eda_knkt.statistics import (
    categorical_summary,
    correlation_matrix,
    distribution_shape,
    numeric_summary,
)


def test_numeric_summary_returns_descriptive_statistics():
    df = pd.DataFrame({"speed": [10, 20, 30], "distance": [1.0, 2.0, 3.0]})
    result = numeric_summary(df)
    assert result.loc["speed", "mean"] == 20
    assert result.loc["speed", "min"] == 10
    assert result.loc["speed", "max"] == 30


def test_numeric_summary_rejects_non_numeric_columns():
    df = pd.DataFrame({"status": ["A", "B"]})
    with pytest.raises(TypeError):
        numeric_summary(df)


def test_categorical_summary_counts_observed_values():
    df = pd.DataFrame({"status": ["A", "B", "A", None]})
    result = categorical_summary(df, ["status"])
    assert result.loc["status", "count"] == 3
    assert result.loc["status", "unique"] == 2
    assert result.loc["status", "top"] == "A"
    assert result.loc["status", "freq"] == 2


def test_categorical_summary_handles_all_missing_column():
    df = pd.DataFrame({"status": [None, None]})
    result = categorical_summary(df, ["status"])
    assert result.loc["status", "count"] == 0
    assert result.loc["status", "top"] is pd.NA or pd.isna(result.loc["status", "top"])
    assert result.loc["status", "freq"] == 0


def test_distribution_shape_returns_skewness_and_kurtosis():
    df = pd.DataFrame({"x": [1, 2, 2, 3, 10]})
    result = distribution_shape(df, ["x"])
    assert list(result.columns) == ["skewness", "kurtosis"]
    assert result.loc["x", "skewness"] > 0


def test_correlation_matrix_supports_spearman():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
    result = correlation_matrix(df, ["x", "y"], method="spearman")
    assert result.loc["x", "y"] == pytest.approx(1.0)


def test_invalid_method_and_missing_column_raise():
    df = pd.DataFrame({"x": [1, 2]})
    with pytest.raises(ValueError):
        correlation_matrix(df, ["x"], method="invalid")
    with pytest.raises(KeyError):
        numeric_summary(df, ["unknown"])
