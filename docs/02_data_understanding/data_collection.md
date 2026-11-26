# Pengumpulan Data

## Sumber primer

Sumber acuan adalah Laporan Akhir Investigasi KNKT Nomor KNKT.26.04.03.02, khususnya Tabel 6–10 pada halaman tercetak 65–68 (halaman PDF 75–78). Dokumen resmi tersedia melalui [situs KNKT](https://laman.knkt.go.id/Repo/Files/Laporan/Perkeretaapian/2026/KNKT.26.04.03.02-Final-Report.pdf).

## Metode dan cakupan

Dataset repository merupakan transkripsi manual dari tabel yang dicetak dalam PDF, bukan berkas biner logger atau ekspor asli perangkat Data Logger. Jumlah baris per tabel adalah 10, 10, 13, 14, dan 12 (total 59 baris sumber). Satu rekaman identik pada 20:51:43 muncul di Tabel 7 dan Tabel 8; setelah deduplikasi berdasarkan seluruh isi rekaman, CSV analitis memuat 58 rekaman unik × 16 kolom.

Rentang waktu CSV adalah 27/04/2026 20:51:18 sampai 20:52:21. Terdapat gap timestamp 20:51:28–20:51:33; tidak dilakukan interpolasi. Tujuh placeholder `---` pada akselerasi dipertahankan pada CSV mentah. Empat kolom status yang tidak disajikan pada Tabel 9–10 memiliki 26 sel kosong per kolom.

## Aturan semantik jarak

Kolom `km` dan `m` merupakan komponen satu besaran jarak tersisa menuju titik henti akhir, bukan dua variabel independen atau chainage absolut. Pada salinan analisis, keduanya digabung sebagai `distance_to_stop_m = km * 1000 + m`. Kolom mentah tetap dipertahankan. Beberapa uraian chainage pada PDF tidak konsisten; proyek tidak merekonstruksi chainage absolut. Bukti dan keputusan rinci terdapat pada [verifikasi semantik jarak](source_validation_distance.md).

## Keterlacakan dan batas verifikasi

CSV tersedia pada `data/processed/data_logger_knkt_tabel_6_10.csv`. Workbook transkripsi per sumber dan salinan PDF tidak disertakan di repository pada saat pemeriksaan. Karena itu, 59 baris sumber dapat dihitung dari tabel KNKT dan keputusan deduplikasi didokumentasikan, tetapi audit independen terhadap lembar kerja transkripsi per sumber belum dapat dilakukan hanya dari repository ini. Setiap koreksi sel harus dicatat dengan nomor tabel, halaman, timestamp, nilai sebelum/sesudah, dan bukti sumber.

Tanggal pemeriksaan sumber: 26 November 2026. Simpan checksum SHA-256 untuk setiap berkas dataset yang digunakan pada rilis analisis; jangan menganggap checksum CSV sebagai checksum PDF sumber.
