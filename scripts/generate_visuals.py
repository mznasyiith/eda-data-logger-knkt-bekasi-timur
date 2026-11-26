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

from eda_knkt.transformation import add_distance_to_stop_feature

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "processed" / "data_logger_knkt_tabel_6_10.csv"
DEFAULT_OUTPUT = ROOT / "outputs"

SOURCE_DISTANCE_COLUMNS = ["km", "m"]
NUMERIC_COLUMNS = [
    "distance_to_stop_m",
    "Speed (km/h)",
    "Acceleration (m/sec²)",
    "Load (amps)",
    "EAB BP (psi)",
    "EAB BC (psi)",
]
CORRELATION_COLUMNS = [
    "distance_to_stop_m",
    "Speed (km/h)",
    "Acceleration (m/sec²)",
    "Load (amps)",
    "EAB BP (psi)",
    "EAB BC (psi)",
]
CATEGORICAL_COLUMNS = ["Throttle", "PCS Open", "IBS"]
DISPLAY_LABELS = {
    "distance_to_stop_m": "Jarak tersisa menuju titik henti akhir (m)",
    "Speed (km/h)": "Kecepatan (km/jam)",
    "Acceleration (m/sec²)": "Akselerasi (m/s²)",
    "Load (amps)": "Arus motor traksi (A)",
    "EAB BP (psi)": "Tekanan Brake Pipe (psi)",
    "EAB BC (psi)": "Tekanan Brake Cylinder (psi)",
}


def load_data(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return immutable-style raw transcription and a typed analysis copy."""
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    required = {
        "Date",
        "Time",
        "Speed (km/h)",
        *SOURCE_DISTANCE_COLUMNS,
        "Acceleration (m/sec²)",
        "Load (amps)",
        "EAB BP (psi)",
        "EAB BC (psi)",
    }
    missing = required.difference(raw.columns)
    if missing:
        raise ValueError(f"Required columns are missing: {sorted(missing)}")

    df = raw.copy()
    df["Timestamp"] = pd.to_datetime(
        df["Date"].astype(str) + " " + df["Time"].astype(str),
        format="%d/%m/%Y %H.%M.%S",
        errors="raise",
    )
    numeric_source_columns = [
        *SOURCE_DISTANCE_COLUMNS,
        "Speed (km/h)",
        "Acceleration (m/sec²)",
        "Load (amps)",
        "EAB BP (psi)",
        "EAB BC (psi)",
    ]
    for column in numeric_source_columns:
        df[column] = pd.to_numeric(
            df[column].replace({"---": np.nan, "": np.nan}), errors="coerce"
        )
    # Keep source columns in raw; analyze their verified combined distance only.
    df = add_distance_to_stop_feature(df)
    for column in CATEGORICAL_COLUMNS:
        if column in df.columns:
            df[column] = df[column].replace("", np.nan)
    df = df.sort_values("Timestamp").reset_index(drop=True)
    if df.empty:
        raise ValueError("Dataset contains no records.")
    df["Elapsed (s)"] = (df["Timestamp"] - df["Timestamp"].iloc[0]).dt.total_seconds()
    df["Interval (s)"] = df["Timestamp"].diff().dt.total_seconds()
    return raw, df


def save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=240, bbox_inches="tight")
    plt.close(fig)


def chapter_i_scope(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 4.5), constrained_layout=True)
    ax.axis("off")
    ax.set_title("BAB I — Ruang Lingkup dan Tujuan EDA", fontsize=16, pad=18)
    stages = [
        ("SUMBER", "Tabel 6–10\nLaporan KNKT"),
        ("DATASET", "58 rekaman unik\n16 kolom"),
        ("ANALISIS", "Kualitas data\nStatistik dan visual"),
        ("BATAS", "Deskriptif\nTidak menyimpulkan sebab"),
    ]
    for i, (head, body) in enumerate(stages):
        x = 0.035 + i * 0.245
        ax.text(
            x,
            0.62,
            head,
            transform=ax.transAxes,
            fontsize=12,
            weight="bold",
            bbox={"boxstyle": "round,pad=0.65", "facecolor": "#e8f1f8"},
        )
        ax.text(
            x,
            0.37,
            body,
            transform=ax.transAxes,
            fontsize=10.5,
            va="center",
            linespacing=1.5,
        )
        if i < len(stages) - 1:
            ax.annotate(
                "",
                xy=(x + 0.215, 0.57),
                xytext=(x + 0.17, 0.57),
                xycoords=ax.transAxes,
                arrowprops={"arrowstyle": "->"},
            )
    ax.text(
        0.03,
        0.08,
        "Tujuan: mendeskripsikan rekaman yang tersedia, memeriksa kualitasnya, "
        "dan menjaga batas interpretasi bukti.",
        transform=ax.transAxes,
        fontsize=10,
    )
    save(fig, out / "bab_i" / "ruang_lingkup_eda.png")


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
            (row[0], 1),
            xytext=(0, 18),
            textcoords="offset points",
            ha="center",
            arrowprops={"arrowstyle": "->"},
        )
    save(fig, out / "bab_ii" / "cakupan_waktu_rekaman.png")


def chapter_iii_profile(raw: pd.DataFrame, out: Path) -> None:
    profile = raw.replace({"": np.nan, "---": np.nan})
    completeness = profile.notna().mean().mul(100).sort_values()
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
    plot = raw.replace({"": np.nan, "---": np.nan}).isna().sum().sort_values()
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
        0.01,
        -0.34,
        "Catatan: empat kolom status tidak ditampilkan pada Tabel 9–10; "
        "7 tanda '---' pada akselerasi merupakan placeholder sumber.",
        transform=ax.transAxes,
        fontsize=8,
        wrap=True,
    )
    save(fig, out / "bab_iv" / "missingness_per_kolom.png")


def chapter_v_distributions(df: pd.DataFrame, out: Path) -> None:
    numeric = [c for c in NUMERIC_COLUMNS if c in df.columns]
    fig, axes = plt.subplots(4, 2, figsize=(12, 13), constrained_layout=True)
    for ax, column in zip(axes.flat, numeric):
        values = df[column].dropna()
        ax.hist(values, bins=min(15, max(5, values.nunique())), edgecolor="white")
        ax.set_title(DISPLAY_LABELS.get(column, column))
        ax.set_ylabel("Frekuensi")
        ax.grid(axis="y", alpha=0.2)
    for ax in axes.flat[len(numeric) :]:
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
    ax.set(
        title="KA 4B — Kecepatan terhadap Waktu Rekaman",
        xlabel="Detik sejak rekaman pertama",
        ylabel="Kecepatan (km/jam)",
    )
    ax.grid(True, alpha=0.25)
    save(fig, folder / "grafik_kecepatan_waktu.png")

    fig, ax = plt.subplots(figsize=(12, 5.5), constrained_layout=True)
    ax.plot(x, df["EAB BP (psi)"], marker="o", label="EAB BP")
    ax.plot(x, df["EAB BC (psi)"], marker="o", label="EAB BC")
    ax.set(
        title="KA 4B — Tekanan Brake Pipe dan Brake Cylinder",
        xlabel="Detik sejak rekaman pertama",
        ylabel="Tekanan (psi)",
    )
    ax.legend()
    ax.grid(True, alpha=0.25)
    save(fig, folder / "tekanan_bp_bc_waktu.png")

    chart = px.line(
        df,
        x="Timestamp",
        y="Speed (km/h)",
        markers=True,
        title="KA 4B — Deret Waktu Kecepatan",
        hover_data=[
            "Elapsed (s)",
            "distance_to_stop_m",
            "EAB BP (psi)",
            "EAB BC (psi)",
        ],
    )
    chart.update_layout(
        template="plotly_white",
        xaxis_title="Waktu sumber",
        yaxis_title="Kecepatan (km/jam)",
    )
    chart.write_html(folder / "deret_waktu_interaktif.html", include_plotlyjs="cdn")

    brake = px.line(
        df,
        x="Timestamp",
        y=["EAB BP (psi)", "EAB BC (psi)"],
        markers=True,
        title="KA 4B — Deret Waktu Tekanan BP dan BC",
    )
    brake.update_layout(
        template="plotly_white", xaxis_title="Waktu sumber", yaxis_title="Tekanan (psi)"
    )
    brake.write_html(folder / "tekanan_bp_bc_interaktif.html", include_plotlyjs="cdn")

    corr = df[CORRELATION_COLUMNS].corr(method="spearman", min_periods=3)
    corr_display = corr.rename(index=DISPLAY_LABELS, columns=DISPLAY_LABELS)
    heat = px.imshow(
        corr_display,
        text_auto=".3f",
        zmin=-1,
        zmax=1,
        color_continuous_scale="RdBu_r",
        origin="lower",
        aspect="auto",
        title="Korelasi Spearman — Variabel Operasional Terpilih",
    )
    heat.update_layout(template="plotly_white")
    heat.write_html(folder / "heatmap_spearman_interaktif.html", include_plotlyjs="cdn")
    counts = pd.DataFrame(
        index=CORRELATION_COLUMNS, columns=CORRELATION_COLUMNS, dtype=int
    )
    for left in CORRELATION_COLUMNS:
        for right in CORRELATION_COLUMNS:
            counts.loc[left, right] = int(df[[left, right]].dropna().shape[0])
    counts.to_csv(folder / "jumlah_pasangan_valid_korelasi.csv")

    fig, ax = plt.subplots(figsize=(8.5, 6.5), constrained_layout=True)
    image = ax.imshow(corr_display, vmin=-1, vmax=1, cmap="RdBu_r", aspect="auto")
    ax.set_xticks(
        range(len(corr_display.columns)),
        labels=corr_display.columns,
        rotation=40,
        ha="right",
    )
    ax.set_yticks(range(len(corr_display.index)), labels=corr_display.index)
    ax.set_title("Korelasi Spearman — Variabel Operasional Terpilih")
    for i in range(len(corr_display.index)):
        for j in range(len(corr_display.columns)):
            value = corr_display.iloc[i, j]
            ax.text(j, i, f"{value:.3f}", ha="center", va="center", fontsize=8)
    fig.colorbar(image, ax=ax, label="Koefisien Spearman")
    save(fig, folder / "heatmap_spearman.png")

    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
    xvals = df["Elapsed (s)"].to_numpy()
    yvals = df["Speed (km/h)"].to_numpy()
    (line,) = ax.plot([], [], linewidth=2)
    (point,) = ax.plot([], [], marker="o")
    ax.set(
        title="Animasi Urutan Rekaman Kecepatan KA 4B",
        xlabel="Detik sejak rekaman pertama",
        ylabel="Kecepatan (km/jam)",
        xlim=(0, max(float(xvals.max()), 1)),
        ylim=(min(0, float(yvals.min()) - 3), float(yvals.max()) + 5),
    )
    ax.grid(True, alpha=0.25)

    def update(frame: int):
        line.set_data(xvals[: frame + 1], yvals[: frame + 1])
        point.set_data([xvals[frame]], [yvals[frame]])
        return line, point

    animation = FuncAnimation(
        fig, update, frames=len(df), interval=180, blit=True, repeat=False
    )
    folder.mkdir(parents=True, exist_ok=True)
    animation.save(
        folder / "animasi_urutan_kecepatan.gif", writer=PillowWriter(fps=6), dpi=100
    )
    plt.close(fig)


def chapter_viii_outliers(df: pd.DataFrame, out: Path) -> None:
    columns = [
        "distance_to_stop_m",
        "Speed (km/h)",
        "Acceleration (m/sec²)",
        "Load (amps)",
        "EAB BP (psi)",
        "EAB BC (psi)",
    ]
    fig, axes = plt.subplots(2, 3, figsize=(13, 7), constrained_layout=True)
    summary = []
    for ax, column in zip(axes.flat, columns):
        values = df[column].dropna()
        q1, q3 = values.quantile([0.25, 0.75])
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        count = int(((values < low) | (values > high)).sum())
        summary.append((column, len(values), count, low, high))
        ax.boxplot(values, orientation="vertical")
        ax.set_title(f"{DISPLAY_LABELS.get(column, column)}\nKandidat IQR: {count}")
        ax.grid(axis="y", alpha=0.2)
    fig.suptitle("BAB VIII — Box Plot dan Pemeriksaan Pencilan IQR")
    save(fig, out / "bab_viii" / "boxplot_iqr.png")
    pd.DataFrame(
        summary,
        columns=[
            "variable",
            "n_valid",
            "iqr_outlier_count",
            "lower_fence",
            "upper_fence",
        ],
    ).to_csv(out / "bab_viii" / "ringkasan_iqr.csv", index=False)


def chapter_ix_findings(df: pd.DataFrame, raw: pd.DataFrame, out: Path) -> None:
    speed = df["Speed (km/h)"]
    gap_count = int((df["Interval (s)"] > 1).sum())
    accel_missing = int(raw["Acceleration (m/sec²)"].eq("---").sum())
    fig, ax = plt.subplots(figsize=(12, 4.8), constrained_layout=True)
    ax.axis("off")
    ax.set_title("BAB IX — Ikhtisar Temuan EDA", fontsize=16, pad=18)
    items = [
        ("REKAMAN UNIK", f"{len(df)}"),
        ("JUMLAH KOLOM", f"{len(raw.columns)}"),
        ("RENTANG KECEPATAN", f"{speed.min():.0f}–{speed.max():.0f} km/jam"),
        (
            "RENTANG WAKTU",
            f"{df['Timestamp'].iloc[0]:%H:%M:%S} – {df['Timestamp'].iloc[-1]:%H:%M:%S}",
        ),
        ("JEDA > 1 DETIK", f"{gap_count} interval"),
        ("PLACEHOLDER AKSELERASI", f"{accel_missing} nilai"),
    ]
    for i, (label, value) in enumerate(items):
        col, row = i % 3, i // 3
        x0, y0 = 0.045 + col * 0.32, 0.68 - row * 0.43
        ax.text(
            x0,
            y0,
            label,
            transform=ax.transAxes,
            fontsize=9.5,
            weight="bold",
            bbox={"boxstyle": "round,pad=0.45", "facecolor": "#e8f1f8"},
        )
        ax.text(
            x0,
            y0 - 0.16,
            value,
            transform=ax.transAxes,
            fontsize=12,
            va="center",
            linespacing=1.4,
        )
    ax.text(
        0.04,
        0.04,
        "Deskriptif terhadap transkripsi Tabel 6–10; bukan simulasi fisik, "
        "rekonstruksi kausal, atau penetapan penyebab kecelakaan.",
        transform=ax.transAxes,
        fontsize=9,
    )
    save(fig, out / "bab_ix" / "ikhtisar_temuan.png")


# Extended, evidence-aware chapter visuals.
def _panel_title(ax, title):
    ax.set_title(title, loc="left", fontsize=10, weight="bold", pad=8)
    ax.grid(alpha=0.18)


def _save_table(fig, ax, path):
    ax.axis("off")
    save(fig, path)


def _break_lines(x, y, intervals):
    xx, yy = [], []
    for i, (xv, yv) in enumerate(zip(x, y)):
        if i and intervals[i] > 1:
            xx.append(np.nan)
            yy.append(np.nan)
        xx.append(xv)
        yy.append(yv)
    return np.asarray(xx, dtype=float), np.asarray(yy, dtype=float)


def extended_chapter_i(df, raw, out):
    folder = out / "bab_i"
    folder.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
    ax.axis("off")
    ax.set_title(
        "BAB I — Issue Tree: Pertanyaan Analitis EDA", fontsize=15, weight="bold"
    )
    ax.text(
        0.5,
        0.88,
        "Apa yang dapat dijelaskan oleh transkripsi Data Logger KA 4B?",
        ha="center",
        va="center",
        transform=ax.transAxes,
        fontsize=12,
        weight="bold",
        bbox=dict(boxstyle="round,pad=.7", fc="#e8f1f8", ec="#476b83"),
    )
    branches = [
        (
            0.08,
            "Kualitas data",
            "Kelengkapan • duplikasi\nplaceholder • interval waktu",
        ),
        (0.32, "Karakteristik", "Statistik deskriptif\nDistribusi numerik/kategori"),
        (0.56, "Perubahan temporal", "Kecepatan • tekanan\narus • status operasi"),
        (
            0.80,
            "Batas bukti",
            "Sumber tunggal • gap waktu\nTidak menyimpulkan kausalitas",
        ),
    ]
    for x, title, body in branches:
        ax.annotate(
            "",
            xy=(x + 0.09, 0.57),
            xytext=(0.5, 0.79),
            xycoords=ax.transAxes,
            arrowprops=dict(arrowstyle="->", lw=1.3, color="#476b83"),
        )
        ax.text(
            x + 0.09,
            0.49,
            title,
            ha="center",
            transform=ax.transAxes,
            weight="bold",
            bbox=dict(boxstyle="round,pad=.45", fc="#edf4ee", ec="#5c8068"),
        )
        ax.text(
            x + 0.09,
            0.30,
            body,
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=9,
            linespacing=1.5,
        )
    ax.text(
        0.5,
        0.08,
        "Keluaran: deskripsi data yang dapat ditelusuri, bukan rekonstruksi kecelakaan.",
        ha="center",
        transform=ax.transAxes,
        fontsize=9,
        style="italic",
    )
    save(fig, folder / "issue_tree_pertanyaan_eda.png")

    fig, ax = plt.subplots(figsize=(12, 3.7), constrained_layout=True)
    ax.axis("off")
    ax.set_title("BAB I — Alur Pemeriksaan Data (As-Is)", fontsize=15, weight="bold")
    stages = [
        ("Laporan KNKT", "Tabel 6–10"),
        ("Ekstraksi", "PDF dan transkripsi"),
        ("Validasi", "59 baris sumber"),
        ("Deduplikasi", "58 rekaman unik"),
        ("EDA", "Kualitas, karakteristik,\nhubungan temporal"),
        ("Komunikasi", "Temuan dan batasan"),
    ]
    for i, (head, body) in enumerate(stages):
        x = 0.025 + i * 0.163
        ax.text(
            x,
            0.62,
            head,
            transform=ax.transAxes,
            fontsize=9,
            weight="bold",
            bbox=dict(boxstyle="round,pad=.45", fc="#e8f1f8", ec="#476b83"),
        )
        ax.text(
            x + 0.005, 0.34, body, transform=ax.transAxes, fontsize=8.5, va="center"
        )
        if i < len(stages) - 1:
            ax.annotate(
                "",
                xy=(x + 0.155, 0.59),
                xytext=(x + 0.125, 0.59),
                xycoords=ax.transAxes,
                arrowprops=dict(arrowstyle="->"),
            )
    save(fig, folder / "alur_pemeriksaan_data.png")

    fig, ax = plt.subplots(figsize=(10, 3.6), constrained_layout=True)
    ax.axis("off")
    ax.set_title("BAB I — KPI Cakupan EDA", fontsize=15, weight="bold")
    metrics = [
        ("Rekaman unik", f"{len(df)}"),
        ("Kolom", f"{len(raw.columns)}"),
        ("Baris sumber", "59"),
        ("Placeholder akselerasi", str(raw["Acceleration (m/sec²)"].eq("---").sum())),
        ("Gap > 1 detik", str(int((df["Interval (s)"] > 1).sum()))),
    ]
    for i, (label, value) in enumerate(metrics):
        x = 0.025 + i * 0.195
        ax.text(
            x,
            0.68,
            label,
            transform=ax.transAxes,
            fontsize=8.5,
            weight="bold",
            bbox=dict(boxstyle="round,pad=.45", fc="#e8f1f8"),
        )
        ax.text(
            x + 0.015, 0.32, value, transform=ax.transAxes, fontsize=18, weight="bold"
        )
    save(fig, folder / "kpi_cakupan_eda.png")


def extended_chapter_ii(df, raw, out):
    folder = out / "bab_ii"
    folder.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 4.3), constrained_layout=True)
    ax.axis("off")
    ax.set_title(
        "BAB II — Pipeline Akuisisi dan Penyiapan Data", fontsize=15, weight="bold"
    )
    nodes = [
        ("Sumber primer", "Laporan akhir KNKT\nTabel 6–10"),
        ("Ekstraksi", "Pembacaan tabel PDF\nTranskripsi manual"),
        ("Validasi", "Kolom, timestamp,\nformat dan nilai"),
        ("Pengolahan", "Deduplikasi lintas tabel\nRaw dan analysis copy"),
        ("Dataset", "58 × 16\nCSV terstruktur"),
    ]
    for i, (h, b) in enumerate(nodes):
        x = 0.025 + i * 0.195
        ax.text(
            x,
            0.62,
            h,
            transform=ax.transAxes,
            weight="bold",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=.5", fc="#e8f1f8"),
        )
        ax.text(x + 0.005, 0.35, b, transform=ax.transAxes, fontsize=8.5, va="center")
        if i < 4:
            ax.annotate(
                "",
                xy=(x + 0.18, 0.59),
                xytext=(x + 0.145, 0.59),
                xycoords=ax.transAxes,
                arrowprops=dict(arrowstyle="->"),
            )
    ax.text(
        0.03,
        0.08,
        "Tidak ada klaim ETL otomatis: ekstraksi tabel dilakukan melalui transkripsi.",
        transform=ax.transAxes,
        fontsize=9,
        style="italic",
    )
    save(fig, folder / "pipeline_akuisisi_data.png")

    mapping = [
        ["Pertanyaan analitis", "Kolom utama", "Bentuk pemeriksaan"],
        ["Apakah data lengkap?", "Seluruh 16 kolom", "Missingness, placeholder"],
        [
            "Bagaimana parameter berubah?",
            "Timestamp, Speed, BP, BC, Load",
            "Deret waktu",
        ],
        [
            "Bagaimana status tercatat?",
            "Throttle, PCS Open, IBS",
            "Frekuensi dan timeline",
        ],
        [
            "Apakah ada nilai ekstrem?",
            "distance_to_stop_m, Speed, Acceleration, Load, BP, BC",
            "IQR dan konteks waktu",
        ],
        [
            "Apa batas interpretasi?",
            "Sumber dan metadata waktu",
            "Provenance dan keterbatasan",
        ],
    ]
    fig, ax = plt.subplots(figsize=(12, 4.2), constrained_layout=True)
    table = ax.table(
        cellText=mapping[1:], colLabels=mapping[0], loc="center", cellLoc="left"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    table.scale(1, 1.7)
    ax.axis("off")
    ax.set_title(
        "BAB II — Matriks Penyelarasan Data dan Pertanyaan",
        fontsize=14,
        weight="bold",
        pad=15,
    )
    save(fig, folder / "matriks_data_ke_pertanyaan.png")

    fig, ax = plt.subplots(figsize=(12, 3.2), constrained_layout=True)
    ax.axis("off")
    ax.set_title("BAB II — Ringkasan Skema Dataset", fontsize=14, weight="bold")
    groups = [
        ("Waktu/lokasi", "Date • Time • komponen jarak km+m"),
        ("Dinamika", "Speed • Acceleration • Load"),
        ("Pengereman", "EAB BP • EAB BC"),
        ("Status", "DB Excit • Throttle • PCS Open\nDir Call • DB Set • DB Star • IBS"),
    ]
    for i, (h, b) in enumerate(groups):
        x = 0.04 + i * 0.245
        ax.text(
            x,
            0.62,
            h,
            transform=ax.transAxes,
            weight="bold",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=.5", fc="#e8f1f8"),
        )
        ax.text(x, 0.30, b, transform=ax.transAxes, fontsize=8.5, va="center")
    save(fig, folder / "ringkasan_skema_dataset.png")


def extended_chapter_iii(df, raw, out):
    folder = out / "bab_iii"
    folder.mkdir(parents=True, exist_ok=True)
    nrow, ncol = raw.shape
    filled = raw.replace({"": np.nan, "---": np.nan}).notna().sum().sum()
    fig, ax = plt.subplots(figsize=(10, 3.2), constrained_layout=True)
    ax.axis("off")
    ax.set_title("BAB III — Scorecard Struktur Dataset", fontsize=14, weight="bold")
    vals = [
        ("Baris", str(nrow)),
        ("Kolom", str(ncol)),
        ("Sel total", str(nrow * ncol)),
        ("Sel terisi", str(int(filled))),
        ("Sel kosong/placeholder", str(int(nrow * ncol - filled))),
    ]
    for i, (lab, val) in enumerate(vals):
        x = 0.025 + i * 0.195
        ax.text(
            x,
            0.68,
            lab,
            transform=ax.transAxes,
            fontsize=9,
            weight="bold",
            bbox=dict(boxstyle="round,pad=.4", fc="#e8f1f8"),
        )
        ax.text(x, 0.30, val, transform=ax.transAxes, fontsize=19, weight="bold")
    save(fig, folder / "scorecard_struktur_dataset.png")

    preview = raw.head(8).copy()
    preview["Time"] = preview["Time"].astype(str)
    fig, ax = plt.subplots(figsize=(15, 4.2), constrained_layout=True)
    ax.axis("off")
    tbl = ax.table(
        cellText=preview.values,
        colLabels=preview.columns,
        loc="center",
        cellLoc="center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(6.7)
    tbl.scale(1, 1.55)
    ax.set_title(
        "BAB III — Cuplikan Delapan Rekaman Pertama (Data Mentah)",
        fontsize=13,
        weight="bold",
        pad=12,
    )
    save(fig, folder / "cuplikan_data_mentah.png")

    type_counts = df[raw.columns].dtypes.astype(str).value_counts()
    fig, ax = plt.subplots(figsize=(7, 3.8), constrained_layout=True)
    ax.bar(type_counts.index, type_counts.values)
    ax.set(
        title="BAB III — Distribusi Tipe Data pada Salinan Analisis",
        ylabel="Jumlah kolom",
        xlabel="Tipe data setelah konversi",
    )
    ax.grid(axis="y", alpha=0.2)
    for i, value in enumerate(type_counts.values):
        ax.text(i, value + 0.1, str(value), ha="center")
    save(fig, folder / "distribusi_tipe_data_raw.png")

    cols = [c for c in NUMERIC_COLUMNS if c in df and df[c].notna().any()]
    stats = df[cols].agg(["min", "max"]).T
    fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
    for i, (col, row) in enumerate(stats.iterrows()):
        ax.plot([row["min"], row["max"]], [i, i], marker="o", lw=2)
        ax.text(row["min"], i + 0.13, f"{row['min']:g}", ha="center", fontsize=8)
        ax.text(row["max"], i + 0.13, f"{row['max']:g}", ha="center", fontsize=8)
    ax.set_yticks(range(len(cols)), labels=cols)
    ax.set_xlabel("Rentang nilai (satuan mengikuti variabel)")
    ax.set_title(
        "BAB III — Rentang Minimum dan Maksimum Variabel Numerik", weight="bold"
    )
    ax.grid(axis="x", alpha=0.2)
    save(fig, folder / "rentang_minimum_maksimum.png")


def extended_chapter_iv(df, raw, out):
    folder = out / "bab_iv"
    folder.mkdir(parents=True, exist_ok=True)
    columns = list(raw.columns)
    matrix = np.zeros((len(raw), len(columns)), dtype=int)
    for j, col in enumerate(columns):
        vals = raw[col].astype(str)
        matrix[:, j] = np.where(vals.eq("---"), 2, np.where(vals.eq(""), 1, 0))
    fig, ax = plt.subplots(figsize=(14, 7), constrained_layout=True)
    from matplotlib.colors import ListedColormap

    cmap = ListedColormap(["#e7f1e9", "#d7dce2", "#e5a34b"])
    ax.imshow(matrix, aspect="auto", interpolation="nearest", cmap=cmap, vmin=0, vmax=2)
    ax.set_xticks(
        range(len(columns)), labels=columns, rotation=55, ha="right", fontsize=8
    )
    tick_idx = list(range(0, len(raw), 3))
    ax.set_yticks(tick_idx, labels=raw.iloc[tick_idx]["Time"], fontsize=7)
    ax.set_title(
        "BAB IV — Missingness Matrix: Nilai Terisi, Kosong, dan Placeholder",
        weight="bold",
    )
    from matplotlib.patches import Patch

    ax.legend(
        handles=[
            Patch(color="#e7f1e9", label="Terisi"),
            Patch(color="#d7dce2", label="Kosong"),
            Patch(color="#e5a34b", label="Placeholder ---"),
        ],
        loc="upper left",
        bbox_to_anchor=(1.01, 1),
    )
    ax.set_xlabel("Kolom dataset")
    ax.set_ylabel("Waktu sumber (label tiap 3 rekaman)")
    save(fig, folder / "missingness_matrix.png")

    structural_cols = ["DB Excit", "Dir Call", "DB Set", "DB Star"]
    counts = raw[structural_cols].eq("").sum()
    fig, ax = plt.subplots(figsize=(9, 3.8), constrained_layout=True)
    ax.bar(counts.index, counts.values)
    ax.set(
        title="BAB IV — Ketidaktersediaan Empat Kolom Status",
        ylabel="Jumlah baris kosong",
    )
    ax.grid(axis="y", alpha=0.2)
    for i, value in enumerate(counts.values):
        ax.text(i, value + 0.3, str(value), ha="center")
    ax.text(
        0.01,
        -0.25,
        "Nilai kosong berkelompok pada bagian tabel sumber yang tidak menampilkan kolom-kolom tersebut.",
        transform=ax.transAxes,
        fontsize=8.5,
    )
    save(fig, folder / "missingness_kolom_status.png")

    fig, ax = plt.subplots(figsize=(8, 3.4), constrained_layout=True)
    ax.bar(["Baris sumber", "Rekaman unik"], [59, len(df)])
    ax.set(title="BAB IV — Dampak Deduplikasi Rekaman Identik", ylabel="Jumlah baris")
    ax.grid(axis="y", alpha=0.2)
    for i, value in enumerate([59, len(df)]):
        ax.text(i, value + 0.5, str(value), ha="center", weight="bold")
    ax.text(
        0.5,
        0.05,
        "Satu timestamp 20:51:43 tercatat identik pada Tabel 7 dan 8.",
        transform=ax.transAxes,
        ha="center",
        fontsize=8.5,
    )
    save(fig, folder / "dampak_deduplikasi.png")


def extended_chapter_v(df, out):
    folder = out / "bab_v"
    folder.mkdir(parents=True, exist_ok=True)
    cols = [c for c in NUMERIC_COLUMNS if c in df and df[c].notna().sum() > 2]
    fig, axes = plt.subplots(2, 4, figsize=(13, 7), constrained_layout=True)
    for ax, col in zip(axes.flat, cols):
        vals = df[col].dropna()
        ax.boxplot(vals, showmeans=True, meanline=True)
        ax.set_title(DISPLAY_LABELS.get(col, col), fontsize=9)
        ax.grid(axis="y", alpha=0.2)
    for ax in axes.flat[len(cols) :]:
        ax.remove()
    fig.suptitle(
        "BAB V — Sebaran Numerik dengan Median dan Mean", fontsize=14, weight="bold"
    )
    save(fig, folder / "boxplot_mean_median.png")

    fig, axes = plt.subplots(2, 4, figsize=(13, 7), constrained_layout=True)
    for ax, col in zip(axes.flat, cols):
        vals = np.sort(df[col].dropna().to_numpy())
        y = np.arange(1, len(vals) + 1) / len(vals)
        ax.step(vals, y, where="post")
        ax.set_title(col, fontsize=9)
        ax.set_ylim(0, 1.03)
        ax.grid(alpha=0.2)
        ax.set_ylabel("Proporsi kumulatif")
    for ax in axes.flat[len(cols) :]:
        ax.remove()
    fig.suptitle(
        "BAB V — Empirical Cumulative Distribution Function (ECDF)",
        fontsize=14,
        weight="bold",
    )
    save(fig, folder / "ecdf_variabel_numerik.png")

    moments = []
    for col in cols:
        vals = df[col].dropna()
        moments.append((col, vals.skew(), vals.kurt()))
    m = pd.DataFrame(moments, columns=["Variabel", "Skewness", "Excess kurtosis"])
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True)
    axes[0].barh(m["Variabel"], m["Skewness"])
    axes[0].axvline(0, color="black", lw=0.8)
    axes[0].set_title("Skewness")
    axes[0].grid(axis="x", alpha=0.2)
    axes[1].barh(m["Variabel"], m["Excess kurtosis"])
    axes[1].axvline(0, color="black", lw=0.8)
    axes[1].set_title("Excess kurtosis")
    axes[1].grid(axis="x", alpha=0.2)
    fig.suptitle("BAB V — Ringkasan Bentuk Distribusi", fontsize=14, weight="bold")
    save(fig, folder / "skewness_kurtosis.png")
    m.to_csv(folder / "ringkasan_momen_distribusi.csv", index=False)


def extended_chapter_vi(df, raw, out):
    folder = out / "bab_vi"
    folder.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 4.2), constrained_layout=True)
    ax.axis("off")
    ax.set_title(
        "BAB VI — Alur Konversi dan Rekayasa Fitur Aktual", fontsize=14, weight="bold"
    )
    nodes = [
        ("Raw CSV", "Teks dipertahankan\ntermasuk ---"),
        ("Analysis copy", "Salinan terpisah"),
        ("Datetime", "Date + Time → Timestamp"),
        ("Numerik", "Konversi nilai\n--- → missing"),
        ("Fitur waktu", "Elapsed seconds\nInterval aktual"),
        ("Validasi", "58 baris tetap\nTidak imputasi"),
    ]
    for i, (h, b) in enumerate(nodes):
        x = 0.025 + i * 0.163
        ax.text(
            x,
            0.62,
            h,
            transform=ax.transAxes,
            fontsize=8.5,
            weight="bold",
            bbox=dict(boxstyle="round,pad=.45", fc="#e8f1f8"),
        )
        ax.text(x, 0.34, b, transform=ax.transAxes, fontsize=8, va="center")
        if i < 5:
            ax.annotate(
                "",
                xy=(x + 0.15, 0.59),
                xytext=(x + 0.125, 0.59),
                xycoords=ax.transAxes,
                arrowprops=dict(arrowstyle="->"),
            )
    save(fig, folder / "alur_transformasi_aktual.png")

    cols = list(raw.columns)
    type_rows = []
    for c in cols:
        if c in ["Date", "Time"]:
            target = "datetime (gabungan)"
        elif c in NUMERIC_COLUMNS:
            target = "numerik"
        else:
            target = "kategori/teks"
        type_rows.append((c, str(raw[c].dtype), target))
    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
    ax.axis("off")
    tbl = ax.table(
        cellText=type_rows,
        colLabels=["Kolom", "Tipe raw CSV", "Perlakuan salinan analisis"],
        loc="center",
        cellLoc="left",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.scale(1, 1.35)
    ax.set_title(
        "BAB VI — Pemetaan Tipe Data dan Konversi", fontsize=14, weight="bold", pad=12
    )
    save(fig, folder / "pemetaan_tipe_dan_konversi.png")


def extended_chapter_vii(df, out):
    folder = out / "bab_vii"
    folder.mkdir(parents=True, exist_ok=True)
    x = df["Elapsed (s)"].to_numpy()
    intervals = df["Interval (s)"].fillna(1).to_numpy()
    panels = [
        ("Kecepatan (km/jam)", "Speed (km/h)"),
        ("Tekanan BP (psi)", "EAB BP (psi)"),
        ("Tekanan BC (psi)", "EAB BC (psi)"),
        ("Arus (ampere)", "Load (amps)"),
        ("Akselerasi (m/s²)", "Acceleration (m/sec²)"),
    ]
    fig, axes = plt.subplots(
        len(panels), 1, figsize=(13, 11), sharex=True, constrained_layout=True
    )
    for ax, (title, col) in zip(axes, panels):
        y = df[col].to_numpy(dtype=float)
        xx, yy = _break_lines(x, y, intervals)
        ax.plot(xx, yy, marker="o", ms=3, lw=1.4)
        _panel_title(ax, title)
        ax.set_ylabel(title, fontsize=8)
    axes[-1].set_xlabel("Detik sejak rekaman pertama (timestamp aktual)")
    axes[0].axvspan(9, 16, color="#e5a34b", alpha=0.12, label="Rentang gap sumber")
    axes[0].legend(loc="upper right", fontsize=8)
    fig.suptitle(
        "BAB VII — Multi-panel Perubahan Parameter terhadap Waktu",
        fontsize=15,
        weight="bold",
    )
    save(fig, folder / "multi_panel_parameter_waktu.png")

    state_cols = ["Throttle", "PCS Open", "IBS"]
    fig, axes = plt.subplots(
        3, 1, figsize=(13, 6.5), sharex=True, constrained_layout=True
    )
    for ax, col in zip(axes, state_cols):
        observed = df[col].notna()
        cats = df.loc[observed, col].astype(str)
        levels = {value: i for i, value in enumerate(sorted(cats.unique()))}
        observed_positions = np.flatnonzero(observed.to_numpy())
        for position in observed_positions:
            category = str(df.iloc[position][col])
            y_value = levels[category]
            ax.scatter(x[position], y_value, s=28, label=category)
            # Connect only adjacent source rows with a one-second interval
            # and an unchanged observed category. Missing rows remain gaps.
            if position > 0 and observed.iloc[position - 1]:
                previous = str(df.iloc[position - 1][col])
                if intervals[position] == 1 and previous == category:
                    ax.plot(
                        [x[position - 1], x[position]],
                        [levels[previous], y_value],
                        lw=2,
                        alpha=0.45,
                    )
        ax.set_yticks(list(levels.values()), labels=list(levels.keys()), fontsize=8)
        ax.set_ylabel(col, fontsize=9)
        ax.grid(axis="x", alpha=0.18)
    axes[-1].set_xlabel("Detik sejak rekaman pertama")
    fig.suptitle(
        "BAB VII — Timeline Observasi Kategori Status", fontsize=14, weight="bold"
    )
    fig.text(
        0.5,
        -0.015,
        "Titik = observasi pada timestamp sumber; bukan durasi status. "
        "Nilai kosong ditampilkan sebagai gap, bukan kategori.",
        ha="center",
        fontsize=8,
    )
    save(fig, folder / "categorical_state_timeline.png")

    pairs = [
        ("Speed (km/h)", "EAB BP (psi)"),
        ("Speed (km/h)", "EAB BC (psi)"),
        ("EAB BP (psi)", "EAB BC (psi)"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.3), constrained_layout=True)
    for ax, (a, b) in zip(axes, pairs):
        valid = df[[a, b, "Elapsed (s)"]].dropna()
        points = ax.scatter(
            valid[a], valid[b], c=valid["Elapsed (s)"], cmap="viridis", s=40
        )
        ax.set_xlabel(DISPLAY_LABELS.get(a, a))
        ax.set_ylabel(DISPLAY_LABELS.get(b, b))
        ax.set_title(
            f"{DISPLAY_LABELS.get(a, a)} vs {DISPLAY_LABELS.get(b, b)}",
            fontsize=9,
        )
        ax.grid(alpha=0.2)
    fig.colorbar(points, ax=axes, label="Detik sejak rekaman pertama")
    fig.suptitle(
        "BAB VII — Hubungan Bivariat Parameter Operasional", fontsize=14, weight="bold"
    )
    save(fig, folder / "scatter_hubungan_parameter.png")


def extended_chapter_viii(df, out):
    folder = out / "bab_viii"
    folder.mkdir(parents=True, exist_ok=True)
    cols = [
        "distance_to_stop_m",
        "Speed (km/h)",
        "Acceleration (m/sec²)",
        "Load (amps)",
        "EAB BP (psi)",
        "EAB BC (psi)",
    ]
    rows = []
    for c in cols:
        v = df[c].dropna()
        q1, q3 = v.quantile([0.25, 0.75])
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        rows.append((c, int(((v < lo) | (v > hi)).sum()), len(v), lo, hi))
    summary = pd.DataFrame(
        rows,
        columns=["Variabel", "Kandidat IQR", "n valid", "Batas bawah", "Batas atas"],
    )
    fig, ax = plt.subplots(figsize=(9, 4.2), constrained_layout=True)
    display_variables = summary["Variabel"].map(
        lambda value: DISPLAY_LABELS.get(value, value)
    )
    ax.barh(display_variables, summary["Kandidat IQR"])
    ax.set_xlabel("Jumlah kandidat menurut aturan IQR")
    ax.set_title("BAB VIII — Jumlah Kandidat Pencilan IQR per Variabel", weight="bold")
    ax.grid(axis="x", alpha=0.2)
    for i, value in enumerate(summary["Kandidat IQR"]):
        ax.text(value + 0.03, i, str(value), va="center")
    save(fig, folder / "jumlah_kandidat_iqr.png")

    fig, axes = plt.subplots(
        3, 1, figsize=(13, 8), sharex=True, constrained_layout=True
    )
    for ax, col in zip(axes, ["Speed (km/h)", "EAB BP (psi)", "EAB BC (psi)"]):
        y = df[col].to_numpy(dtype=float)
        xx, yy = _break_lines(
            df["Elapsed (s)"].to_numpy(), y, df["Interval (s)"].fillna(1).to_numpy()
        )
        ax.plot(xx, yy, marker="o", ms=3)
        ax.set_ylabel(col)
        ax.grid(alpha=0.2)
        _panel_title(ax, col)
    axes[-1].set_xlabel("Detik sejak rekaman pertama")
    fig.suptitle(
        "BAB VIII — Konteks Temporal Parameter yang Ditinjau",
        fontsize=14,
        weight="bold",
    )
    save(fig, folder / "konteks_temporal_parameter.png")


def extended_chapter_ix(df, raw, out):
    folder = out / "bab_ix"
    folder.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 3.4), constrained_layout=True)
    ax.axis("off")
    ax.set_title(
        "BAB IX — Matriks Kebutuhan Bukti untuk Analisis Lanjutan",
        fontsize=14,
        weight="bold",
    )
    rows = [
        [
            "Pertanyaan lanjutan",
            "Data tambahan yang dibutuhkan",
            "Status dalam dataset ini",
        ],
        [
            "Penyelarasan dua kereta",
            "Logger KA 5568A dan metadata jam",
            "Tidak tersedia",
        ],
        [
            "Aspek persinyalan",
            "Log interlocking, sinyal, konfigurasi perangkat",
            "Tidak tersedia",
        ],
        ["Komunikasi operasi", "Rekaman radio dan log komunikasi", "Tidak tersedia"],
        [
            "Respons pengereman",
            "Spesifikasi rangkaian, rem, massa, gradien",
            "Belum cukup",
        ],
        ["Konteks kejadian", "CCTV, kronologi, bukti lapangan", "Di luar dataset"],
    ]
    tbl = ax.table(cellText=rows[1:], colLabels=rows[0], loc="center", cellLoc="left")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.scale(1, 1.5)
    save(fig, folder / "decision_matrix_bukti_lanjutan.png")

    fig, ax = plt.subplots(figsize=(12, 3.8), constrained_layout=True)
    ax.axis("off")
    ax.set_title(
        "BAB IX — Ringkasan Cakupan dan Keterbatasan", fontsize=14, weight="bold"
    )
    items = [
        ("58", "rekaman unik"),
        ("16", "kolom"),
        ("59", "baris sumber"),
        ("6 s", "rentang timestamp hilang"),
        ("7", "placeholder akselerasi"),
        ("4", "kolom status tidak tersedia pada Tabel 9–10"),
    ]
    for i, (value, label) in enumerate(items):
        x = 0.035 + (i % 3) * 0.32
        y = 0.65 - (i // 3) * 0.42
        ax.text(
            x,
            y,
            value,
            transform=ax.transAxes,
            fontsize=20,
            weight="bold",
            bbox=dict(boxstyle="round,pad=.35", fc="#e8f1f8"),
        )
        ax.text(x, y - 0.15, label, transform=ax.transAxes, fontsize=8.5)
    save(fig, folder / "scorecard_keterbatasan.png")


def generate_extended_visuals(raw, df, out):
    extended_chapter_i(df, raw, out)
    extended_chapter_ii(df, raw, out)
    extended_chapter_iii(df, raw, out)
    extended_chapter_iv(df, raw, out)
    extended_chapter_v(df, out)
    extended_chapter_vi(df, raw, out)
    extended_chapter_vii(df, out)
    extended_chapter_viii(df, out)
    extended_chapter_ix(df, raw, out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    raw, df = load_data(args.input)
    out = args.output_dir
    chapter_i_scope(out)
    chapter_ii_source_coverage(df, out)
    chapter_iii_profile(raw, out)
    chapter_iv_missingness(raw, out)
    chapter_v_distributions(df, out)
    chapter_vi_temporal_feature(df, out)
    chapter_vii_visuals(df, out)
    chapter_viii_outliers(df, out)
    chapter_ix_findings(df, raw, out)
    generate_extended_visuals(raw, df, out)
    files = sorted(p for p in out.rglob("*") if p.is_file())
    print(f"Generated {len(files)} artifacts under {out}")
    for path in files:
        print(f"{path.relative_to(out)}\t{path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
