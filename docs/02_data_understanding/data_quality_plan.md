# Rencana dan Status Pemeriksaan Kualitas Data

Dokumen ini mencatat pemeriksaan kualitas untuk dataset transkripsi Tabel 6–10 Laporan KNKT KNKT.26.04.03.02.

## Checklist dan status

| Pemeriksaan | Kriteria | Status pada subset Tabel 6–10 |
|---|---|---|
| Format dan skema | CSV, header, delimiter, 16 kolom | Selesai; diuji otomatis |
| Jumlah rekaman | 59 baris tabel sumber, 58 unik setelah satu duplikasi identik | Selesai |
| Timestamp | Format eksplisit, urutan, keunikan | Selesai untuk subset |
| Gap waktu | 20:51:28–20:51:33 tidak ada pada Tabel 6–10 | Selesai; batas cakupan subset didokumentasikan |
| Nilai kosong | Empat kolom status, masing-masing 26 sel kosong | Selesai |
| Placeholder | Tujuh nilai `---` pada akselerasi | Selesai |
| Tipe dan satuan | Sesuai kamus data; transformasi pada salinan | Selesai |
| Rekonsiliasi sumber | Pencocokan visual setiap baris/kolom Tabel 6–10 | Selesai; satu koreksi Load 160 A |
| Lampiran 7 | Audit seluruh rekaman pada tabel Data Logger setelah penyesuaian master time | Belum dilakukan; di luar cakupan dataset saat ini |

## Batas dataset

CSV `data/processed/data_logger_knkt_tabel_6_10.csv` hanya merepresentasikan Tabel 6–10. Lampiran 7 PDF KNKT memuat enam timestamp tambahan 20:51:28–20:51:33. Timestamp tersebut tidak diinterpolasi atau ditambahkan ke CSV ini. Jeda tujuh detik harus disebut sebagai batas cakupan subset Tabel 6–10, bukan sebagai ketiadaan rekaman di seluruh PDF.

Jika cakupan diperluas ke Lampiran 7, lakukan transkripsi dan audit independen atas seluruh 64 timestamp dan 16 kolom, rekonsiliasi perbedaan header, nilai, serta penyesuaian master time, kemudian hitung ulang seluruh statistik, grafik, dan narasi. Jangan menambahkan enam baris hanya berdasarkan cuplikan teks OCR.
