# EDA Data Logger KNKT - Bekasi Timur

[![CI](https://github.com/mznasyiith/eda-data-logger-knkt-bekasi-timur/actions/workflows/ci.yml/badge.svg)](https://github.com/mznasyiith/eda-data-logger-knkt-bekasi-timur/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Proyek akademik **Exploratory Data Analysis (EDA)** terhadap rekaman *Data Logger* yang dirujuk dalam Laporan Investigasi Kecelakaan Perkeretaapian KNKT Nomor **KNKT.26.04.03.02**, mengenai tabrakan KA 4B Argo Bromo Anggrek dan KA 5568A Commuter Line di Stasiun Bekasi Timur pada 27 April 2026.

> **Status:** kerangka proyek / bootstrap. Dataset belum disertakan. Hasil analisis dan jumlah kolom harus diverifikasi menggunakan berkas data aktual sebelum dinyatakan final.

## Tujuan

1. Mendokumentasikan asal-usul, struktur, dan batasan data.
2. Memeriksa kualitas dan karakteristik rekaman Data Logger.
3. Melakukan pembersihan dan transformasi secara transparan.
4. Menghasilkan statistik deskriptif dan visualisasi eksploratif.
5. Menyajikan temuan yang dapat ditelusuri dan direproduksi.

## Cakupan analisis

Proyek ini berfokus pada EDA, bukan penetapan penyebab kecelakaan, penilaian tanggung jawab, atau pembuktian kausalitas. Analisis dibatasi pada variabel dan rentang rekaman yang benar-benar tersedia. Korelasi tidak ditafsirkan sebagai sebab-akibat.

## Struktur repository

```text
.
├── data/                 # raw, interim, processed, external (data tidak di-commit)
├── docs/                 # konteks masalah, data, metodologi, keputusan, panduan
├── notebooks/            # tahapan kerja EDA berurutan
├── outputs/              # grafik, tabel, statistik, validasi
├── reports/              # laporan akademik dan teknis
├── src/eda_knkt/         # modul Python yang dapat digunakan ulang
├── tests/                # pengujian otomatis
├── pyproject.toml
└── requirements.txt
```

Rincian: [Panduan struktur repository](docs/repository_guide/project_structure.md).

## Persiapan lingkungan

Disarankan Python 3.10 atau lebih baru.

```bash
git clone https://github.com/mznasyiith/eda-data-logger-knkt-bekasi-timur.git
cd eda-data-logger-knkt-bekasi-timur
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

Jalankan notebook secara berurutan menggunakan Jupyter:

```bash
jupyter lab
```

## Modul Python

Modul di `src/eda_knkt/` menyediakan fungsi reusable untuk tahapan EDA:

| Modul | Tanggung jawab |
|---|---|
| `config.py` | Lokasi direktori proyek dan data |
| `ingestion.py` | Memuat berkas CSV dan Excel |
| `validation.py` | Memeriksa dimensi, nama kolom, tipe data, dan nilai hilang |
| `cleaning.py` | Operasi pembersihan yang eksplisit dan non-destruktif |
| `transformation.py` | Konversi numerik/datetime, pengurutan, dan pemilihan kolom |
| `statistics.py` | Statistik deskriptif, ringkasan kategorikal, bentuk distribusi, dan korelasi |
| `visualization.py` | Histogram, frekuensi kategori, scatter plot, dan heatmap korelasi |
| `reporting.py` | Ekspor tabel CSV, grafik, dan laporan Markdown |

Fungsi transformasi dan pembersihan mengembalikan salinan data; pemilihan kolom serta aturan konversi harus ditentukan berdasarkan kamus data yang telah diverifikasi. Modul statistik dan visualisasi tidak menetapkan arti atau satuan variabel secara otomatis.

## Urutan notebook

| Notebook | Tahap |
|---|---|
| 00 | Project setup |
| 01 | Problem understanding |
| 02 | Data understanding |
| 03 | Importing and inspecting |
| 04 | Handling missing data |
| 05 | Exploring characteristics |
| 06 | Data transformation |
| 07 | Visualizing relationships |
| 08 | Handling outliers |
| 09 | Findings and insights |

Notebook 00–09 berisi urutan kerja, penjelasan metodologis, dan sel kode yang dapat dijalankan setelah dataset aktual tersedia. Seluruh hasil numerik, interpretasi, serta temuan harus dihasilkan dari data yang telah diverifikasi; repository ini tidak menyertakan dataset.

## Kebijakan data dan hak penggunaan

- Berkas PDF laporan KNKT dan dataset hasil ekstraksi **tidak disertakan** dalam repository ini.
- Jangan mengunggah data sumber sebelum hak akses dan distribusinya dipastikan.
- Simpan data lokal pada direktori `data/raw/`; direktori data diabaikan Git melalui `.gitignore`.
- Jangan memasukkan data pribadi, kredensial, atau informasi yang tidak relevan.
- Lisensi MIT pada repository hanya ditujukan untuk kode dan dokumentasi orisinal proyek, bukan untuk materi pihak ketiga.

Baca [Kebijakan hak data](docs/DATA_RIGHTS.md) sebelum menambahkan berkas.

## Reproducibility dan kualitas

Setiap perubahan data harus dapat ditelusuri. Data mentah dipertahankan tanpa modifikasi; pembersihan dilakukan pada salinan kerja. Nilai kosong seperti `---` tidak boleh otomatis dianggap nol. Outlier tidak dihapus hanya karena nilainya ekstrem. Keputusan analisis dicatat pada [analysis decisions](docs/decisions/analysis_decisions.md).

## Pengujian

```bash
pytest
```

## Identitas akademik

- Penyusun: Muhammad Za'iimun Nasyiith
- NIM: 26MA41D002
- Program: Magister Ilmu Komputer
- Institusi: Universitas Amikom Purwokerto

## Lisensi

Kode dan dokumentasi orisinal dilisensikan di bawah MIT License. Ketentuan untuk sumber data pihak ketiga tetap berlaku. Lihat [LICENSE](LICENSE).
