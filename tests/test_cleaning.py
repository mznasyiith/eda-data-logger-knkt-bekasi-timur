import pandas as pd
import pytest

from eda_knkt.cleaning import (
    missing_value_summary,
    normalize_column_names,
    remove_duplicate_rows,
    replace_placeholders,
)


def test_normalize_column_names_returns_copy():
    source = pd.DataFrame({"Event Time": [1], "Speed (km/h)": [2]})
    result = normalize_column_names(source)
    assert list(result.columns) == ["event_time", "speed_km_h"]
    assert list(source.columns) == ["Event Time", "Speed (km/h)"]


def test_normalize_column_names_rejects_collisions():
    source = pd.DataFrame([[1, 2]], columns=["Event-Time", "Event Time"])
    with pytest.raises(ValueError, match="duplicate"):
        normalize_column_names(source)


def test_replace_placeholders_does_not_replace_with_zero_or_mutate_source():
    source = pd.DataFrame({"value": ["---", "0", "12"]})
    result = replace_placeholders(source)
    assert pd.isna(result.loc[0, "value"])
    assert result.loc[1, "value"] == "0"
    assert source.loc[0, "value"] == "---"


def test_missing_value_summary():
    source = pd.DataFrame({"a": [1, None], "b": [1, 2]})
    result = missing_value_summary(source)
    assert result.loc["a", "missing_count"] == 1
    assert result.loc["a", "missing_percent"] == 50.0


def test_remove_duplicate_rows_returns_copy():
    source = pd.DataFrame({"event": [1, 1, 2]})
    result = remove_duplicate_rows(source)
    assert len(result) == 2
    assert len(source) == 3
