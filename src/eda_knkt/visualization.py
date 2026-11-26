"""Reusable plotting helpers for exploratory data analysis."""
from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt
import pandas as pd


def _require_columns(df: pd.DataFrame, columns: Sequence[str]) -> None:
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise KeyError(f"Column(s) not found: {missing}")


def plot_numeric_distribution(
    df: pd.DataFrame,
    column: str,
    *,
    bins: int = 20,
    kde: bool = False,
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Plot a numeric column histogram; optional KDE is intentionally omitted."""
    _require_columns(df, [column])
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise TypeError(f"Column '{column}' must be numeric.")
    if bins < 1:
        raise ValueError("bins must be at least 1.")
    if ax is None:
        _, ax = plt.subplots()
    values = df[column].dropna()
    ax.hist(values, bins=bins)
    ax.set(title=f"Distribution of {column}", xlabel=column, ylabel="Frequency")
    if kde:
        # Keep the core plotting dependency minimal; callers can add KDE separately.
        ax.text(
            0.99, 0.98, "KDE not included",
            transform=ax.transAxes, ha="right", va="top",
        )
    return ax


def plot_categorical_counts(
    df: pd.DataFrame,
    column: str,
    *,
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Plot non-null category frequencies as a bar chart."""
    _require_columns(df, [column])
    if ax is None:
        _, ax = plt.subplots()
    counts = df[column].dropna().value_counts()
    counts.plot(kind="bar", ax=ax)
    ax.set(title=f"Counts of {column}", xlabel=column, ylabel="Frequency")
    return ax


def plot_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    *,
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Plot two explicitly selected numeric columns against each other."""
    _require_columns(df, [x, y])
    non_numeric = [
        column for column in [x, y]
        if not pd.api.types.is_numeric_dtype(df[column])
    ]
    if non_numeric:
        raise TypeError(f"Non-numeric column(s) selected: {non_numeric}")
    if ax is None:
        _, ax = plt.subplots()
    points = df.loc[:, [x, y]].dropna()
    ax.scatter(points[x], points[y])
    ax.set(title=f"{y} vs {x}", xlabel=x, ylabel=y)
    return ax


def plot_correlation_heatmap(
    correlations: pd.DataFrame,
    *,
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Render a correlation matrix with a Matplotlib color mesh."""
    if correlations.empty:
        raise ValueError("correlations must not be empty.")
    if ax is None:
        _, ax = plt.subplots()
    image = ax.imshow(correlations, vmin=-1, vmax=1, cmap="coolwarm")
    labels = [str(value) for value in correlations.columns]
    ax.set_xticks(range(len(labels)), labels=labels, rotation=45, ha="right")
    ax.set_yticks(range(len(labels)), labels=labels)
    ax.set_title("Correlation matrix")
    ax.figure.colorbar(image, ax=ax, label="Correlation")
    return ax
