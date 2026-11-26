import pandas as pd
import pytest

from eda_knkt.transformation import (
    convert_datetime_columns,
    convert_numeric_columns,
    select_columns,
    sort_dataframe,
)


def test_convert_numeric_columns_converts_selected_column_without_mutation():
    source = pd.DataFrame({"speed": ["10", "12.5"], "label": ["A", "B"]})
    result = convert_numeric_columns(source, ["speed"])
    assert str(result["speed"].dtype).startswith(("int", "float"))
    assert source["speed"].tolist() == ["10", "12.5"]
    assert result["label"].tolist() == ["A", "B"]


def test_convert_numeric_columns_can_explicitly_coerce_invalid_values():
    source = pd.DataFrame({"reading": ["10", "not-recorded"]})
    result = convert_numeric_columns(source, ["reading"], errors="coerce")
    assert result.loc[0, "reading"] == 10
    assert pd.isna(result.loc[1, "reading"])
    assert source.loc[1, "reading"] == "not-recorded"


def test_convert_numeric_columns_raises_on_invalid_value_by_default():
    source = pd.DataFrame({"reading": ["10", "---"]})
    with pytest.raises((ValueError, TypeError)):
        convert_numeric_columns(source, ["reading"])


def test_convert_datetime_columns_uses_explicit_format_and_preserves_source():
    source = pd.DataFrame({"recorded_at": ["27/04/2026 10:15"]})
    result = convert_datetime_columns(
        source, ["recorded_at"], format="%d/%m/%Y %H:%M"
    )
    assert pd.api.types.is_datetime64_any_dtype(result["recorded_at"])
    assert source.loc[0, "recorded_at"] == "27/04/2026 10:15"


def test_sort_dataframe_returns_sorted_copy():
    source = pd.DataFrame({"sequence": [3, 1, 2]})
    result = sort_dataframe(source, "sequence")
    assert result["sequence"].tolist() == [1, 2, 3]
    assert source["sequence"].tolist() == [3, 1, 2]


def test_select_columns_returns_only_requested_columns():
    source = pd.DataFrame({"time": [1], "speed": [2], "status": [3]})
    result = select_columns(source, ["time", "speed"])
    assert list(result.columns) == ["time", "speed"]
    assert list(source.columns) == ["time", "speed", "status"]


def test_transformations_reject_unknown_columns():
    source = pd.DataFrame({"time": [1]})
    with pytest.raises(KeyError, match="not found"):
        convert_numeric_columns(source, ["speed"])


def test_transformations_reject_invalid_error_mode():
    source = pd.DataFrame({"speed": ["10"]})
    with pytest.raises(ValueError, match="errors"):
        convert_numeric_columns(source, ["speed"], errors="ignore")
