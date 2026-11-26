"""Generate reproducible time-series visuals from the KNKT Data Logger CSV.

The GIF animates recorded rows; it is not a physical simulation or causal
reconstruction. Plotly HTML files provide interactive companions.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "processed" / "data_logger_knkt_tabel_6_10.csv"
DEFAULT_OUTPUT = ROOT / "outputs"

def load_data(path: Path) -> pd.DataFrame:
    """Load source values and derive a timestamp/elapsed-time axis."""
    df = pd.read_csv(path)
    required = {"Date", "Time", "Speed (km/h)"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Required columns are missing: {sorted(missing)}")
    df = df.copy()
    df["Timestamp"] = pd.to_datetime(
        df["Date"].astype(str) + " " + df["Time"].astype(str),
        format="%d/%m/%Y %H.%M.%S",
        errors="coerce",
    )
    df["Speed (km/h)"] = pd.to_numeric(df["Speed (km/h)"], errors="coerce")
    df = df.dropna(subset=["Timestamp", "Speed (km/h)"]).sort_values("Timestamp")
    if df.empty:
        raise ValueError("No valid timestamp/speed records found.")
    df["Elapsed (s)"] = (df["Timestamp"] - df["Timestamp"].iloc[0]).dt.total_seconds()
    return df

def make_speed_animation(df: pd.DataFrame, output: Path) -> None:
    """Animate recorded speed in timestamp order."""
    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
    x, y = df["Elapsed (s)"].to_numpy(), df["Speed (km/h)"].to_numpy()
    line, = ax.plot([], [], color="#0072B2", linewidth=2.5)
    point, = ax.plot([], [], marker="o", color="#D55E00", markersize=7)
    ax.set(title="KA 4B Data Logger — Recorded Speed Over Time",
           xlabel="Elapsed time from first available record (seconds)",
           ylabel="Speed (km/h)", xlim=(float(x.min()), max(float(x.max()), 1.0)),
           ylim=(min(0.0, float(y.min()) - 5), float(y.max()) + 5))
    ax.grid(True, alpha=0.25)
    def update(frame: int):
        line.set_data(x[:frame + 1], y[:frame + 1])
        point.set_data([x[frame]], [y[frame]])
        return line, point
    animation = FuncAnimation(fig, update, frames=len(df), interval=180, blit=True, repeat=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    animation.save(output, writer=PillowWriter(fps=6), dpi=110)
    plt.close(fig)

def make_visuals(df: pd.DataFrame, output_dir: Path) -> None:
    """Export high-resolution static plots and interactive Plotly charts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
    ax.plot(df["Elapsed (s)"], df["Speed (km/h)"], marker="o", linewidth=1.8, color="#0072B2")
    ax.set(title="KA 4B Data Logger — Speed Time Series",
           xlabel="Elapsed time from first available record (seconds)", ylabel="Speed (km/h)")
    ax.grid(True, alpha=0.25)
    fig.savefig(output_dir / "speed_timeseries.png", dpi=300)
    plt.close(fig)
    chart = px.line(df, x="Timestamp", y="Speed (km/h)", markers=True,
                    title="KA 4B Data Logger — Recorded Speed",
                    color_discrete_sequence=["#0072B2"], hover_data=["Elapsed (s)"])
    chart.update_layout(template="plotly_white")
    chart.write_html(output_dir / "speed_timeseries_interactive.html", include_plotlyjs="cdn")
    numeric = df.select_dtypes(include="number").drop(columns=["Elapsed (s)"], errors="ignore")
    corr = numeric.corr(method="spearman", min_periods=3)
    if not corr.empty:
        heat = px.imshow(corr, text_auto=".2f", zmin=-1, zmax=1,
                         color_continuous_scale="Viridis", aspect="auto",
                         title="Spearman Correlation — Numeric Data Logger Variables")
        heat.write_html(output_dir / "correlation_heatmap_interactive.html", include_plotlyjs="cdn")
        fig, ax = plt.subplots(figsize=(10, 8), constrained_layout=True)
        image = ax.imshow(corr, vmin=-1, vmax=1, cmap="viridis", aspect="auto")
        ax.set_xticks(range(len(corr.columns)), labels=corr.columns, rotation=45, ha="right")
        ax.set_yticks(range(len(corr.index)), labels=corr.index)
        ax.set_title("Spearman Correlation — Numeric Data Logger Variables")
        fig.colorbar(image, ax=ax, label="Spearman correlation")
        fig.savefig(output_dir / "correlation_heatmap.png", dpi=300)
        plt.close(fig)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    data = load_data(args.input)
    make_speed_animation(data, args.output_dir / "speed_timeseries.gif")
    make_visuals(data, args.output_dir)
    print(f"Visual outputs written to: {args.output_dir}")

if __name__ == "__main__":
    main()
