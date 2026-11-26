import pandas as pd
from eda_knkt.validation import inspect_dataframe


def test_inspect_dataframe_reports_dimensions():
    df = pd.DataFrame({"event": [1, 2], "time": ["10:00", "10:01"]})
    result = inspect_dataframe(df)
    assert result["rows"] == 2
    assert result["columns"] == 2
