"""Basic dataset validation helpers."""
import pandas as pd


def inspect_dataframe(df: pd.DataFrame) -> dict:
    """Return basic dimensions, dtypes, and missing-value counts."""
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "dtypes": {str(k): str(v) for k, v in df.dtypes.items()},
        "missing": {str(k): int(v) for k, v in df.isna().sum().items()},
    }
