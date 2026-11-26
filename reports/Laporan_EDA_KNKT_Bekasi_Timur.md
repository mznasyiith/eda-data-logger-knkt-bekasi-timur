# LAPORAN EXPLORATORY DATA ANALYSIS (EDA)
## Rekaman Data Logger Lokomotif KA 4B pada Fase Emergency Brake dan Tabrakan di Stasiun Bekasi Timur

**Mata Kuliah:** Exploratory Data Analysis  
**Program Studi:** Magister Ilmu Komputer, Universitas Amikom Purwokerto  
**Penyusun:** Muhammad Za’iimun Nasyiith  
**Sumber utama:** Laporan Akhir Investigasi KNKT Nomor KNKT.26.04.03.02  
**Tanggal penyusunan:** 26 November 2026

> **Pernyataan ruang lingkup.** Analisis empiris menggunakan transkripsi Tabel 6, 7, 8, 9, dan 10. Terdapat 59 baris sumber; satu rekaman pukul 20:51:43 tercantum identik pada Tabel 7 dan Tabel 8 sehingga dataset gabungan deduplikasi memuat 58 rekaman unik dan 16 kolom. Rentang waktu tercatat 20:51:18–20:52:21, dengan celah rekaman 20:51:28–20:51:33. Empat kolom pada Tabel 9–10 tidak ditampilkan dan tetap kosong untuk 26 rekaman dari dua tabel tersebut.

---

# BAB 1. PENDAHULUAN DAN MEMAHAMI MASALAH (UNDERSTANDING THE PROBLEM)

## 1.1 Latar Belakang Masalah dan Tujuan Utama

Laporan Akhir Investigasi KNKT Nomor KNKT.26.04.03.02 membahas tabrakan antara KA 4B Argo Bromo Anggrek dan KA 5568A Commuter Line di Jalur 1 Stasiun Bekasi Timur pada 27 April 2026. Salah satu sumber informasi teknis dalam laporan adalah rekaman Data Logger lokomotif KA 4B. Data Logger merekam sejumlah parameter operasi, antara lain waktu, jarak, kecepatan, akselerasi, arus motor traksi, tekanan Brake Pipe (BP), tekanan Brake Cylinder (BC), posisi throttle, indikator PCS, dan status Independent Brake System (IBS).

Permasalahan yang dikaji dalam proyek ini bukan persoalan komersial seperti kehilangan pelanggan atau prediksi harga. Permasalahan analitisnya adalah bagaimana merekonstruksi secara terbatas perubahan parameter operasi lokomotif KA 4B pada rentang waktu yang disajikan, khususnya perubahan kecepatan, sistem pengereman, dan kontrol traksi, serta memastikan bahwa data yang ditranskripsikan dari laporan investigasi dapat dibaca, diperiksa, dan dianalisis secara terstruktur. Dalam perspektif investigasi kecelakaan, Data Logger merupakan satu sumber bukti teknis; interpretasinya harus diuji silang dengan kronologi KNKT dan bukti independen lain sebelum digunakan untuk menyimpulkan urutan sebab-akibat.

Tujuan EDA adalah:
1. Mengidentifikasi struktur dan cakupan dataset Data Logger yang digunakan.
2. Memeriksa kelengkapan, konsistensi, tipe data, nilai kosong, placeholder, dan duplikasi.
3. Mendeskripsikan perubahan kecepatan, jarak, tekanan BP/BC, arus motor traksi, throttle, PCS, dan IBS selama cuplikan waktu yang tersedia.
4. Menyajikan pola melalui statistik deskriptif dan visualisasi eksploratif.
5. Menetapkan batas interpretasi agar hasil EDA tidak disamakan dengan pembuktian sebab-akibat atau kesimpulan investigasi teknis.
6. Menyusun kebutuhan integrasi bukti lanjutan untuk rekonstruksi kejadian yang tersinkronisasi, termasuk data persinyalan, komunikasi, sarana, prasarana, dan faktor manusia.

## 1.2 Tipe Masalah

Proyek ini merupakan **Exploratory Data Analysis (EDA) deskriptif terhadap data runtun waktu (time-series)**. Dalam konteks investigasi, analisis ini merupakan tahap *data understanding* dan *preliminary event-pattern analysis*, bukan rekonstruksi kecelakaan menyeluruh dan bukan penetapan penyebab. Proyek ini tidak ditetapkan sebagai klasifikasi, regresi, maupun klasterisasi karena belum terdapat variabel target dan tujuan prediksi yang dirumuskan.

EDA digunakan untuk memahami data dan membangun pertanyaan analitis lanjutan. Penerapan model Machine Learning bukan sasaran wajib pada tahap ini. Pemaksaan algoritma klasifikasi atau regresi tanpa target yang sahih justru berisiko menghasilkan analisis yang tidak sesuai dengan tujuan penelitian.

## 1.3 Metrik Keberhasilan

Karena proyek ini tidak membangun model prediktif, akurasi, precision, recall, F1-score, MAE, dan RMSE belum relevan sebagai metrik keberhasilan. Keberhasilan EDA dinilai melalui kriteria kualitas, keterlacakan, dan reproduksibilitas berikut:
- Asal data dan halaman sumber dapat ditelusuri.
- Struktur dataset yang digunakan konsisten, yaitu 58 baris unik dan 16 kolom untuk cakupan Tabel 6–10.
- Nilai asli, termasuk penanda `---`, tidak diubah tanpa dasar.
- Nilai kosong struktural dibedakan dari penanda data sensor yang tidak terbaca.
- Proses pemuatan dengan Pandas berhasil dan dapat diulang.
- Statistik dan visualisasi dapat dihasilkan kembali dari berkas dataset yang sama.
- Setiap interpretasi dibatasi pada rekaman yang tersedia dan konteks yang dijelaskan dalam laporan KNKT.
- Tidak ada klaim sinkronisasi lintas-sumber, analisis ATP/interlocking, perhitungan jarak henti, atau penilaian faktor manusia tanpa bukti primer yang relevan.

---

# BAB 2. MEMAHAMI DATA (UNDERSTANDING THE DATA)

## 2.1 Pengumpulan Data (Data Collection)

### Identifikasi sumber data

Sumber primer adalah dokumen **Laporan Akhir Investigasi Kecelakaan Perkeretaapian KNKT Nomor KNKT.26.04.03.02**, yang diterbitkan oleh Komite Nasional Keselamatan Transportasi. Dokumen membahas tabrakan KA 4B Argo Bromo Anggrek dan KA 5568A Commuter Line di Stasiun Bekasi Timur pada 27 April 2026.

Dataset yang diperiksa berasal dari lima tabel yang saling melengkapi:
- Tabel 6–8, halaman tercetak 65–66 atau halaman PDF 75–76, yang memuat rekaman pada fase sebelum dan selama penerapan pengereman layanan.
- Tabel 9, “Rekaman data logger lokomotif KA 4B saat emergency brake aktif”, halaman tercetak 67 atau halaman PDF 77.
- Tabel 10, “Rekaman data logger lokomotif KA 4B saat tabrakan dengan KA 5568A”, halaman tercetak 68 atau halaman PDF 78.

Dengan demikian, cakupan laporan ini bukan hanya dua tabel terakhir, melainkan seluruh Tabel 6–10.

### Akses dan ekstraksi data

Dokumen PDF diperoleh dari situs resmi KNKT. Tabel sumber ditranskripsikan ke lembar kerja Excel. Berkas kerja yang diperiksa bernama `data_logger_knkt_tabel_6_10_lengkap.xlsx`, dengan sheet `Data_Logger_Raw`, `Data_By_Source`, dan `Metadata`. CSV gabungan tersedia pada `data/processed/data_logger_knkt_tabel_6_10.csv`.

Transkripsi tabel merupakan proses ekstraksi manual, sehingga validasi visual terhadap PDF tetap diperlukan. Dataset tidak boleh dianggap sebagai data mentah asli dari perangkat logger; dataset merupakan representasi tabel yang dipublikasikan dalam laporan investigasi. PDF sumber dipertahankan sebagai rujukan dan tidak dimodifikasi.

## 2.2 Deskripsi dan Eksplorasi Awal Data

Dataset gabungan memiliki **58 baris unik dan 16 kolom**. Baris sumber berjumlah 59 karena rekaman pukul 20:51:43 tercantum identik pada Tabel 7 dan Tabel 8. Setelah satu duplikasi lintas tabel dihilangkan, tersisa 58 timestamp unik. Cakupan waktu 20:51:18–20:52:21, tetapi terdapat celah enam detik tanpa rekaman yang disajikan, yaitu 20:51:28–20:51:33.

Enam belas kolom pada skema dataset:
1. `Date`
2. `Time`
3. `km`
4. `m`
5. `Speed (km/h)`
6. `Acceleration (m/sec²)`
7. `Load (amps)`
8. `EAB BP (psi)`
9. `EAB BC (psi)`
10. `DB Excit`
11. `Throttle`
12. `PCS Open`
13. `Dir Call`
14. `DB Set`
15. `DB Star`
16. `IBS`

Empat kolom, yaitu `DB Excit`, `Dir Call`, `DB Set`, dan `DB Star`, tersedia pada Tabel 6–8 tetapi tidak ditampilkan pada Tabel 9–10. Karena itu, kolom tersebut terisi pada 32 rekaman dari Tabel 6–8 dan kosong pada 26 rekaman Tabel 9–10. Keberadaan kolom tersebut dipertahankan untuk menjaga skema 16 kolom yang digunakan dalam proyek; nilai tidak direkonstruksi atau diisi dari asumsi.

Secara deskriptif, kecepatan berada pada rentang 0–109 km/jam, nilai kolom `m` pada rentang 0–863, dan kolom `km` bernilai 0 atau 1 sesuai tabel sumber. Nilai `km` dan `m` dipertahankan terpisah sebagaimana dicetak; tidak dilakukan rekonstruksi jarak absolut. Kolom `km` bernilai 1 pada sepuluh rekaman awal Tabel 6 dan 0 pada 48 rekaman berikutnya. Perubahan ini dicatat sebagai karakteristik representasi sumber dan tidak ditafsirkan sebagai kesalahan atau diperbaiki tanpa dokumentasi teknis.

## 2.3 Peninjauan Kualitas Data (Data Quality Assessment)

### Missing values dan placeholder

Pemeriksaan nilai kosong dengan Pandas menunjukkan 26 nilai kosong pada masing-masing kolom `DB Excit`, `Dir Call`, `DB Set`, dan `DB Star`, yaitu 44,83% dari 58 baris. Keempat kolom tersebut tersedia pada Tabel 6–8, tetapi tidak ditampilkan pada Tabel 9–10. Kondisi ini adalah ketidaktersediaan kolom pada cakupan dua tabel terakhir, bukan bukti bahwa sensor gagal merekam variabel tersebut.

Kolom `Acceleration (m/sec²)` memuat tujuh nilai teks `---`. Karena `---` adalah penanda yang tercantum dalam sumber, nilai tersebut dipertahankan pada dataset mentah. Untuk perhitungan numerik, penanda dapat dipetakan menjadi nilai tidak tersedia pada salinan analisis saja, tanpa mengubah berkas sumber. Laporan KNKT menjelaskan bahwa pada waktu tabrakan, akselerometer mencatat data kosong/tidak terbaca yang dikaitkan dengan G-Force akibat tabrakan yang melampaui batas ukur sensor.

### Duplikasi

Pemeriksaan duplikasi seluruh baris pada dataset menghasilkan **0 baris duplikat identik**. Pemeriksaan ini tidak membuktikan bahwa transkripsi bebas dari seluruh kemungkinan kesalahan; pencocokan setiap sel dengan gambar tabel PDF tetap merupakan langkah verifikasi yang diperlukan.

### Deteksi pencilan awal

Pencilan statistik tidak otomatis merupakan kesalahan. Pada hasil pemeriksaan IQR terhadap enam variabel numerik operasional (`m`, kecepatan, akselerasi numerik, arus, tekanan BP, dan tekanan BC), tidak ditemukan nilai di luar pagar IQR. Kolom `km` menghasilkan sepuluh penandaan mekanis karena Q1 dan Q3 sama-sama 0; hal ini merupakan konsekuensi variabel koordinat diskrit, bukan bukti pencilan operasional. Rincian dijelaskan pada Bab 8.

### Konsistensi format

Tanggal tercatat sebagai `27/04/2026`; waktu menggunakan format `HH.MM.SS`. Kolom akselerasi bertipe campuran karena berisi angka desimal dan placeholder teks. Kolom kategori seperti `Throttle`, `PCS Open`, dan `IBS` disimpan sebagai teks. Konversi tanggal, waktu, dan akselerasi harus dilakukan pada salinan analisis, bukan dengan menimpa nilai transkripsi.

## 2.4 Eksplorasi Visual Awal

Eksplorasi visual diarahkan pada urutan waktu dan karakteristik parameter operasi. Visualisasi yang relevan untuk dataset ini meliputi:
- Grafik garis kecepatan terhadap waktu untuk melihat penurunan kecepatan pada cuplikan yang tersedia.
- Grafik garis tekanan BP dan BC terhadap waktu untuk melihat perubahan tekanan selama pengereman.
- Histogram dan box plot untuk memeriksa distribusi kecepatan, jarak meter, arus motor traksi, tekanan BP/BC, dan akselerasi numerik.
- Diagram batang untuk frekuensi kategori throttle dan IBS.

Visualisasi bersifat deskriptif. Pola yang tampak tidak dapat digunakan sendiri untuk menyatakan penyebab kecelakaan atau menilai tindakan personel.

## 2.5 Penyelarasan dengan Kebutuhan Operasional

Data relevan untuk memahami perubahan parameter lokomotif pada cuplikan waktu yang meliputi fase sebelum emergency brake, pengereman darurat, dan saat tabrakan. Dataset gabungan memuat 58 rekaman unik dari Tabel 6–10. Meskipun lebih luas daripada Tabel 9–10 saja, data ini tetap belum cukup untuk menggambarkan keseluruhan rangkaian peristiwa, seluruh sistem pengereman rangkaian, kondisi sarana lain, aspek persinyalan secara lengkap, atau faktor eksternal.

Kebutuhan data tambahan untuk analisis yang lebih luas mencakup Tabel 6–8, keterangan teknis sistem pengereman, kronologi persinyalan dan komunikasi operasional, serta data pendukung lain yang telah diverifikasi dari laporan KNKT. Penambahan data harus menjaga identitas sumber, satuan, urutan waktu, dan jejak transkripsi.

### 2.6 Kerangka Bukti Investigasi dan Kebutuhan Data Lintas-Disiplin

Agar analisis tidak melampaui bukti yang tersedia, setiap kelompok pertanyaan investigasi dipetakan terhadap sumber data yang diperlukan. Status *tersedia* berarti tercakup dalam dataset yang dianalisis; *konteks dokumen* berarti dapat ditelaah dari bagian lain laporan KNKT tetapi belum menjadi variabel dalam dataset; dan *belum tersedia dalam dataset* berarti tidak boleh disimpulkan dari Data Logger KA 4B saja.

| Domain investigasi | Pertanyaan analitis | Bukti/data yang diperlukan | Status dalam proyek ini |
|---|---|---|---|
| Data logger lokomotif | Bagaimana kecepatan, arus, throttle, BP, BC, dan IBS berubah terhadap waktu? | Tabel 6–10 Data Logger KA 4B | Tersedia sebagai transkripsi tabel |
| Rekonstruksi kronologi | Bagaimana urutan kejadian lintas sumber dan ketidakpastian waktunya? | Timestamp logger, kronologi KNKT, jam sistem, catatan sinkronisasi | Terbatas; satu sumber logger dan narasi dokumen |
| Persinyalan, block, interlocking, wesel | Apa aspek status sinyal, rute, okupansi petak, dan penguncian wesel? | Log interlocking, log block, indikasi sinyal, data CTC/PPKA, diagram rute | Belum tersedia sebagai dataset terstruktur |
| ATP/ETCS/CBTC dan perlindungan SPAD | Apakah sistem proteksi aktif, memberi peringatan, atau melakukan intervensi? | Log perangkat proteksi yang benar-benar terpasang, konfigurasi, alarm, event record | Belum tersedia; jangan mengasumsikan teknologi tertentu terpasang |
| Sinkronisasi dua kereta | Bagaimana posisi, kecepatan, dan waktu kedua rangkaian dibandingkan? | Data logger KA 5568A dan KA 4B, sumber waktu, metode clock correction | Belum tersedia untuk analisis sinkronisasi |
| Komunikasi dan dispatch | Apa instruksi, konfirmasi, dan urutan komunikasi operasional? | Rekaman radio/audio, log telepon, catatan PPKA/OC, timestamp dan identitas kanal | Belum tersedia dalam dataset |
| Dinamika pengereman | Berapa jarak henti dan perlambatan aktual serta bagaimana perbandingannya dengan karakteristik rem? | Kecepatan awal, waktu respons, tekanan rem, massa, gradien, kondisi roda-rel, komposisi rangkaian, parameter rem | Belum cukup untuk menghitung jarak henti secara tervalidasi |
| Faktor manusia | Apa kondisi kewaspadaan, beban kerja, kepatuhan prosedur, dan tindakan kru? | Wawancara, rekaman komunikasi, jadwal dinas, bukti prosedural, data relevan lain | Tidak dapat dinilai dari logger saja |
| Prasarana dan jarak pandang | Bagaimana geometri lintas, lokasi sinyal, jarak pandang, cuaca, dan pencahayaan? | Track chart, survei geospasial, foto/video, cuaca, kondisi penerangan | Belum dianalisis dari dataset ini |
| Crashworthiness | Bagaimana pola deformasi, penetrasi, dan transfer energi benturan? | Pemeriksaan fisik, foto ukur, data struktur sarana, material, titik kontak | Di luar cakupan dataset logger |
| Operasi perjalanan | Bagaimana posisi kejadian terhadap GAPEKA, perjalanan aktual, dan izin masuk petak? | GAPEKA, train graph aktual, log perjalanan, izin dan komunikasi operasi | Perlu dokumen operasional pendukung |

Matriks tersebut adalah peta kebutuhan bukti, bukan pernyataan bahwa seluruh bukti telah diperoleh atau telah dianalisis. Istilah ATP, ETCS, CBTC, deadman, anti-climber, dan perangkat sejenis hanya boleh digunakan sebagai kategori pemeriksaan apabila relevan dengan konfigurasi sarana/prasarana yang dibuktikan oleh dokumen teknis. Tidak boleh diasumsikan terpasang hanya karena istilah tersebut termasuk dalam kerangka keahlian tim.

---

# BAB 3. MEMUAT DAN MEMERIKSA DATA (IMPORTING AND INSPECTING THE DATA)

## 3.1 Import Library dan Loading Dataset

Library utama adalah Pandas untuk pemuatan dan manipulasi tabel, NumPy untuk operasi numerik, serta Matplotlib/Seaborn untuk visualisasi. Contoh pemuatan Excel:

```python
import pandas as pd
import numpy as np

file_path = "data_logger_knkt_tabel_6_10_lengkap.xlsx"
df = pd.read_excel(file_path, sheet_name="Data_Logger_Raw")
```

Jika menggunakan CSV:

```python
df = pd.read_csv("data/processed/data_logger_knkt_tabel_6_10.csv")
```

Dataset tidak dibagi menjadi data latih dan data uji karena proyek ini belum melakukan pemodelan prediktif.

## 3.2 Inspeksi Dimensi dan Struktur Data

Pemeriksaan dilakukan menggunakan:

```python
df.head()
df.shape
df.columns.tolist()
```

Hasil pemeriksaan: `df.shape == (58, 16)`. Gunakan `pd.read_csv("data/processed/data_logger_knkt_tabel_6_10.csv")` untuk memuat versi CSV dalam repositori. Nama kolom mengikuti urutan skema 16 kolom yang disebutkan pada Bab 2. Dataset memuat 58 rekaman unik hasil penggabungan Tabel 6–10.

## 3.3 Pemeriksaan Tipe Data dan Informasi Umum

Hasil pembacaan dataset gabungan: `km`, `m`, `Speed (km/h)`, `Load (amps)`, `EAB BP (psi)`, dan `EAB BC (psi)` terbaca integer. `Acceleration (m/sec²)` terbaca object karena memuat angka dan placeholder `---`. `Date`, `Time`, serta variabel status terbaca object. Empat kolom `DB Excit`, `Dir Call`, `DB Set`, dan `DB Star` bertipe object dan memiliki 26 nilai kosong pada baris Tabel 9–10, tetapi berisi data pada 32 baris Tabel 6–8.

Tipe object pada akselerasi dapat dimengerti karena kolom memuat angka dan teks `---`. Tipe tanggal dan waktu belum berupa datetime; parsing dilakukan secara eksplisit pada salinan analisis.

### 3.5 Penanganan Waktu dan Integritas Urutan Rekaman

Kolom `Date` dan `Time` perlu digabung menjadi timestamp pada salinan analisis dengan format yang eksplisit. Pemeriksaan urutan dilakukan setelah parsing, tetapi timestamp hasil parsing tetap merepresentasikan waktu sebagaimana dicetak pada tabel sumber. Belum ada dasar untuk menyatakan bahwa jam Data Logger telah tersinkronisasi dengan jam interlocking, radio, CCTV, atau logger kereta lain. Setiap analisis lintas-sumber nantinya harus mendokumentasikan zona waktu, resolusi timestamp, kemungkinan offset/drift, metode koreksi jam, dan rentang ketidakpastian. Jangan menggeser timestamp agar tampak cocok dengan kronologi tanpa dasar kalibrasi atau bukti sinkronisasi.

## 3.4 Ringkasan Statistik Awal

Ringkasan statistik untuk variabel numerik yang memiliki data:
| Variabel | n | Mean | Median | Modus | Std. deviasi | Varians | Q1 | Q3 | Minimum | Maksimum |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| km | 58 | 0,172 | 0 | 0 | 0,381 | 0,145 | 0 | 0 | 0 | 1 |
| m | 58 | 300,483 | 244,5 | 0 | 256,769 | 65.930,044 | 84 | 478 | 0 | 863 |
| Speed (km/h) | 58 | 73,638 | 82,5 | 108 | 33,077 | 1.094,060 | 57,5 | 101,75 | 0 | 109 |
| Acceleration (m/sec²) | 51 | -0,336 | -0,38 | -0,38 | 0,203 | 0,041 | -0,5 | -0,16 | -0,84 | 0,05 |
| Load (amps) | 58 | 86,345 | 136 | 0 | 76,730 | 5.887,458 | 0 | 152 | 0 | 168 |
| EAB BP (psi) | 58 | 31,897 | 49 | 0 | 28,264 | 798,831 | 0 | 51,75 | 0 | 71 |
| EAB BC (psi) | 58 | 26 | 2 | 0 | 31,191 | 972,877 | 0 | 58 | 0 | 73 |

Untuk akselerasi, n numerik adalah 51 karena tujuh nilai `---` tidak dapat diperlakukan sebagai angka. Statistik dihitung setelah placeholder dikecualikan pada salinan analisis. Empat kolom status merupakan variabel kategorikal, sehingga tidak diringkas dengan statistik numerik.

---

# BAB 4. PENANGANAN DATA YANG HILANG (HANDLING MISSING DATA)

## 4.1 Identifikasi Nilai yang Hilang

Pemeriksaan `isnull().sum()` menemukan 26 nilai kosong pada masing-masing kolom `DB Excit`, `Dir Call`, `DB Set`, dan `DB Star`, atau 44,83% dari 58 baris per kolom. Keempat kolom tersebut tidak ditampilkan pada Tabel 9–10. Secara terpisah, `Acceleration (m/sec²)` memiliki tujuh placeholder `---` (12,07% dari 58 baris) pada bagian Tabel 10. Placeholder ini bukan null teknis dalam berkas transkripsi mentah, tetapi menandakan data akselerasi tidak tersedia/tidak terbaca sebagaimana ditampilkan pada sumber.

## 4.2 Analisis Mekanisme Missing Data

Mekanisme kehilangan data tidak dapat diklasifikasikan secara menyeluruh sebagai MCAR, MAR, atau MNAR hanya dari dataset kecil ini.

- Empat kolom kosong karena tidak ditampilkan pada Tabel 9–10. Kondisi ini lebih tepat disebut tidak tersedia dalam cakupan sumber, bukan missing value observasional yang mekanismenya dapat diuji.
- Tujuh placeholder akselerasi terkait dengan kondisi tabrakan dan keterbatasan pembacaan sensor sebagaimana diterangkan dalam laporan KNKT. Karena berkaitan dengan peristiwa yang sedang diamati, kehilangan tersebut tidak layak diasumsikan MCAR. Akan tetapi, label MAR/MNAR formal tidak ditetapkan tanpa data sensor dan rancangan pengukuran yang lebih lengkap.

## 4.3 Strategi Eliminasi (Deletions)

Tidak dilakukan penghapusan baris maupun kolom. Menghapus empat kolom akan menghilangkan informasi tentang struktur skema yang digunakan proyek. Menghapus baris akselerasi dengan placeholder juga berisiko menghilangkan rekaman penting pada saat tabrakan. Ukuran dataset gabungan dipertahankan pada 58 × 16.

## 4.4 Strategi Imputasi (Imputation Methods)

Tidak dilakukan imputasi mean, median, modus, KNN Imputer, atau MICE. Pengisian nilai sensor yang tidak terbaca dengan angka statistik akan menghasilkan nilai buatan yang tidak bersumber dari logger. Empat kolom yang tidak disediakan dalam tabel juga tidak boleh diimputasi. Untuk analisis numerik akselerasi, placeholder dikecualikan pada salinan sementara dan jumlah nilai yang dikecualikan dilaporkan secara eksplisit.

---

# BAB 5. EKSPLORASI KARAKTERISTIK DATA (EXPLORING DATA CHARACTERISTICS)

## 5.1 Statistik Deskriptif Data Numerik

Tabel pada Bab 3 menyajikan mean, median, modus, standar deviasi, minimum, dan maksimum. Secara umum, distribusi nilai pada beberapa variabel dipengaruhi oleh perubahan keadaan operasi dalam rentang waktu singkat. Karena data merupakan rekaman berurutan setiap satu detik, nilai tidak dapat diperlakukan sebagai sampel acak yang saling independen.

Kolom `km` dan `m` dianalisis sebagai dua komponen lokasi sebagaimana dicetak. Kolom `km` bernilai 1 pada sepuluh rekaman Tabel 6 dan 0 pada 48 rekaman berikutnya; perubahan tersebut tidak diubah atau direkonstruksi. Interpretasi lokasi harus mempertimbangkan format koordinat pada sumber.

## 5.2 Bentuk Distribusi: Skewness dan Kurtosis

Nilai skewness dan excess kurtosis pada variabel numerik yang dapat dihitung:
| Variabel | Skewness | Excess kurtosis |
|---|---:|---:|
| km | 1,781 | 1,212 |
| m | 0,656 | -0,698 |
| Speed (km/h) | -0,958 | -0,084 |
| Acceleration (m/sec²) | 0,290 | -0,444 |
| Load (amps) | -0,216 | -1,937 |
| EAB BP (psi) | -0,130 | -1,830 |
| EAB BC (psi) | 0,503 | -1,660 |

Kurtosis yang disajikan adalah excess kurtosis (kurtosis Fisher), sehingga nilai 0 menjadi acuan distribusi normal secara teoretis. Pada gabungan ini, skewness kecepatan negatif (-0,958), sedangkan skewness akselerasi mendekati nol (0,290). Nilai skewness tidak digunakan untuk menyimpulkan normalitas. Akselerasi dihitung hanya dari 51 angka, bukan tujuh placeholder.

Ukuran skewness dan kurtosis pada sampel kecil dan berurutan ini tidak cukup untuk menyatakan normalitas. Histogram/KDE dapat membantu inspeksi visual, tetapi uji normalitas formal dan asumsi inferensial tidak menjadi tujuan utama proyek.

---

# BAB 6. TRANSFORMASI DATA (PERFORMING DATA TRANSFORMATION)

## 6.1 Transformasi untuk Memperbaiki Distribusi

Tidak diterapkan transformasi log, akar kuadrat, Box-Cox, atau Yeo-Johnson pada dataset sumber. Beberapa variabel menunjukkan kemiringan distribusi, tetapi transformasi tidak diperlukan untuk tujuan deskriptif dan dapat mengurangi keterbacaan satuan operasional. Perlu diluruskan bahwa model linear tidak mensyaratkan setiap fitur harus berdistribusi normal; asumsi normalitas dalam regresi klasik terutama berkaitan dengan residual untuk keperluan inferensi. Jika pemodelan dilakukan pada tahap berikutnya, transformasi hanya dipertimbangkan berdasarkan kebutuhan model, bentuk hubungan, dan diagnostik residual, kemudian diuji pada salinan data.

## 6.2 Transformasi Skala

StandardScaler dan MinMaxScaler tidak diterapkan. Scaling relevan untuk algoritma yang sensitif terhadap perbedaan skala, seperti KNN, K-Means, SVM, dan PCA, tetapi bukan prasyarat EDA deskriptif. Nilai asli dalam km/jam, ampere, psi, meter, dan m/s² dipertahankan agar interpretasi domain tetap jelas. Apabila scaling diperlukan pada pemodelan lanjutan, parameter scaler harus dipelajari hanya dari data latih untuk mencegah data leakage.

## 6.3 Konversi Data Kategorikal

Kategori `Throttle`, `PCS Open`, dan `IBS` tetap disimpan sebagai teks. One-hot encoding atau ordinal encoding belum diperlukan karena tidak ada model yang membutuhkan representasi numerik. Jika kelak digunakan, pengkodean harus didasarkan pada makna kategori dan tidak boleh mengasumsikan urutan numerik yang tidak ada.

## 6.4 Pembuatan Fitur Baru (Feature Engineering)

Untuk analisis lanjutan, fitur turunan yang dapat dipertimbangkan adalah timestamp gabungan dari Date dan Time, detik relatif sejak awal cuplikan, serta penanda fase berdasarkan definisi yang bersumber dari laporan. Fitur turunan tersebut harus dibuat pada tabel analisis terpisah dan didokumentasikan. Tidak dibuat fitur rasio atau label kejadian baru dalam dataset sumber pada tahap ini.

---

# BAB 7. VISUALISASI HUBUNGAN DATA (VISUALIZING RELATIONSHIP OF DATA)

## 7.1 Analisis Univariate

Analisis univariat dilakukan dengan histogram/box plot untuk variabel numerik dan diagram batang untuk kategori. Variabel yang paling relevan adalah kecepatan, jarak meter, arus motor traksi, tekanan BP, tekanan BC, dan akselerasi numerik. Frekuensi throttle pada 58 baris: T5 17, Idle 13, T7 11, Off 10, T4 4, T6 2, dan T1 1. PCS tercatat Closed pada 32 baris dan Open pada 26 baris. IBS tercatat Rel pada 39 baris dan Appl pada 19 baris. Frekuensi tersebut menggambarkan keseluruhan gabungan Tabel 6–10, bukan hanya Tabel 9–10.

## 7.2 Analisis Bivariate dan Multivariate

Grafik garis kecepatan terhadap waktu dan grafik tekanan BP/BC terhadap waktu lebih sesuai daripada scatter plot generik karena urutan waktu merupakan konteks utama data. Perbandingan dua tekanan harus memperhatikan satuan yang sama (psi), sedangkan arus motor traksi menggunakan ampere dan kecepatan menggunakan km/jam. Hubungan visual tidak otomatis menunjukkan pengaruh kausal. Untuk rekonstruksi kecelakaan, sumbu waktu harus diperlakukan sebagai kunci pengurutan yang masih memiliki ketidakpastian sumber. Dataset ini hanya memuat logger KA 4B; karena itu, tidak boleh dibuat klaim bahwa data telah disinkronkan dengan KA 5568A, log persinyalan, rekaman radio, CCTV, atau data operasi. Analisis silang baru dapat dilakukan setelah timestamp, sumber jam, offset, drift, dan metode penyelarasan didokumentasikan. Jika tersedia data tambahan, gunakan *timeline evidence matrix* yang mencatat waktu sumber, waktu terkoreksi, ketidakpastian, sumber bukti, dan status verifikasi untuk setiap peristiwa.

## 7.3 Analisis Korelasi dan Asosiasi

Matriks korelasi tidak dijadikan dasar kesimpulan utama. Dataset berisi 58 rekaman unik yang berurutan dari beberapa fase operasi dalam rentang waktu singkat. Variabel dapat berubah bersama karena dipengaruhi waktu dan fase pengereman. Korelasi Pearson atau Spearman berpotensi dipengaruhi tren waktu, autokorelasi, perubahan status sistem, dan ukuran sampel yang terbatas. Apabila heatmap korelasi ditampilkan, interpretasinya harus eksploratif, disertai jumlah observasi yang digunakan, dan tidak dianggap sebagai bukti sebab-akibat atau multikolinearitas dalam model yang belum dibangun.

---

# BAB 8. PENANGANAN PENCILAN (HANDLING OUTLIERS)

## 8.1 Metode Deteksi Pencilan

Deteksi menggunakan aturan Interquartile Range (IQR), dengan batas bawah Q1 − 1,5 × IQR dan batas atas Q3 + 1,5 × IQR. Pada 58 rekaman gabungan (51 nilai akselerasi numerik), tidak ditemukan pencilan IQR pada enam variabel numerik operasional: `m`, `Speed (km/h)`, `Acceleration (m/sec²)`, `Load (amps)`, `EAB BP (psi)`, dan `EAB BC (psi)`. Pada kolom `km`, Q1=Q3=0 sehingga IQR=0 dan pagar atas maupun bawah sama dengan nol. Sepuluh nilai `km=1` kemudian ditandai oleh aturan secara mekanis. Karena `km` adalah komponen koordinat diskrit dan pola tersebut mengikuti pembagian tabel sumber, penandaan ini tidak diperlakukan sebagai pencilan operasional. Z-score tidak digunakan sebagai metode utama karena distribusi normal tidak dapat diasumsikan pada cuplikan runtun waktu yang kecil dan berurutan.

## 8.2 Keputusan Perlakuan terhadap Pencilan

Semua nilai dipertahankan. Nilai ekstrem terjadi dalam cuplikan perubahan keadaan pengereman, sehingga secara domain dapat merepresentasikan transisi sistem yang justru penting untuk diamati. Tidak dilakukan trimming, capping, winsorization, atau transformasi untuk menyembunyikan nilai ekstrem. Setiap koreksi hanya dapat dilakukan jika ditemukan kesalahan transkripsi yang dapat dibuktikan dengan membandingkan kembali ke tabel sumber. Perlu dibedakan tiga konsep: (1) pencilan statistik, yaitu nilai yang berada di luar pagar metode statistik; (2) anomali operasional, yaitu perilaku yang menyimpang dari ekspektasi teknis berdasarkan konteks sistem; dan (3) bukti kegagalan/penyebab, yang memerlukan verifikasi teknis dan bukti independen. Ketiganya tidak saling identik. Hasil IQR pada dataset ini tidak menemukan pencilan pada enam variabel numerik operasional, tetapi hal tersebut tidak membuktikan bahwa seluruh perilaku sistem normal atau bebas anomali.

---

# BAB 9. KESIMPULAN DAN TEMUAN UTAMA (COMMUNICATE FINDINGS AND INSIGHTS)

## 9.1 Rangkuman Temuan Utama

Berdasarkan 58 rekaman unik Tabel 6–10:
1. Rekaman mencakup rentang 20:51:18–20:52:21. Tidak semua detik tersedia: tidak ada rekaman yang disajikan untuk 20:51:28–20:51:33.
2. Kecepatan pada rekaman awal Tabel 6 adalah 108 km/jam (20:51:18); nilai maksimum dalam gabungan adalah 109 km/jam pada 20:51:20. Pada akhir Tabel 10, kecepatan tercatat 0 km/jam pada 20:52:19–20:52:21.
3. Tekanan BP turun dari 71 psi pada 20:51:18 menjadi 49 psi pada 20:51:43, lalu turun menjadi 0 psi pada 20:52:00 dan sebagian besar tetap 0 psi pada rekaman berikutnya.
4. Tekanan BC pada lokomotif meningkat hingga 8 psi pada fase awal full service (20:51:39), kemudian tercatat 0 psi pada 20:51:43–20:51:55; pada fase emergency meningkat hingga 70 psi pada 20:52:00 dan maksimum 73 psi pada 20:52:12.
5. Arus motor traksi tercatat 168 ampere pada awal Tabel 6, turun menjadi 136 ampere pada 20:51:39–20:51:43, dan menjadi 0 ampere sejak 20:51:57.
6. Throttle berubah dari T7 menuju T5 pada fase full service, T4 menjelang emergency brake, lalu T4/T1/Idle dan Off pada fase emergency. IBS berubah dari Rel menjadi Appl pada 20:52:03 dan tetap Appl dalam rekaman berikutnya.
7. Pada pukul 20:52:12–20:52:18, tujuh nilai akselerasi berturut-turut ditandai `---`. Laporan KNKT menjelaskan bahwa sensor akselerometer mencatat data kosong/tidak terbaca pada saat tabrakan karena G-Force melampaui batas ukur sensor.

Temuan di atas merupakan pembacaan deskriptif terhadap tabel. Interpretasi teknis mengenai sistem pengereman dan kejadian tabrakan harus merujuk pada uraian investigasi KNKT secara keseluruhan.

## 9.2 Keterbatasan dan Kendala Analisis

- Dataset mencakup Tabel 6–10 sebagaimana disajikan pada halaman tercetak 65–68 laporan KNKT. Dataset tetap bukan ekspor mentah perangkat logger dan tidak mencakup data lain di luar tabel tersebut.
- Jumlah data gabungan adalah 58 timestamp unik dari 59 baris sumber; terdapat celah enam detik antara Tabel 6 dan Tabel 7.
- Empat kolom kosong karena tidak tersedia pada dua tabel sumber.
- Tujuh nilai akselerasi berupa placeholder `---`; nilai tersebut tidak dapat digunakan dalam perhitungan numerik.
- Data bersifat time-series dan berurutan, sehingga asumsi independensi sampel tidak dapat langsung digunakan.
- Analisis bergantung pada transkripsi tabel PDF. Pemeriksaan visual telah dilakukan, tetapi verifikasi independen oleh pemeriksa kedua terhadap setiap sel masih direkomendasikan.
- Data logger lokomotif saja tidak mewakili seluruh faktor teknis, operasional, persinyalan, kondisi lintas, dan rangkaian kereta.
- EDA tidak membuktikan sebab-akibat, kelalaian, atau tanggung jawab pihak tertentu.

## 9.3 Rekomendasi Langkah Selanjutnya

1. Lakukan verifikasi independen kedua terhadap transkripsi Tabel 6–8, terutama angka yang dibaca dari tabel raster, sebelum menjadikannya data final publikasi.
2. Lakukan verifikasi ganda (double-entry/checking) terhadap setiap sel hasil transkripsi dengan gambar tabel PDF.
3. Simpan dataset mentah tanpa perubahan, kemudian buat salinan analisis dengan tipe datetime dan numerik yang eksplisit.
4. Tambahkan pemeriksaan otomatis untuk jumlah kolom, jumlah baris, urutan waktu, duplikasi, placeholder, dan nilai di luar rentang yang dapat diverifikasi.
5. Perluas konteks dengan bagian laporan KNKT yang menjelaskan kronologi, persinyalan, komunikasi, serta sistem pengereman.
6. Jangan menerapkan SMOTE, klasifikasi, regresi, atau algoritma prediktif sebelum tujuan prediksi, target, cakupan data, dan strategi validasi runtun waktu dirumuskan.
7. Jika analisis lanjutan bertujuan mendeteksi anomali, definisikan terlebih dahulu anomali berdasarkan konteks teknis dan validasi domain; jangan menjadikan pencilan IQR sebagai label kesalahan secara otomatis.
8. Jika dokumen sumber tersedia, ekstrak log persinyalan/interlocking, catatan perjalanan aktual dan izin masuk petak, serta kronologi komunikasi PPKA/OC/masinis dengan mempertahankan file asli, metadata, zona waktu, dan hash integritasnya.
9. Peroleh data logger KA 5568A dan dokumentasi sumber waktunya sebelum melakukan sinkronisasi dua kereta. Lakukan koreksi offset/drift hanya jika ada dasar teknis yang dapat diuji; laporkan rentang ketidakpastian waktu.
10. Untuk kajian pengereman, kumpulkan parameter massa dan komposisi rangkaian, karakteristik rem, gradien lintas, kondisi adhesi roda-rel, kecepatan, tekanan dan waktu respons. Jangan menyimpulkan jarak henti dari perubahan kecepatan saja tanpa model dan parameter yang tervalidasi.
11. Untuk aspek persinyalan, ATP/SPAD, geometri lintas, visibilitas, faktor manusia, dan crashworthiness, gunakan bukti primer yang sesuai: log perangkat yang benar-benar terpasang, diagram interlocking, track chart, survei lapangan, rekaman komunikasi, pemeriksaan sarana, dan dokumen prosedur. Jika bukti tidak tersedia, nyatakan sebagai keterbatasan, bukan mengisi dengan asumsi.
12. Simpan setiap sumber sebagai artefak immutable, catat asal-usul dan checksum, pisahkan data mentah, data hasil transkripsi, data hasil normalisasi waktu, dan data analisis; lakukan validasi skema, unit test, pemeriksaan perubahan, serta review independen sebelum rilis dataset.
13. Untuk pemodelan lanjutan, prioritaskan metode yang sesuai dengan tujuan dan struktur data. Dengan 58 rekaman dari satu kejadian, dataset ini belum memadai untuk melatih model prediktif yang dapat digeneralisasi. Model anomali atau klasifikasi baru dipertimbangkan setelah tersedia kumpulan kejadian yang representatif, label yang tervalidasi, dan strategi validasi berbasis waktu/kejadian agar tidak terjadi data leakage.

---

## REFERENSI

Komite Nasional Keselamatan Transportasi. (2026). *Laporan akhir investigasi kecelakaan perkeretaapian: Tabrakan antara KA 4B Argo Bromo Anggrek dan KA 5568A Commuter Line, Jalur 1 Stasiun Bekasi Timur, Daop 1 Jakarta, 27 April 2026* (Nomor laporan KNKT.26.04.03.02). https://knkt.go.id/Repo/Files/Laporan/Perkeretaapian/2026/KNKT.26.04.03.02-Final-Report.pdf

## CATATAN REPRODUKSIBILITAS

- Dataset yang dianalisis: `data_logger_knkt_tabel_6_10_lengkap.xlsx`, sheet `Data_Logger_Raw`; CSV repositori: `data/processed/data_logger_knkt_tabel_6_10.csv`.
- Cakupan sumber: Tabel 6–10, halaman tercetak 65–68.
- Baris transkripsi dari seluruh tabel: 59; dataset gabungan setelah menghapus satu duplikasi identik lintas Tabel 7–8: 58 baris × 16 kolom.
- Gap sumber: tidak ada rekaman yang ditampilkan untuk 20:51:28–20:51:33; tidak dilakukan interpolasi.
- File CSV proyek: `data/processed/data_logger_knkt_tabel_6_10.csv`.
- Placeholder `---` dipertahankan pada data mentah dan hanya dikecualikan dari kalkulasi numerik akselerasi.
- Tidak dilakukan imputasi, penghapusan baris, penghapusan kolom, scaling, encoding, atau transformasi terhadap dataset mentah.
- CSV transkripsi Tabel 6–10 disertakan pada repositori di `data/processed/`; PDF sumber tidak disertakan. Penggunaan ulang dataset harus tetap mencantumkan laporan KNKT sebagai sumber dan memperhatikan ketentuan penggunaan materi sumber.
