"""Interactive Streamlit companion for the transcribed KNKT Data Logger dataset."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed" / "data_logger_knkt_tabel_6_10.csv"

st.set_page_config(page_title="EDA Data Logger KNKT", page_icon="🚆", layout="wide")
st.title("EDA Data Logger KNKT — Bekasi Timur")
st.caption("Interactive exploration of transcribed Tables 6–10; not an accident-causation tool.")

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Timestamp"] = pd.to_datetime(
        df["Date"].astype(str) + " " + df["Time"].astype(str),
        dayfirst=True,
        errors="coerce",
    )
    return df

if not DATA.exists():
    st.error("Dataset tidak ditemukan. Pastikan CSV tersedia di data/processed/.")
    st.stop()

df = load_data(str(DATA))
st.warning(
    "Data yang ditampilkan adalah transkripsi tabel laporan KNKT, bukan ekspor mentah "
    "perangkat logger. Visualisasi tidak menyinkronkan kedua kereta dan tidak "
    "menetapkan sebab kecelakaan."
)

numeric_columns = [
    c for c in ["Speed (km/h)", "Load (amps)", "EAB BP (psi)", "EAB BC (psi)", "km", "m"]
    if c in df.columns
]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

with st.sidebar:
    st.header("Filter eksplorasi")
    variables = st.multiselect("Variabel numerik", numeric_columns, default=["Speed (km/h)"])
    start, end = st.select_slider(
        "Rentang waktu",
        options=df["Timestamp"].dropna().sort_values().tolist(),
        value=(df["Timestamp"].min(), df["Timestamp"].max()),
        format_func=lambda x: x.strftime("%H:%M:%S"),
    )
    category_columns = [c for c in ["Throttle", "PCS Open", "IBS"] if c in df.columns]
    selected_category = st.selectbox("Filter kategori", ["(Semua)"] + category_columns)
    selected_values = None
    if selected_category != "(Semua)":
        values = sorted(df[selected_category].dropna().astype(str).unique().tolist())
        selected_values = st.multiselect("Nilai kategori", values, default=values)

view = df[df["Timestamp"].between(start, end)].copy()
if selected_category != "(Semua)" and selected_values is not None:
    view = view[view[selected_category].astype(str).isin(selected_values)]

m1, m2, m3 = st.columns(3)
m1.metric("Rekaman ditampilkan", len(view))
m2.metric("Variabel dipilih", len(variables))
m3.metric("Timestamp unik", view["Timestamp"].nunique())

if variables:
    melted = view[["Timestamp", *variables]].melt(
        id_vars="Timestamp", var_name="Variabel", value_name="Nilai"
    )
    fig = px.line(
        melted, x="Timestamp", y="Nilai", color="Variabel", markers=True,
        title="Perubahan parameter terhadap waktu",
    )
    fig.update_layout(template="plotly_white", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Pilih minimal satu variabel numerik pada panel filter.")

st.subheader("Tabel rekaman terfilter")
st.dataframe(view, use_container_width=True, hide_index=True)
st.download_button(
    "Unduh hasil filter (CSV)",
    data=view.to_csv(index=False).encode("utf-8-sig"),
    file_name="data_logger_knkt_filtered.csv",
    mime="text/csv",
)

st.subheader("Korelasi Spearman")
if len(numeric_columns) >= 2:
    corr = view[numeric_columns].corr(method="spearman", min_periods=3)
    heat = px.imshow(
        corr, text_auto=".2f", zmin=-1, zmax=1, aspect="auto",
        color_continuous_scale="Viridis",
        title="Korelasi antarvariabel numerik",
    )
    st.plotly_chart(heat, use_container_width=True)
else:
    st.info("Variabel numerik belum cukup untuk menghitung korelasi.")
