"""Small, explicit helpers for exporting EDA artifacts."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def export_dataframe_csv(
    df: pd.DataFrame,
    path: str | Path,
    *,
    index: bool = False,
) -> Path:
    """Write a DataFrame to CSV and return the destination path."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=index)
    return destination


def save_figure(
    figure: plt.Figure,
    path: str | Path,
    *,
    dpi: int = 150,
    bbox_inches: str | None = "tight",
) -> Path:
    """Save a Matplotlib figure to the requested path."""
    if dpi < 1:
        raise ValueError("dpi must be at least 1.")
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination, dpi=dpi, bbox_inches=bbox_inches)
    return destination


def write_markdown_report(
    content: str,
    path: str | Path,
) -> Path:
    """Write caller-provided Markdown without altering its content."""
    if not isinstance(content, str):
        raise TypeError("content must be a string.")
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    return destination
