# Presentasi EDA KNKT — Quarto + reveal.js

Sumber presentasi tunggal berada di `eda-knkt-bekasi-timur.qmd`. Dari sumber ini dibangun:

- HTML reveal.js untuk presentasi interaktif.
- PDF landscape untuk distribusi dan arsip akademik.

## Build lokal

Prasyarat: Quarto CLI, Node.js, npm, dan Chromium yang dikelola Playwright.

```bash
cd presentations
quarto render eda-knkt-bekasi-timur.qmd
npm install --no-save --package-lock=false playwright@1.56.1
npx playwright install --with-deps chromium
node scripts/export-pdf.mjs
python scripts/validate_outputs.py
```

Keluaran ada di `presentations/dist/`:

- `eda-knkt-bekasi-timur.html`
- `eda-knkt-bekasi-timur.pdf`

## Identitas visual: PT KAI Academic

Tema presentasi mengikuti palet yang ditetapkan: biru tua `#323A70`, putih `#FFFFFF`, dan oranye `#ED6B23`, dengan Georgia sebagai tipografi utama. Slide pembuka menggunakan latar biru tua; slide isi menggunakan latar putih. Implementasi tema berada di `styles/knkt-theme.scss` dalam format SCSS untuk Reveal.js.

## Prinsip pemeliharaan

- Edit konten hanya pada berkas QMD dan tema SCSS.
- Jangan mengedit HTML/PDF hasil render secara manual.
- Visual merujuk ke snapshot analisis yang telah dilacak di `outputs/`.
- Klaim data dibatasi pada transkripsi Tabel 6–10 (58 rekaman unik × 16 kolom).
- Jangan mengubah batasan sumber, semantik jarak, atau interpretasi timestamp tanpa memperbarui audit dan laporan induk.

Workflow GitHub Actions membangun kedua keluaran dan mengunggahnya sebagai artifact; workflow tidak melakukan commit otomatis dan tidak menerbitkan ke GitHub Pages.
