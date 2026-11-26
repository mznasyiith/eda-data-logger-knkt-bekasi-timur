# Verifikasi Sumber Variabel Jarak Data Logger KA 4B

## Status

**Terverifikasi untuk pembentukan besaran jarak gabungan; belum layak untuk merekonstruksi chainage absolut setiap baris.**

Pemeriksaan dilakukan terhadap Laporan Akhir Investigasi KNKT Nomor KNKT.26.04.03.02, khususnya Gambar 36, uraian Bagian II.3, Tabel 6–10, dan penjelasan kejadian tabrakan hingga lokomotif berhenti.

Sumber resmi: [Laporan Akhir KNKT KNKT.26.04.03.02 (PDF)](https://laman.knkt.go.id/Repo/Files/Laporan/Perkeretaapian/2026/KNKT.26.04.03.02-Final-Report.pdf)  
Tanggal pemeriksaan: 26 November 2026.

## Kesimpulan semantik

Kolom `km` dan `m` pada Tabel 6–10 merupakan dua komponen dari satu besaran jarak yang dicatat dalam satuan kilometer dan meter. Keduanya **bukan dua variabel numerik independen** dan tidak boleh masing-masing diperlakukan sebagai ukuran kuantitatif terpisah dalam statistik, distribusi, korelasi, atau deteksi pencilan.

Besaran gabungannya merepresentasikan **jarak tersisa menuju titik henti akhir lokomotif** sebagaimana dijelaskan dalam Bagian II.3 laporan KNKT. Besaran ini menurun menuju nol ketika lokomotif berhenti. Besaran ini bukan chainage/nomor kilometer absolut lintas.

Variabel analitis yang direkomendasikan:

```python
distance_to_stop_m = km * 1000 + m
```

Nama `distance_to_stop_m` dipilih agar makna dan satuannya eksplisit. Kolom sumber `km` dan `m` wajib tetap dipertahankan tanpa perubahan dalam data mentah.

## Bukti silang dari laporan KNKT

1. Gambar 36, halaman tercetak 63, menampilkan sumbu jarak yang menurun dari sekitar 1,34 km sampai 0,00 km seiring urutan waktu.
2. Bagian II.3.1, halaman tercetak 64, menyebut rekaman awal pada jarak 1.341 m dari titik berhenti setelah tabrakan di Km 28+941; jarak ke titik tabrakan di Km 28+915 disebut 1.315 m.
3. Uraian pada halaman tercetak 65 menghubungkan rekaman 20:51:34 dengan jarak 863 m dan lokasi Km 28+078.
4. Tabel 9, halaman tercetak 67, mencatat 301 m pada 20:51:56.
5. Tabel 10, halaman tercetak 68, mencatat 26 m pada 20:52:12 saat tabrakan, kemudian 0 m pada 20:52:18 dan seterusnya ketika lokomotif berhenti.
6. Uraian halaman tercetak 68 menyebut tabrakan di Km 28+915 dan lokomotif berhenti di Km 28+941, selisih 26 m. Ini konsisten dengan nilai jarak gabungan 26 m pada rekaman tabrakan dan 0 m pada rekaman berhenti.

Contoh pembacaan nilai tabel:

| Waktu | km sumber | m sumber | Jarak tersisa gabungan |
|---|---:|---:|---:|
| 20:51:18 | 1 | 341 | 1.341 m |
| 20:51:27 | 1 | 70 | 1.070 m |
| 20:51:34 | 0 | 863 | 863 m |
| 20:52:12 (tabrakan) | 0 | 26 | 26 m |
| 20:52:19 (berhenti) | 0 | 0 | 0 m |

## Ketidaksesuaian internal yang harus dipertahankan sebagai catatan sumber

Ditemukan ketidaksesuaian pada narasi chainage dalam PDF yang tidak boleh diperbaiki diam-diam:

- Pada halaman tercetak 66, uraian rentang 20:51:43–20:51:55 mengaitkan jarak 611 m dengan chainage Km 28+078. Namun, halaman sebelumnya mengaitkan 863 m pada 20:51:34 dengan Km 28+078. Pasangan 611 m dan Km 28+078 tampak tidak konsisten dengan urutan jarak pada tabel.
- Pada halaman tercetak 66, laporan menyebut emergency brake diaktifkan di Km 28+588 atau sekitar 275 m sebelum tabrakan di Km 28+915. Namun Tabel 9 pada halaman 67 mencatat jarak tersisa 301 m pada 20:51:56. Dengan jarak tabrakan 26 m dari titik henti akhir, selisih dari titik aktivasi hingga tabrakan adalah 301 - 26 = 275 m, sehingga nilai tabel mendukung jarak 275 m tetapi tidak mendukung chainage Km 28+588 jika titik henti akhir Km 28+941 digunakan.
- Karena terdapat konflik narasi chainage, proyek ini hanya akan menggunakan `distance_to_stop_m` sebagai jarak tersisa yang diturunkan dari dua komponen tabel. Jangan membuat variabel chainage absolut hasil rekonstruksi sebelum konflik tersebut diselesaikan dengan bukti primer tambahan atau klarifikasi KNKT.

Catatan ini merupakan dokumentasi atas isi sumber, bukan koreksi terhadap laporan KNKT.

## Keputusan untuk pipeline EDA

1. Pertahankan kolom mentah `km` dan `m`.
2. Bentuk `distance_to_stop_m` pada salinan analisis menggunakan `km * 1000 + m`.
3. Keluarkan `km` dan `m` dari daftar variabel numerik analitis yang digunakan untuk statistik, distribusi, korelasi, dan IQR.
4. Gunakan `distance_to_stop_m` untuk analisis jarak, dengan label grafik “Jarak tersisa menuju titik henti akhir (m)”.
5. Jangan menyebut besaran ini sebagai jarak pengereman murni, jarak ke titik tabrakan, atau chainage absolut. Nilainya adalah jarak tersisa menuju titik henti akhir menurut representasi sumber.
6. Jangan mengubah data mentah atau menambahkan baris interpolasi.
7. Hitung ulang seluruh tabel, grafik, korelasi, dan narasi yang sebelumnya menggunakan `km` atau `m` secara terpisah.

## Referensi

Komite Nasional Keselamatan Transportasi. (2026). *Laporan akhir investigasi kecelakaan perkeretaapian: Tabrakan antara KA 4B Argo Bromo Anggrek dan KA 5568A Commuter Line di Jalur I Stasiun Bekasi Timur, Daerah Operasi 1 Jakarta, tanggal 27 April 2026* (No. KNKT.26.04.03.02), khususnya Gambar 36 dan Bagian II.3, halaman tercetak 63–70.
