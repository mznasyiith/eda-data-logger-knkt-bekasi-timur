# Matriks Penyelarasan Laporan, Notebook, Kode, Visualisasi, dan Pengujian

Dokumen ini menjadi acuan tunggal untuk menjaga konsistensi laporan UTS, notebook, modul Python, artefak visual, dan pengujian pada repositori.

## Prinsip

1. Urutan laporan mengikuti sembilan bab EDA yang disepakati.
2. Notebook bernomor 01–09 menjadi demonstrasi analisis per bab; notebook 00 khusus penyiapan proyek.
3. Fungsi yang dapat digunakan ulang ditempatkan di `src/eda_knkt/`; notebook berperan sebagai narasi dan pemanggil fungsi, bukan salinan implementasi.
4. Data sumber/transkripsi tidak ditimpa. Transformasi dan fitur turunan harus dapat ditelusuri.
5. Grafik hanya menggambarkan rekaman yang tersedia. Tidak boleh diberi label sebagai simulasi fisik atau rekonstruksi kausal.
6. Setiap klaim kuantitatif dalam laporan harus dapat ditelusuri ke notebook, kode, dataset, atau hasil pengujian.

## Matriks sembilan bab

| Bab laporan UTS | Notebook utama | Modul/kode pendukung | Dokumentasi/artefak | Pengujian terkait |
|---|---|---|---|---|
| I. Pendahuluan dan Pemahaman Permasalahan | `notebooks/01_problem_understanding.ipynb` | `src/eda_knkt/config.py` | `docs/01_problem_understanding/problem_statement.md`; `objectives_scope.md` | Pemeriksaan ruang lingkup dan asumsi secara review; bukan uji statistik otomatis |
| II. Memahami Data | `notebooks/02_data_understanding.ipynb` | `src/eda_knkt/ingestion.py`; `config.py` | `docs/02_data_understanding/data_collection.md`; `data_dictionary.md`; `data_quality_plan.md`; `data/processed/README.md` | `tests/test_dataset_integrity.py`; `tests/test_validation.py` |
| III. Memuat dan Memeriksa Data | `notebooks/03_importing_and_inspecting.ipynb` | `ingestion.py`; `validation.py` | Dataset `data/processed/data_logger_knkt_tabel_6_10.csv` | `tests/test_dataset_integrity.py`; `tests/test_validation.py`; `tests/test_notebooks.py` |
| IV. Penilaian dan Penanganan Kualitas Data | `notebooks/04_handling_missing_data.ipynb` | `cleaning.py`; `validation.py` | `docs/02_data_understanding/data_quality_plan.md`; `docs/decisions/analysis_decisions.md` | `tests/test_cleaning.py`; `tests/test_dataset_integrity.py` |
| V. Eksplorasi Karakteristik Data | `notebooks/05_exploring_characteristics.ipynb` | `statistics.py` | Tabel statistik deskriptif dan distribusi pada notebook/laporan | `tests/test_statistics.py` |
| VI. Transformasi dan Rekayasa Fitur | `notebooks/06_data_transformation.ipynb` | `transformation.py`; `cleaning.py` | `docs/decisions/analysis_decisions.md` | `tests/test_transformation.py` |
| VII. Visualisasi dan Analisis Hubungan Antarvariabel | `notebooks/07_visualizing_relationships.ipynb` | `visualization.py`; `statistics.py`; `scripts/generate_visuals.py` | `outputs/` (GIF, PNG, HTML setelah generator dijalankan) | `tests/test_visualization.py`; `tests/test_notebooks.py` |
| VIII. Deteksi Pencilan dan Analisis Anomali | `notebooks/08_handling_outliers.ipynb` | `statistics.py`; `validation.py` | `docs/decisions/analysis_decisions.md` | `tests/test_statistics.py`; `tests/test_validation.py` |
| IX. Kesimpulan, Temuan, dan Rekomendasi | `notebooks/09_findings_and_insights.ipynb` | `reporting.py`; seluruh modul analisis yang relevan | `reports/Laporan_EDA_KNKT_Bekasi_Timur.md`; README | `tests/test_reporting.py`; `tests/test_notebooks.py` |

### Notebook 00

`notebooks/00_project_setup.ipynb` adalah notebook pendukung untuk konfigurasi lingkungan, lokasi proyek, dan persiapan analisis. Notebook ini tidak dihitung sebagai bab laporan.

## Pemetaan keluaran visual

| Keluaran | Sumber pembentukan | Bab laporan |
|---|---|---|
| Histogram, KDE, box plot, ringkasan distribusi | Notebook 05 dan fungsi statistik/visualisasi | V |
| Grafik kecepatan terhadap waktu | Notebook 07 dan `scripts/generate_visuals.py` | VII |
| Heatmap korelasi Spearman | Notebook 07 dan `scripts/generate_visuals.py` | VII |
| Grafik interaktif Plotly | `scripts/generate_visuals.py` | VII |
| GIF urutan rekaman kecepatan | `scripts/generate_visuals.py` | VII |
| Grafik pencilan dan nilai ekstrem | Notebook 08 | VIII |

Nama file keluaran aktual harus diperiksa pada direktori `outputs/` setelah generator berhasil dijalankan. Jangan menuliskan bahwa artefak tersedia jika belum terbentuk.

## Pemetaan pengujian

- `test_dataset_integrity.py`: dimensi, nama/struktur kolom, placeholder, missingness, duplikasi, dan kesenjangan waktu yang diketahui.
- `test_validation.py`: aturan validasi data.
- `test_cleaning.py`: perilaku pembersihan data.
- `test_statistics.py`: fungsi statistik.
- `test_transformation.py`: transformasi dan fitur turunan.
- `test_visualization.py`: fungsi visualisasi.
- `test_reporting.py`: pembentukan ringkasan/laporan.
- `test_notebooks.py`: pemeriksaan notebook.

Status lulus/gagal harus diambil dari hasil eksekusi `pytest` atau GitHub Actions pada commit yang disebutkan. Keberadaan file pengujian bukan bukti bahwa seluruh pengujian telah lulus.

## Aturan konsistensi akademik

1. Gunakan istilah **data transkripsi Tabel 6–10**; jangan menyebutnya ekspor mentah perangkat logger.
2. Bedakan 59 baris sumber dengan 58 rekaman unik setelah penggabungan.
3. Pertahankan tujuh placeholder `---` pada kolom akselerasi sebagai nilai yang tidak tersedia, bukan nol.
4. Jelaskan 26 nilai kosong pada masing-masing kolom `DB Excit`, `Dir Call`, `DB Set`, dan `DB Star` sebagai missingness yang berkaitan dengan cakupan tabel sumber, sesuai bukti yang tersedia.
5. Jangan mengisi celah timestamp 20:51:28–20:51:33 dengan interpolasi.
6. Jangan menyimpulkan sebab-akibat dari korelasi atau menyebut pencilan statistik sebagai kegagalan operasional tanpa bukti pendukung.
7. Jangan memaksakan imputasi, scaling, encoding, atau model prediktif jika tidak dibutuhkan oleh tujuan EDA.
8. Setiap tabel/gambar di laporan diberi nomor, judul, satuan, sumber, dan rujukan pembahasan.

## Checklist sebelum pengumpulan UTS

- [ ] Semua sembilan bab laporan mengikuti judul dan ruang lingkup pada matriks ini.
- [ ] Setiap bab memiliki notebook yang sesuai.
- [ ] Kode reusable berada di `src/eda_knkt/`.
- [ ] Seluruh notebook dijalankan ulang dari awal tanpa error.
- [ ] Dataset yang dibaca notebook sama dengan dataset yang dirujuk laporan.
- [ ] Grafik pada laporan berasal dari keluaran kode/notebook yang dapat direproduksi.
- [ ] Angka statistik pada laporan cocok dengan hasil notebook.
- [ ] `pytest` berhasil pada commit final.
- [ ] Status GitHub Actions dicatat berdasarkan run final.
- [ ] Laporan menyatakan keterbatasan dan tidak mengklaim temuan investigasi kausal.
- [ ] README, laporan, dan presentasi menggunakan angka dataset serta istilah yang sama.
