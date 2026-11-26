"""Generate chapter-linked, reproducible visuals from the KNKT Data Logger CSV.

All plots describe transcribed table records. The GIF is a sequential display,
not a physical simulation or a causal reconstruction.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import pandas as pd
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "processed" / "data_logger_knkt_tabel_6_10.csv"
DEFAULT_OUTPUT = ROOT / "outputs"

NUMERIC_COLUMNS = [
    "km", "m", "Speed (km/h)", "Acceleration (m/sec²)",
    "Load (amps)", "EAB BP (psi)", "EAB BC (psi)",
]
CORRELATION_COLUMNS = [
    "Speed (km/h)", "Acceleration (m/sec²)", "Load (amps)",
    "EAB BP (psi)", "EAB BC (psi)",
]
CATEGORICAL_COLUMNS = ["Throttle", "PCS Open", "IBS"]


def load_data(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return immutable-style raw transcription and a typed analysis copy."""
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    required = {"Date", "Time", "Speed (km/h)", *NUMERIC_COLUMNS}
    missing = required.difference(raw.columns)
    if missing:
        raise ValueError(f"Required columns are missing: {sorted(missing)}")

    df = raw.copy()
    df["Timestamp"] = pd.to_datetime(
        df["Date"].astype(str) + " " + df["Time"].astype(str),
        format="%d/%m/%Y %H.%M.%S",
        errors="raise",
    )
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(
            df[column].replace({"---": np.nan, "": np.nan}), errors="coerce"
        )
    for column in CATEGORICAL_COLUMNS:
        if column in df.columns:
            df[column] = df[column].replace("", np.nan)
    df = df.sort_values("Timestamp").reset_index(drop=True)
    if df.empty:
        raise ValueError("Dataset contains no records.")
    df["Elapsed (s)"] = (
        df["Timestamp"] - df["Timestamp"].iloc[0]
    ).dt.total_seconds()
    df["Interval (s)"] = df["Timestamp"].diff().dt.total_seconds()
    return raw, df


def save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=240, bbox_inches="tight")
    plt.close(fig)


def chapter_ii_source_coverage(df: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 3.8), constrained_layout=True)
    ax.scatter(df["Timestamp"], np.ones(len(df)), s=35)
    ax.set_yticks([])
    ax.set_title("BAB II — Cakupan Waktu Rekaman Data Logger KA 4B")
    ax.set_xlabel("Waktu sumber (27 April 2026)")
    ax.grid(axis="x", alpha=0.25)
    gaps = df.loc[df["Interval (s)"] > 1, ["Timestamp", "Interval (s)"]]
    for row in gaps.itertuples(index=False):
        ax.annotate(
            f"Jeda {int(row[1])} detik",
            (row[0], 1), xytext=(0, 18), textcoords="offset points",
            ha="center", arrowprops={"arrowstyle": "->"},
        )
    save(fig, out / "bab_ii" / "cakupan_waktu_rekaman.png")


def chapter_iii_profile(raw: pd.DataFrame, out: Path) -> None:
    completeness = raw.replace("", np.nan).notna().mean().mul(100).sort_values()
    fig, ax = plt.subplots(figsize=(10, 7), constrained_layout=True)
    ax.barh(completeness.index, completeness.values)
    ax.set_xlim(0, 105)
    ax.set_xlabel("Kelengkapan nilai (%)")
    ax.set_title("BAB III — Kelengkapan 16 Kolom Dataset")
    ax.grid(axis="x", alpha=0.25)
    for y, value in enumerate(completeness.values):
        ax.text(value + 1, y, f"{value:.1f}%", va="center")
    save(fig, out / "bab_iii" / "kelengkapan_kolom.png")


def chapter_iv_missingness(raw: pd.DataFrame, out: Path) -> None:
    plot = raw.replace("", np.nan).isna().sum().sort_values()
    plot = plot[plot > 0]
    fig, ax = plt.subplots(figsize=(10, 4.8), constrained_layout=True)
    ax.bar(plot.index, plot.values)
    ax.set_ylabel("Jumlah nilai kosong/placeholder")
    ax.set_title("BAB IV — Nilai Tidak Tersedia pada Transkripsi")
    ax.tick_params(axis="x", rotation=35)
    ax.grid(axis="y", alpha=0.25)
    for x, value in enumerate(plot.values):
        ax.text(x, value + 0.2, str(int(value)), ha="center")
    ax.text(
        0.01, -0.34,
        "Catatan: empat kolom status tidak ditampilkan pada Tabel 9–10; "
        "7 tanda '---' pada akselerasi merupakan placeholder sumber.",
        transform=ax.transAxes, fontsize=8, wrap=True,
    )
    save(fig, out / "bab_iv" / "missingness_per_kolom.png")


def chapter_v_distributions(df: pd.DataFrame, out: Path) -> None:
    numeric = [c for c in NUMERIC_COLUMNS if c in df.columns]
    fig, axes = plt.subplots(4, 2, figsize=(12, 13), constrained_layout=True)
    for ax, column in zip(axes.flat, numeric):
        values = df[column].dropna()
        ax.hist(values, bins=min(15, max(5, values.nunique())), edgecolor="white")
        ax.set_title(column)
        ax.set_ylabel("Frekuensi")
        ax.grid(axis="y", alpha=0.2)
    for ax in axes.flat[len(numeric):]:
        ax.remove()
    fig.suptitle("BAB V — Distribusi Variabel Numerik", fontsize=15)
    save(fig, out / "bab_v" / "distribusi_numerik.png")

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5), constrained_layout=True)
    for ax, column in zip(axes, CATEGORICAL_COLUMNS):
        counts = df[column].fillna("(kosong)").value_counts()
        ax.bar(counts.index.astype(str), counts.values)
        ax.set_title(column)
        ax.set_ylabel("Jumlah rekaman")
        ax.tick_params(axis="x", rotation=35)
        ax.grid(axis="y", alpha=0.2)
    fig.suptitle("BAB V — Frekuensi Variabel Kategorikal", fontsize=15)
    save(fig, out / "bab_v" / "frekuensi_kategorikal.png")


def chapter_vi_temporal_feature(df: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(11, 4.5), constrained_layout=True)
    ax.bar(df["Elapsed (s)"], df["Interval (s)"].fillna(0), width=0.75)
    ax.axhline(1, linestyle="--", linewidth=1, label="Interval 1 detik")
    ax.set_title("BAB VI — Interval Aktual Antarrekaman")
    ax.set_xlabel("Detik sejak rekaman pertama")
    ax.set_ylabel("Selang dari rekaman sebelumnya (detik)")
    ax.legend()
    ax.grid(axis="y", alpha=0.2)
    save(fig, out / "bab_vi" / "interval_temporal.png")


def chapter_vii_visuals(df: pd.DataFrame, out: Path) -> None:
    folder = out / "bab_vii"
    folder.mkdir(parents=True, exist_ok=True)
    x = df["Elapsed (s)"]

    fig, ax = plt.subplots(figsize=(12, 5.5), constrained_layout=True)
    ax.plot(x, df["Speed (km/h)"], marker="o", linewidth=1.8)
    ax.set(title="KA 4B — Kecepatan terhadap Waktu Rekaman",
           xlabel="Detik sejak rekaman pertama", ylabel="Kecepatan (km/jam)")
    ax.grid(True, alpha=0.25)
    save(fig, folder / "grafik_kecepatan_waktu.png")

    fig, ax = plt.subplots(figsize=(12, 5.5), constrained_layout=True)
    ax.plot(x, df["EAB BP (psi)"], marker="o", label="EAB BP")
    ax.plot(x, df["EAB BC (psi)"], marker="o", label="EAB BC")
    ax.set(title="KA 4B — Tekanan Brake Pipe dan Brake Cylinder",
           xlabel="Detik sejak rekaman pertama", ylabel="Tekanan (psi)")
    ax.legend()
    ax.grid(True, alpha=0.25)
    save(fig, folder / "tekanan_bp_bc_waktu.png")

    chart = px.line(
        df, x="Timestamp", y="Speed (km/h)", markers=True,
        title="KA 4B — Deret Waktu Kecepatan",
        hover_data=["Elapsed (s)", "m", "EAB BP (psi)", "EAB BC (psi)"],
    )
    chart.update_layout(template="plotly_white", xaxis_title="Waktu sumber",
                        yaxis_title="Kecepatan (km/jam)")
    chart.write_html(folder / "deret_waktu_interaktif.html", include_plotlyjs="cdn")

    brake = px.line(
        df, x="Timestamp", y=["EAB BP (psi)", "EAB BC (psi)"], markers=True,
        title="KA 4B — Deret Waktu Tekanan BP dan BC",
    )
    brake.update_layout(template="plotly_white", xaxis_title="Waktu sumber",
                        yaxis_title="Tekanan (psi)")
    brake.write_html(folder / "tekanan_bp_bc_interaktif.html", include_plotlyjs="cdn")

    corr = df[CORRELATION_COLUMNS].corr(method="spearman", min_periods=3)
    heat = px.imshow(
        corr, text_auto=".2f", zmin=-1, zmax=1,
        color_continuous_scale="RdBu_r", origin="lower", aspect="auto",
        title="Korelasi Spearman — Variabel Operasional Terpilih",
    )
    heat.update_layout(template="plotly_white")
    heat.write_html(folder / "heatmap_spearman_interaktif.html", include_plotlyjs="cdn")

    fig, ax = plt.subplots(figsize=(8.5, 6.5), constrained_layout=True)
    image = ax.imshow(corr, vmin=-1, vmax=1, cmap="RdBu_r", aspect="auto")
    ax.set_xticks(range(len(corr.columns)), labels=corr.columns, rotation=40, ha="right")
    ax.set_yticks(range(len(corr.index)), labels=corr.index)
    ax.set_title("Korelasi Spearman — Variabel Operasional Terpilih")
    for i in range(len(corr.index)):
        for j in range(len(corr.columns)):
            value = corr.iloc[i, j]
            ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(image, ax=ax, label="Koefisien Spearman")
    save(fig, folder / "heatmap_spearman.png")

    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
    xvals = df["Elapsed (s)"].to_numpy()
    yvals = df["Speed (km/h)"].to_numpy()
    line, = ax.plot([], [], linewidth=2)
    point, = ax.plot([], [], marker="o")
    ax.set(title="Animasi Urutan Rekaman Kecepatan KA 4B",
           xlabel="Detik sejak rekaman pertama", ylabel="Kecepatan (km/jam)",
           xlim=(0, max(float(xvals.max()), 1)),
           ylim=(min(0, float(yvals.min()) - 3), float(yvals.max()) + 5))
    ax.grid(True, alpha=0.25)

    def update(frame: int):
        line.set_data(xvals[:frame + 1], yvals[:frame + 1])
        point.set_data([xvals[frame]], [yvals[frame]])
        return line, point

    animation = FuncAnimation(fig, update, frames=len(df), interval=180,
                              blit=True, repeat=False)
    folder.mkdir(parents=True, exist_ok=True)
    animation.save(folder / "animasi_urutan_kecepatan.gif",
                   writer=PillowWriter(fps=6), dpi=100)
    plt.close(fig)


def chapter_viii_outliers(df: pd.DataFrame, out: Path) -> None:
    columns = ["m", "Speed (km/h)", "Acceleration (m/sec²)",
               "Load (amps)", "EAB BP (psi)", "EAB BC (psi)"]
    fig, axes = plt.subplots(2, 3, figsize=(13, 7), constrained_layout=True)
    summary = []
    for ax, column in zip(axes.flat, columns):
        values = df[column].dropna()
        q1, q3 = values.quantile([0.25, 0.75])
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        count = int(((values < low) | (values > high)).sum())
        summary.append((column, len(values), count, low, high))
        ax.boxplot(values, vert=True)
        ax.set_title(f"{column}\nKandidat IQR: {count}")
        ax.grid(axis="y", alpha=0.2)
    fig.suptitle("BAB VIII — Box Plot dan Pemeriksaan Pencilan IQR")
    save(fig, out / "bab_viii" / "boxplot_iqr.png")
    pd.DataFrame(summary, columns=[
        "variable", "n_valid", "iqr_outlier_count", "lower_fence", "upper_fence"
    ]).to_csv(out / "bab_viii" / "ringkasan_iqr.csv", index=False)


def chapter_ix_findings(df: pd.DataFrame, raw: pd.DataFrame, out: Path) -> None:
    speed = df["Speed (km/h)"]
    gap_count = int((df["Interval (s)"] > 1).sum())
    accel_missing = int(raw["Acceleration (m/sec²)"].eq("---").sum())
    fig, ax = plt.subplots(figsize=(12, 4.8), constrained_layout=True)
    ax.axis("off")
    ax.set_title("BAB IX — Ikhtisar Temuan EDA", fontsize=16, pad=18)
    items = [
        ("Rekaman unik", f"{len(df)}"),
        ("Kolom", f"{len(raw.columns)}"),
        ("Kecepatan", f"{speed.min():.0f}–{speed.max():.0f} km/jam"),
        ("Rentang waktu", f"{df['Timestamp'].iloc[0]:%H:%M:%S}–{df['Timestamp'].iloc[-1]:%H:%M:%S}"),
        ("Interval > 1 detik", f"{gap_count} jeda"),
        ("Placeholder akselerasi", f"{accel_missing} nilai '---'"),
    ]
    for i, (label, value) in enumerate(items):
        col, row = i % 3, i // 3
        x0, y0 = 0.04 + col * 0.32, 0.62 - row * 0.43
        ax.text(x0, y0, label, transform=ax.transAxes, fontsize=11, weight="bold")
        ax.text(x0, y0 - 0.13, value, transform=ax.transAxes, fontsize=14)
    ax.text(
        0.04, 0.04,
        "Deskriptif terhadap transkripsi Tabel 6–10; bukan simulasi fisik, "
        "rekonstruksi kausal, atau penetapan penyebab kecelakaan.",
        transform=ax.transAxes, fontsize=9,
    )
    save(fig, out / "bab_ix" / "ikhtisar_temuan.png")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    raw, df = load_data(args.input)
    out = args.output_dir
    chapter_ii_source_coverage(df, out)
    chapter_iii_profile(raw, out)
    chapter_iv_missingness(raw, out)
    chapter_v_distributions(df, out)
    chapter_vi_temporal_feature(df, out)
    chapter_vii_visuals(df, out)
    chapter_viii_outliers(df, out)
    chapter_ix_findings(df, raw, out)
    files = sorted(p for p in out.rglob("*") if p.is_file())
    print(f"Generated {len(files)} artifacts under {out}")
    for path in files:
        print(f"{path.relative_to(out)}\t{path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
