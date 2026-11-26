# Audit Transkripsi Data Logger terhadap PDF KNKT

## Status

**Audit visual sumber selesai; satu kesalahan transkripsi ditemukan dan dikoreksi.**

- Sumber primer: *Laporan Akhir KNKT.26.04.03.02*, Tabel 6–10.
- Halaman tercetak: 65–68.
- Halaman PDF: 75–78 pada salinan PDF yang diaudit.
- Berkas yang diaudit: `data/processed/data_logger_knkt_tabel_6_10.csv`.
- Cakupan dataset gabungan: 58 rekaman unik × 16 kolom = **928 sel**.

## Metode pemeriksaan

1. Membuka halaman PDF sumber 75–78 dan merender halaman tabel pada resolusi 300 dpi.
2. Membaca setiap baris pada Tabel 6, 7, 8, 9, dan 10 secara visual; OCR dipakai sebagai pemeriksaan bantu, bukan pengganti pemeriksaan visual.
3. Mencocokkan tanggal, waktu, seluruh nilai numerik, kategori, placeholder `---`, dan sel kosong dengan CSV pada branch audit.
4. Memeriksa tumpang tindih timestamp antartabel. Rekaman 20:51:43 tercantum di Tabel 7 dan Tabel 8 dengan nilai identik; satu salinan dipertahankan pada dataset gabungan.
5. Memastikan kolom yang tidak ditampilkan pada Tabel 9–10 tetap kosong pada CSV gabungan, bukan diisi dengan nilai hasil asumsi.

## Rekonsiliasi jumlah baris

| Tabel sumber | Halaman tercetak | Jumlah baris sumber |
|---|---:|---:|
| Tabel 6 | 65 | 10 |
| Tabel 7 | 65 | 10 |
| Tabel 8 | 66 | 13 |
| Tabel 9 | 67 | 14 |
| Tabel 10 | 68 | 12 |
| **Total baris tabel** | | **59** |
| Duplikasi identik 20:51:43 pada Tabel 7 dan 8 | | **−1** |
| **Dataset gabungan** | | **58** |

58 rekaman unik dikalikan 16 kolom menghasilkan 928 posisi sel yang diperiksa. Kolom kosong struktural dan placeholder literal termasuk dalam cakupan.

## Temuan dan koreksi

| Timestamp | Tabel / halaman | Kolom | Nilai di CSV awal | Nilai pada PDF | Tindakan |
|---|---|---|---:|---:|---|
| 20:51:36 | Tabel 7 / 65 (PDF 75) | Load (amps) | 168 | **160** | Dikoreksi menjadi 160 |

Pemeriksaan visual pada baris 20:51:36 menunjukkan nilai Load 160 A. Pembacaan OCR atas tabel yang sama juga menghasilkan 160. Nilai 168 pada CSV awal dan workbook transkripsi sebelumnya tidak sesuai dengan citra tabel sumber.

Tidak ditemukan ketidaksesuaian nilai lain dalam pencocokan visual seluruh baris Tabel 6–10. Nilai `---` pada akselerasi Tabel 10 dipertahankan sebagai placeholder literal; kolom `DB Excit`, `Dir Call`, `DB Set`, dan `DB Star` yang tidak tersedia di Tabel 9–10 tetap kosong.

## Dampak terhadap analisis

Koreksi satu nilai Load (amps) mengubah satu sel sumber dari 168 menjadi 160. Karena variabel Load dipakai dalam statistik deskriptif, korelasi, dan IQR, seluruh output turunan harus dihitung ulang dari CSV yang telah dikoreksi. Pipeline CI menjalankan notebook secara berurutan dan tes regresi untuk memastikan keluaran konsisten dengan dataset terbaru.

## Artefak dan batas audit

- Dataset terkoreksi: `data/processed/data_logger_knkt_tabel_6_10.csv`.
- Golden snapshot diperbarui setelah pencocokan PDF: `tests/fixtures/data_logger_knkt_tabel_6_10_expected.csv`.
- Tes spesifik untuk nilai sumber 20:51:36 ditambahkan ke `tests/test_bab_ix_audit.py`.
- Golden snapshot merupakan baseline regresi setelah audit sumber ini; bukan sumber pembanding independen itu sendiri.

Audit ini memverifikasi transkripsi tabel yang terlihat pada halaman PDF tersebut. Audit ini tidak memverifikasi data mentah perangkat logger, tidak mengisi timestamp yang tidak disajikan, dan tidak mengubah batas interpretasi semantik kolom `km` dan `m`.
