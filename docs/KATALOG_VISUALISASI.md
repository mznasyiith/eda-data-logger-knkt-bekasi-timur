# Katalog Visualisasi dan Panduan Interpretasi EDA

Dokumen ini menjelaskan visual yang dihasilkan secara otomatis oleh `scripts/generate_visuals.py`. Semua grafik diturunkan dari `data/processed/data_logger_knkt_tabel_6_10.csv` dan tidak mengubah transkripsi mentah. Gambar yang sudah ada tetap dipertahankan; visual baru melengkapinya.

## Prinsip membaca

- Data merupakan transkripsi Tabel 6–10 laporan KNKT, bukan ekspor biner perangkat logger.
- Jumlah data analitis 58 rekaman unik; sumber awal 59 baris.
- Gap timestamp 20:51:28–20:51:33 tidak diinterpolasi.
- Tujuh tanda `---` pada akselerasi adalah placeholder, bukan nol.
- Empat kolom status kosong pada bagian sumber yang tidak menampilkan kolom tersebut; ini tidak otomatis menunjukkan kerusakan sensor.
- Korelasi dan perubahan bersama tidak membuktikan sebab-akibat.
- Grafik runtun waktu memakai timestamp aktual. Garis diputus saat terdapat interval lebih dari satu detik agar tidak menyiratkan observasi pada waktu yang hilang.

## Bab I — Pendahuluan dan memahami masalah

### Visual yang dipertahankan
- [Ruang lingkup EDA](../outputs/bab_i/ruang_lingkup_eda.png): menunjukkan batas pekerjaan dari sumber KNKT ke dataset dan analisis deskriptif.

### Visual tambahan
- [Issue Tree](../outputs/bab_i/issue_tree_pertanyaan_eda.png): memecah pertanyaan utama menjadi kualitas data, karakteristik, perubahan temporal, dan batas bukti. Cabang ini merupakan struktur pertanyaan analitis, bukan daftar penyebab kecelakaan.
- [Alur pemeriksaan data](../outputs/bab_i/alur_pemeriksaan_data.png): menggambarkan proses aktual dari laporan, ekstraksi/transkripsi, validasi, deduplikasi, EDA, hingga komunikasi temuan.
- [KPI cakupan EDA](../outputs/bab_i/kpi_cakupan_eda.png): menyajikan ukuran dataset dan indikator kualitas yang dapat dihitung. KPI ini bukan metrik performa model.

## Bab II — Memahami data

### Visual yang dipertahankan
- [Cakupan waktu rekaman](../outputs/bab_ii/cakupan_waktu_rekaman.png): menunjukkan kapan rekaman tersedia dan menandai gap antartimestamp.

### Visual tambahan
- [Pipeline akuisisi data](../outputs/bab_ii/pipeline_akuisisi_data.png): menjelaskan asal dokumen, transkripsi, validasi, pengolahan, dan dataset. Diagram menyebut transkripsi manual agar tidak mengesankan ETL otomatis.
- [Matriks data ke pertanyaan](../outputs/bab_ii/matriks_data_ke_pertanyaan.png): memetakan pertanyaan analitis ke kolom dan teknik pemeriksaan yang relevan.
- [Ringkasan skema dataset](../outputs/bab_ii/ringkasan_skema_dataset.png): mengelompokkan 16 kolom ke dimensi waktu/lokasi, dinamika, pengereman, dan status.

## Bab III — Memuat dan memeriksa data

### Visual yang dipertahankan
- [Kelengkapan kolom](../outputs/bab_iii/kelengkapan_kolom.png): menunjukkan persentase nilai yang tersedia pada setiap kolom.

### Visual tambahan
- [Scorecard struktur dataset](../outputs/bab_iii/scorecard_struktur_dataset.png): menampilkan baris, kolom, jumlah sel, sel terisi, dan sel kosong/placeholder. Angka sel total adalah hasil perkalian dimensi, bukan jumlah observasi independen.
- [Cuplikan data mentah](../outputs/bab_iii/cuplikan_data_mentah.png): memperlihatkan delapan rekaman pertama dalam bentuk transkripsi sebelum konversi tipe.
- [Distribusi tipe data raw](../outputs/bab_iii/distribusi_tipe_data_raw.png): memperlihatkan tipe pembacaan CSV. Kolom numerik pada sumber masih dibaca sebagai teks karena strategi preservasi raw.
- [Rentang minimum–maksimum](../outputs/bab_iii/rentang_minimum_maksimum.png): membandingkan rentang nilai variabel numerik dalam satuan aslinya; rentang lintas variabel tidak boleh dibandingkan tanpa memperhatikan satuan.

## Bab IV — Penilaian dan penanganan kualitas data

### Visual yang dipertahankan
- [Missingness per kolom](../outputs/bab_iv/missingness_per_kolom.png): merangkum jumlah nilai kosong dan placeholder pada setiap kolom.

### Visual tambahan
- [Missingness Matrix](../outputs/bab_iv/missingness_matrix.png): setiap sel membedakan nilai terisi, kosong, dan placeholder `---`. Matriks memperlihatkan pola lokasi nilai tidak tersedia pada level rekaman dan kolom.
- [Missingness kolom status](../outputs/bab_iv/missingness_kolom_status.png): memperlihatkan jumlah nilai kosong pada DB Excit, Dir Call, DB Set, dan DB Star. Kekosongan ini berkaitan dengan struktur tabel sumber yang tidak menampilkan kolom tersebut pada bagian tertentu.
- [Dampak deduplikasi](../outputs/bab_iv/dampak_deduplikasi.png): menunjukkan perubahan 59 baris sumber menjadi 58 rekaman unik karena satu rekaman identik lintas tabel. Ini bukan penghapusan baris karena missing value.

Tidak dilakukan uji MCAR/MAR/MNAR, imputasi, KNN imputation, atau penghapusan baris. Dengan satu kejadian dan pola kekosongan yang terkait struktur tabel, visual tersebut tidak dapat membuktikan mekanisme statistik missingness.

## Bab V — Eksplorasi karakteristik data

### Visual yang dipertahankan
- [Distribusi numerik](../outputs/bab_v/distribusi_numerik.png): histogram frekuensi nilai numerik analitis, termasuk `distance_to_stop_m` (jarak tersisa menuju titik henti akhir). Kolom sumber `km` dan `m` tidak diperlakukan sebagai variabel numerik terpisah.
- [Frekuensi kategorikal](../outputs/bab_v/frekuensi_kategorikal.png): jumlah rekaman pada kategori Throttle, PCS Open, dan IBS.

### Visual tambahan
- [Box plot mean dan median](../outputs/bab_v/boxplot_mean_median.png): memperlihatkan median, rentang antarkuartil, whisker, dan mean tiap variabel.
- [ECDF](../outputs/bab_v/ecdf_variabel_numerik.png): menunjukkan proporsi empiris observasi yang bernilai kurang dari atau sama dengan nilai pada sumbu X. ECDF tidak memerlukan pemilihan bin histogram.
- [Skewness dan excess kurtosis](../outputs/bab_v/skewness_kurtosis.png): membandingkan kemiringan dan keruncingan distribusi. Statistik ini bersifat deskriptif dan tidak membuktikan normalitas.
- [Ringkasan momen distribusi CSV](../outputs/bab_v/ringkasan_momen_distribusi.csv): menyediakan angka yang digunakan dalam grafik skewness/kurtosis.

## Bab VI — Transformasi dan rekayasa fitur

### Visual yang dipertahankan
- [Interval temporal](../outputs/bab_vi/interval_temporal.png): menunjukkan selang waktu aktual antarre­kaman, termasuk interval yang lebih panjang.

### Visual tambahan
- [Alur transformasi aktual](../outputs/bab_vi/alur_transformasi_aktual.png): mendokumentasikan pembuatan salinan analisis, parsing waktu, konversi numerik, pembentukan `distance_to_stop_m = km * 1000 + m`, rekayasa fitur waktu, dan validasi jumlah baris.
- [Pemetaan tipe dan konversi](../outputs/bab_vi/pemetaan_tipe_dan_konversi.png): menunjukkan perlakuan setiap kolom dari pembacaan raw menuju tipe pada salinan analisis.

Tidak dibuat visual before-after log transform, scaling, atau encoding karena operasi tersebut tidak diterapkan. Diagram proses di atas menjelaskan transformasi yang benar-benar dilakukan.

## Bab VII — Visualisasi hubungan antarvariabel

### Visual yang dipertahankan
- [Kecepatan terhadap waktu](../outputs/bab_vii/grafik_kecepatan_waktu.png): menunjukkan perubahan kecepatan sesuai urutan timestamp.
- [Tekanan BP dan BC](../outputs/bab_vii/tekanan_bp_bc_waktu.png): memperlihatkan dua tekanan pengereman dalam satuan psi.
- [Heatmap Spearman](../outputs/bab_vii/heatmap_spearman.png): menampilkan asosiasi monotonik antarvariabel numerik terpilih, termasuk `distance_to_stop_m`; kolom sumber `km` dan `m` tidak dimasukkan terpisah.
- [Animasi urutan kecepatan](../outputs/bab_vii/animasi_urutan_kecepatan.gif): memperlihatkan urutan titik rekaman, bukan simulasi fisik.
- [Deret waktu interaktif](../outputs/bab_vii/deret_waktu_interaktif.html), [tekanan interaktif](../outputs/bab_vii/tekanan_bp_bc_interaktif.html), dan [heatmap interaktif](../outputs/bab_vii/heatmap_spearman_interaktif.html): versi interaktif; Plotly JS dimuat dari CDN sehingga koneksi internet diperlukan.

### Visual tambahan
- [Multi-panel parameter waktu](../outputs/bab_vii/multi_panel_parameter_waktu.png): menempatkan kecepatan, tekanan BP, tekanan BC, arus, dan akselerasi pada panel terpisah dengan sumbu waktu bersama. Garis terputus pada gap agar tidak menghubungkan dua titik seolah-olah ada rekaman di antaranya.
- [Categorical State Timeline](../outputs/bab_vii/categorical_state_timeline.png): menampilkan titik status Throttle, PCS Open, dan IBS menurut timestamp. Segmen penghubung hanya digambar pada observasi berurutan satu detik dan kategori yang sama.
- [Scatter hubungan parameter](../outputs/bab_vii/scatter_hubungan_parameter.png): membandingkan Speed–BP, Speed–BC, dan BP–BC. Warna menunjukkan urutan waktu, bukan kelas atau sebab.

Korelasi harus dibaca sebagai eksplorasi asosiasi. Ukuran sampel kecil, urutan waktu, autokorelasi, dan perubahan fase dapat memengaruhi koefisien. `distance_to_stop_m` adalah jarak tersisa menuju titik henti akhir, bukan chainage absolut atau jarak pengereman murni.

## Bab VIII — Deteksi pencilan dan analisis anomali

### Visual yang dipertahankan
- [Box plot IQR](../outputs/bab_viii/boxplot_iqr.png): memeriksa kandidat pencilan menggunakan pagar 1,5 × IQR.
- [Ringkasan IQR](../outputs/bab_viii/ringkasan_iqr.csv): menyajikan jumlah observasi valid, pagar bawah/atas, dan jumlah kandidat.

### Visual tambahan
- [Jumlah kandidat IQR](../outputs/bab_viii/jumlah_kandidat_iqr.png): membandingkan jumlah kandidat statistik pada enam variabel analitis: `distance_to_stop_m`, kecepatan, akselerasi, arus, BP, dan BC. Kolom sumber `km` dan `m` tidak diuji terpisah.
- [Konteks temporal parameter](../outputs/bab_viii/konteks_temporal_parameter.png): menempatkan kecepatan, BP, dan BC pada urutan waktu agar perubahan ekstrem dapat ditinjau dalam konteks. Grafik ini bukan detektor kegagalan.

Tidak dilakukan trimming, winsorization, capping, Z-score control chart, Isolation Forest, atau Mahalanobis distance. Tidak adanya kandidat IQR pada beberapa variabel bukan bukti bahwa seluruh operasi normal atau bebas anomali.

## Bab IX — Kesimpulan, temuan, dan rekomendasi

### Visual yang dipertahankan
- [Ikhtisar temuan](../outputs/bab_ix/ikhtisar_temuan.png): merangkum ukuran dataset, rentang waktu, kecepatan, gap, dan placeholder akselerasi.

### Visual tambahan
- [Decision Matrix bukti lanjutan](../outputs/bab_ix/decision_matrix_bukti_lanjutan.png): menghubungkan pertanyaan penelitian lanjutan dengan data primer yang diperlukan dan status ketersediaannya pada dataset ini.
- [Scorecard keterbatasan](../outputs/bab_ix/scorecard_keterbatasan.png): mengingatkan pembaca mengenai cakupan data dan keterbatasan yang memengaruhi interpretasi.

## Visual yang sengaja tidak dibuat

Confusion matrix, ROC/PR curve, actual-vs-predicted, residual plot, train-test split, SMOTE, clustering, feature importance terhadap target, grafik imputasi, perbandingan scaling, dan grafik transformasi distribusi tidak dibuat. Tidak ada target prediksi, model terlatih, imputasi, scaling, encoding, atau perlakuan pencilan yang dilakukan pada tahap EDA ini. Menampilkan grafik tersebut akan memberi kesan keliru bahwa prosedur itu sudah dijalankan.

## Reproduksibilitas

Jalankan secara lokal:

```bash
python scripts/generate_visuals.py
```

Atau jalankan workflow CI. Workflow menghasilkan visual dari CSV, lalu mengunggah direktori `outputs/` sebagai artifact. Workflow memiliki izin read-only dan tidak melakukan commit/push; menjalankan workflow tidak mengubah berkas `outputs/` yang terlacak pada branch. Untuk hasil regenerasi yang tervalidasi, unduh [artifact `eda-visualizations` dari run 45836980007](https://github.com/mznasyiith/eda-data-logger-knkt-bekasi-timur/actions/runs/45836980007/artifacts/15126546343).

Semua visual tambahan dihasilkan oleh generator yang sama. Berkas pada `outputs/` di branch adalah snapshot yang dikomit; artifact CI adalah keluaran regenerasi pada commit yang diuji. Keduanya tidak boleh dianggap identik tanpa perbandingan berkas. Untuk reproduksi lokal, jalankan `python scripts/generate_visuals.py` dari root repository.
