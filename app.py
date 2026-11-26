"""Interactive Streamlit companion for the transcribed KNKT Data Logger dataset."""
from pathlib import Path

import plotly.express as px
import streamlit as st

from eda_knkt.dashboard import (
    DASHBOARD_NUMERIC_COLUMNS,
    load_dashboard_data,
    prepare_timeseries_plot_data,
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed" / "data_logger_knkt_tabel_6_10.csv"

st.set_page_config(page_title="EDA Data Logger KNKT", page_icon="🚆", layout="wide")
st.title("EDA Data Logger KNKT — Bekasi Timur")
st.caption(
    "Interactive exploration of transcribed Tables 6–10; "
    "not an accident-causation tool."
)


@st.cache_data
def load_data(path: str):
    return load_dashboard_data(path)


if not DATA.exists():
    st.error("Dataset tidak ditemukan. Pastikan CSV tersedia di data/processed/.")
    st.stop()

df = load_data(str(DATA))
st.warning(
    "Data yang ditampilkan adalah transkripsi Tabel 6–10 dalam laporan KNKT, "
    "bukan ekspor mentah perangkat logger. Enam timestamp 20:51:28–20:51:33 "
    "tidak termasuk dalam subset Tabel 6–10, meskipun tercantum pada Lampiran 7. "
    "Lampiran 7 juga memuat empat kolom status yang kosong pada 26 baris subset ini. "
    "Visualisasi tidak menyinkronkan kedua kereta dan tidak menetapkan sebab kecelakaan."
)

with st.sidebar:
    st.header("Filter eksplorasi")
    variables = st.multiselect(
        "Variabel numerik",
        DASHBOARD_NUMERIC_COLUMNS,
        default=["Speed (km/h)"],
    )
    start, end = st.select_slider(
        "Rentang waktu",
        options=df["Timestamp"].tolist(),
        value=(df["Timestamp"].min(), df["Timestamp"].max()),
        format_func=lambda value: value.strftime("%H:%M:%S"),
    )
    category_columns = [
        column for column in ["Throttle", "PCS Open", "IBS"] if column in df.columns
    ]
    selected_category = st.selectbox(
        "Filter kategori", ["(Semua)"] + category_columns
    )
    selected_values = None
    if selected_category != "(Semua)":
        values = sorted(
            df[selected_category].dropna().astype(str).unique().tolist()
        )
        selected_values = st.multiselect(
            "Nilai kategori", values, default=values
        )

view = df[df["Timestamp"].between(start, end)].copy()
if selected_category != "(Semua)" and selected_values is not None:
    view = view[view[selected_category].astype(str).isin(selected_values)]

m1, m2, m3 = st.columns(3)
m1.metric("Rekaman ditampilkan", len(view))
m2.metric("Variabel dipilih", len(variables))
m3.metric("Timestamp unik", view["Timestamp"].nunique())

if variables:
    plot_data = prepare_timeseries_plot_data(view, variables)
    fig = px.line(
        plot_data,
        x="Timestamp",
        y="Nilai",
        color="Variabel",
        facet_row="Variabel",
        markers=True,
        category_orders={"Variabel": variables},
        title="Perubahan parameter terhadap waktu (panel dan skala per variabel)",
        height=max(320, 250 * len(variables)),
    )
    fig.update_layout(template="plotly_white", hovermode="x unified")
    fig.update_traces(connectgaps=False)
    fig.update_yaxes(matches=None)
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Setiap variabel memakai panel dan skala vertikal sendiri karena satuannya "
        "berbeda. Garis diputus pada jeda lebih dari satu detik; tidak ada interpolasi."
    )
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
if len(view) >= 3:
    corr = view[DASHBOARD_NUMERIC_COLUMNS].corr(method="spearman", min_periods=3)
    if corr.notna().any().any():
        heat = px.imshow(
            corr,
            text_auto=".2f",
            zmin=-1,
            zmax=1,
            aspect="auto",
            color_continuous_scale="Viridis",
            title="Korelasi Spearman antarvariabel analitis",
        )
        st.plotly_chart(heat, use_container_width=True)
    else:
        st.info("Belum ada pasangan variabel dengan sedikitnya tiga observasi valid.")
    st.caption(
        "km dan m tidak dianalisis terpisah; keduanya digabung sebagai "
        "distance_to_stop_m. Korelasi bersifat deskriptif dan bukan kausal."
    )
else:
    st.info("Pilih kategori/rentang yang menyisakan sedikitnya tiga rekaman untuk korelasi.")
