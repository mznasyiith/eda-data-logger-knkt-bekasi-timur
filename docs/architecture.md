# Arsitektur Sistem Analisis

~~~~mermaid
flowchart TD
    A["Sumber KNKT: Tabel 6–10"] --> B["Transkripsi CSV"]
    B --> C["Ingestion"]
    C --> D["Validasi skema, timestamp, missingness"]
    D --> E["Transformasi non-destruktif"]
    E --> F["Statistik deskriptif dan korelasi"]
    E --> G["Visualisasi statis, GIF, Plotly"]
    F --> H["Tabel ringkasan / outputs"]
    G --> H
    H --> I["Laporan dan README"]
    J["pytest + Ruff + Black"] -. "validasi otomatis" .-> C
    J -.-> D
    J -.-> E
~~~~

## Prinsip arsitektur

- Input immutable: berkas sumber tidak ditimpa.
- Transformasi eksplisit: setiap konversi dilakukan pada salinan.
- Notebook mengorkestrasi narasi; fungsi reusable berada di src/eda_knkt/.
- Grafik dan tabel hasil proses disimpan di outputs/.
- Pengujian otomatis memeriksa aturan integritas yang telah ditetapkan.
- Tidak ada klaim sinkronisasi antar-kereta atau sebab kecelakaan tanpa bukti tambahan.
