# Reproducibility

## Environment and installation

- Python minimum yang dideklarasikan: 3.10; CI release gate saat ini berjalan pada Python 3.11.
- Metadata dependensi kanonis berada pada `pyproject.toml`.
- Instalasi analisis dan pengembangan: `pip install -e ".[dev]"`.
- Instalasi portal Streamlit: `pip install -r requirements-streamlit.txt`.
- `requirements.txt` disediakan sebagai daftar dependensi runtime tambahan, bukan lockfile.
- Dependensi menggunakan batas versi minimum, bukan versi exact. Repository belum memiliki lockfile/constraints yang mengunci seluruh dependensi transitif; karena itu instalasi pada tanggal berbeda dapat menghasilkan versi paket berbeda.

## Pipeline reproduksi

1. Checkout commit SHA yang hendak direproduksi.
2. Buat virtual environment Python bersih.
3. Instal dependensi dari metadata proyek.
4. Jalankan notebook berurutan dengan perintah CI.
5. Jalankan `python scripts/generate_visuals.py`.
6. Jalankan `pytest`.
7. Bandingkan keluaran dengan artifact CI pada SHA yang sama.

Contoh:

```bash
python -m venv .venv
python -m pip install --upgrade pip
pip install -e ".[dev]"
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=180 --output-dir /tmp/eda-executed notebooks/*.ipynb
python scripts/generate_visuals.py
pytest
```

## CI, keamanan, dan artefak

- Workflow CI menggunakan izin token minimum `contents: read`.
- GitHub Actions utama dipatok ke commit SHA, bukan tag bergerak.
- CI menjalankan `pip check` dan `pip-audit --skip-editable` untuk memeriksa dependensi lingkungan.
- Dependabot memeriksa pembaruan ekosistem pip dan GitHub Actions setiap minggu.
- Artifact visual diunggah dari runner; workflow tidak melakukan commit otomatis ke branch.
- Snapshot `outputs/` yang terlacak adalah artefak yang dikomit. Artifact CI merupakan keluaran regenerasi pada commit dan lingkungan tertentu.

## Data dan provenance

- CSV kanonis: `data/processed/data_logger_knkt_tabel_6_10.csv`.
- Dataset merupakan transkripsi Tabel 6–10 PDF KNKT, bukan ekspor mentah perangkat logger.
- PDF sumber dan workbook transkripsi eksternal tidak disertakan di repository. Pembaca perlu memperoleh sumber dari situs KNKT dan memeriksa halaman/tabel yang dirujuk.
- Golden snapshot menguji regresi terhadap baseline repositori; bukan sumber independen untuk membuktikan transkripsi.

## Batas reproduksibilitas saat ini

Reproduksi logika analisis dan pembuatan visual telah diuji di CI Python 3.11. Reproduksi bit-for-bit lintas waktu/platform belum dijamin karena belum ada lockfile penuh, dan sumber PDF/workbook tidak disimpan di repository. Untuk rilis yang menuntut reproduksi byte-identik, tambahkan lockfile beserta checksum PDF sumber dan metadata lingkungan.
