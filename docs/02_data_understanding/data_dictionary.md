# Kamus Data (*Data Dictionary*)

## Metadata dataset

- Sumber: Laporan Akhir Investigasi KNKT Nomor KNKT.26.04.03.02.
- Cakupan: transkripsi Tabel 6–10.
- Skema: 58 rekaman unik × 16 kolom pada CSV gabungan.
- Rentang tanggal: 27 April 2026.
- Format tanggal: `DD/MM/YYYY`.
- Format waktu sumber: `HH.MM.SS`.
- Catatan: definisi singkatan yang tidak dijelaskan secara eksplisit di tabel harus diverifikasi terhadap uraian teknis laporan; jangan menebak kepanjangan atau fungsi status.

## Definisi kolom

| Nama kolom sumber | Tipe pada CSV | Kelompok | Satuan/format | Definisi dan batas interpretasi |
|---|---|---|---|---|
| `Date` | object | Temporal | DD/MM/YYYY | Tanggal yang dicetak pada rekaman Data Logger. |
| `Time` | object | Temporal | HH.MM.SS | Waktu yang dicetak pada rekaman Data Logger; titik digunakan sebagai pemisah komponen waktu. |
| `km` | integer | Posisi/jarak tersisa | km (komponen) | Komponen kilometer dari satu besaran jarak tersisa menuju titik henti akhir. Bukan variabel independen dan bukan chainage absolut. Pertahankan sebagai data sumber; untuk analisis gunakan `distance_to_stop_m`. |
| `m` | integer | Posisi/jarak tersisa | m (komponen) | Komponen meter dari satu besaran jarak tersisa menuju titik henti akhir. Bukan variabel independen. Untuk analisis gabungkan dengan `km` menjadi `distance_to_stop_m`; jangan analisis `m` secara terpisah. |
| `Speed (km/h)` | integer | Gerak | km/jam | Kecepatan yang dicatat pada tabel Data Logger. |
| `Acceleration (m/sec²)` | object | Gerak | m/s² | Akselerasi sebagaimana dicetak; tujuh rekaman berisi placeholder `---` yang tidak boleh diperlakukan sebagai nol. |
| `Load (amps)` | integer | Traksi/beban | ampere | Nilai arus/beban yang dicatat pada kolom sumber; interpretasi rinci mengikuti keterangan teknis laporan. |
| `EAB BP (psi)` | integer | Pengereman | psi | Nilai pada kolom EAB BP sesuai label sumber; jangan mengasumsikan lebih dari definisi teknis yang diverifikasi. |
| `EAB BC (psi)` | integer | Pengereman | psi | Nilai pada kolom EAB BC sesuai label sumber; jangan mengasumsikan lebih dari definisi teknis yang diverifikasi. |
| `DB Excit` | object | Status/kendali | label sumber | Status/indikator sebagaimana ditulis pada tabel; kolom tidak ditampilkan pada Tabel 9–10. |
| `Throttle` | object | Kendali | label sumber | Nilai/posisi throttle sebagaimana ditulis pada tabel; makna kategori mengikuti keterangan teknis sumber. |
| `PCS Open` | object | Status/kendali | label sumber | Status PCS sebagaimana ditulis pada tabel; interpretasi teknis harus merujuk laporan. |
| `Dir Call` | object | Status/kendali | label sumber | Kolom status sebagaimana ditulis pada tabel; tidak ditampilkan pada Tabel 9–10. |
| `DB Set` | object | Status/kendali | label sumber | Kolom status/set sebagaimana ditulis pada tabel; tidak ditampilkan pada Tabel 9–10. |
| `DB Star` | object | Status/kendali | label sumber | Kolom status sebagaimana ditulis pada tabel; tidak ditampilkan pada Tabel 9–10. |
| `IBS` | object | Status sistem | label sumber | Nilai status IBS sebagaimana ditulis pada tabel; arti status tidak boleh diperluas tanpa definisi sumber. |

## Catatan kualitas dan transformasi

1. Tujuh nilai `---` pada `Acceleration (m/sec²)` adalah placeholder tekstual dari sumber.
2. Kolom `DB Excit`, `Dir Call`, `DB Set`, dan `DB Star` masing-masing memiliki 26 nilai kosong pada subset Tabel 6–10 karena kolom tersebut tidak ditampilkan pada Tabel 9–10. Lampiran 7 PDF memuat empat kolom status pada tabel Data Logger lengkap; header `DB Start` pada lampiran perlu direkonsiliasi dengan `DB Star` sebelum nilai tersebut digabungkan.
3. Untuk analisis numerik, akselerasi dapat dikonversi pada salinan kerja menggunakan `pd.to_numeric(errors="coerce")`; CSV sumber tetap dipertahankan.
4. `Date` dan `Time` dapat digabung menjadi timestamp analitis dengan format eksplisit `%d/%m/%Y %H.%M.%S`. Ini tidak dengan sendirinya membuktikan sinkronisasi dengan sumber waktu lain.
5. Verifikasi sumber pada `source_validation_distance.md` menunjukkan `km` dan `m` adalah komponen satu besaran jarak tersisa menuju titik henti akhir, bukan dua variabel independen atau chainage absolut. Pada salinan analisis, bentuk `distance_to_stop_m = km * 1000 + m`; data mentah tetap tidak diubah.
6. Tipe data di atas adalah tipe saat CSV dibaca Pandas pada konfigurasi yang digunakan; tipe dapat berubah jika parameter parser berubah.

## Referensi sumber

Laporan Akhir Investigasi KNKT Nomor KNKT.26.04.03.02, Tabel 6–10, halaman tercetak 65–68 (halaman PDF 75–78).

## Variabel turunan tervalidasi

| Nama analitis | Rumus | Satuan | Definisi | Batas interpretasi |
|---|---|---|---|---|
| `distance_to_stop_m` | `km * 1000 + m` | m | Jarak tersisa menuju titik henti akhir menurut representasi Tabel 6–10 | Bukan chainage absolut, bukan jarak ke titik tabrakan, dan bukan jarak pengereman murni. Konflik beberapa narasi chainage KNKT dicatat dalam `source_validation_distance.md`. |
