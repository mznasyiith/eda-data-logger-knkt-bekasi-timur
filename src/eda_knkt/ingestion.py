"""Data loading helpers."""
from pathlib import Path
import pandas as pd


def load_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """Load a CSV file without modifying its source."""
    return pd.read_csv(path, **kwargs)


def load_excel(path: str | Path, **kwargs) -> pd.DataFrame:
    """Load an Excel file."""
    return pd.read_excel(path, **kwargs)
