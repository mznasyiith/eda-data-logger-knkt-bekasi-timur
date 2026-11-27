# Presentasi EDA KNKT — Quarto + reveal.js

Sumber presentasi tunggal berada di `eda-knkt-bekasi-timur.qmd`. Dari sumber ini dibangun:

- HTML reveal.js untuk presentasi interaktif.
- PDF landscape untuk distribusi dan arsip akademik.
- PowerPoint (`.pptx`) untuk penyuntingan lanjutan di Microsoft PowerPoint atau aplikasi kompatibel.

## Build lokal

Prasyarat: Quarto CLI, Node.js, npm, Python 3 + Pillow, Poppler utilities (`pdfinfo`, `pdftotext`, `pdftoppm`), dan Chromium yang dikelola Playwright.

```bash
# Render HTML dari direktori presentasi
cd presentations
quarto render eda-knkt-bekasi-timur.qmd
cd ..

# Instal tooling PDF dan jalankan ekspor/validasi dari root repositori
sudo apt-get install --yes poppler-utils python3-pil
npm install --no-save --package-lock=false playwright@1.56.1
npx playwright install --with-deps chromium
node presentations/scripts/export-pdf.mjs
cd presentations
quarto render eda-knkt-bekasi-timur.qmd --to pptx --output eda-knkt-bekasi-timur.pptx
cd ..
python presentations/scripts/validate_outputs.py
```

Keluaran ada di `presentations/dist/`:

- `eda-knkt-bekasi-timur.html`
- `eda-knkt-bekasi-timur.pdf`
- `eda-knkt-bekasi-timur.pptx`

## Identitas visual: PT KAI Academic

Tema presentasi mengikuti palet yang ditetapkan: biru tua `#174B78`, putih lembut `#F7F8FA`, dan aksen oranye `#F28C28` / `#ED6B23`, dengan Georgia sebagai tipografi utama. Slide pembuka menggunakan latar biru tua; slide isi menggunakan latar putih. Implementasi tema berada di `styles/knkt-theme.scss` dalam format SCSS untuk Reveal.js.

## Prinsip pemeliharaan

- Edit konten hanya pada berkas QMD dan tema SCSS.
- Jangan mengedit HTML/PDF hasil render secara manual.
- Visual merujuk ke snapshot analisis yang telah dilacak di `outputs/`.
- Klaim data dibatasi pada transkripsi Tabel 6–10 (58 rekaman unik × 16 kolom).
- Jangan mengubah batasan sumber, semantik jarak, atau interpretasi timestamp tanpa memperbarui audit dan laporan induk.

Workflow GitHub Actions membangun ketiga keluaran dan mengunggahnya sebagai artifact; workflow tidak melakukan commit otomatis dan tidak menerbitkan ke GitHub Pages.
