# Matriks Penyelarasan Laporan, Notebook, Kode, Visualisasi, dan Pengujian

Dokumen ini memetakan sembilan bab laporan utama ke notebook, generator, modul analisis, pengujian, dan file hasil. Katalog visualisasi berfungsi sebagai indeks artefak; pembahasan tujuan, cara membaca, temuan yang didukung, serta batas interpretasi setiap visual berada di laporan utama.

## Prinsip keterlacakan

1. Dataset analitis merupakan transkripsi Tabel 6–10: 58 rekaman unik × 16 kolom dari 59 baris sumber.
2. Raw CSV dibaca sebagai teks; parsing timestamp dan konversi numerik dilakukan pada salinan analisis.
3. Empat kolom status yang tidak ditampilkan pada Tabel 9–10 dibedakan dari tujuh placeholder akselerasi `---`.
4. Kolom sumber `km` dan `m` dipertahankan, tetapi analisis jarak menggunakan fitur turunan `distance_to_stop_m = km * 1000 + m` sesuai verifikasi sumber KNKT. Fitur tersebut berarti jarak tersisa menuju titik henti akhir, bukan chainage absolut.
5. Statistik, distribusi, korelasi, dan IQR tidak boleh memperlakukan `km` dan `m` sebagai variabel independen.
4. Tidak ada interpolasi pada gap 20:51:28–20:51:33. Grafik waktu memutus garis pada interval lebih dari satu detik.
5. Setiap gambar yang dirujuk laporan harus mempunyai file hasil pada `outputs/`.
6. Klaim kuantitatif harus dapat ditelusuri ke dataset, notebook, generator, tabel sumber KNKT, atau pengujian.

## Matriks bab, notebook, modul, dan pengujian

| Bab laporan | Notebook utama | Generator / modul analisis | Pengujian terkait |
|---|---|---|---|
| I. Pendahuluan dan pemahaman masalah | `notebooks/01_problem_understanding.ipynb` | `extended_chapter_i`; `config.py` | `test_reporting.py`; review ruang lingkup |
| II. Memahami data | `notebooks/02_data_understanding.ipynb` | `extended_chapter_ii`; `ingestion.py` | `test_dataset_integrity.py`; `test_validation.py` |
| III. Memuat dan memeriksa data | `notebooks/03_importing_and_inspecting.ipynb` | `chapter_iii_profile`; `extended_chapter_iii`; `ingestion.py`; `validation.py` | `test_dataset_integrity.py`; `test_validation.py`; `test_notebooks.py` |
| IV. Penilaian kualitas data | `notebooks/04_handling_missing_data.ipynb` | `chapter_iv_missingness`; `extended_chapter_iv`; `cleaning.py`; `validation.py` | `test_cleaning.py`; `test_dataset_integrity.py`; `test_visualization.py` |
| V. Eksplorasi karakteristik | `notebooks/05_exploring_characteristics.ipynb` | `chapter_v_distributions`; `extended_chapter_v`; `statistics.py`; fitur `distance_to_stop_m` | `test_statistics.py`; `test_visualization.py` |
| VI. Transformasi dan rekayasa fitur | `notebooks/06_data_transformation.ipynb` | `chapter_vi_temporal_feature`; `extended_chapter_vi`; `transformation.py` (`add_distance_to_stop_feature`) | `test_transformation.py`; `test_notebooks.py` |
| VII. Visualisasi dan hubungan antarvariabel | `notebooks/07_visualizing_relationships.ipynb` | `chapter_vii_visuals`; `extended_chapter_vii`; `visualization.py`; `statistics.py` | `test_visualization.py`; `test_notebooks.py` |
| VIII. Pencilan dan anomali | `notebooks/08_handling_outliers.ipynb` | `chapter_viii_outliers`; `extended_chapter_viii`; `statistics.py`; IQR pada `distance_to_stop_m` | `test_statistics.py`; `test_validation.py` |
| IX. Temuan dan rekomendasi | `notebooks/09_findings_and_insights.ipynb` | `chapter_ix_findings`; `extended_chapter_ix`; `reporting.py` | `test_reporting.py`; `test_notebooks.py`; `test_bab_ix_audit.py` |

`notebooks/00_project_setup.ipynb` merupakan notebook penyiapan lingkungan, bukan bab laporan.

## Inventaris visual dan file hasil

| Bab | File keluaran | Fungsi generator | Validasi utama |
|---|---|---|---|
| I | `outputs/bab_i/ruang_lingkup_eda.png` | `chapter_i_scope` | Ruang lingkup EDA dan batas inferensi |
| I | `outputs/bab_i/issue_tree_pertanyaan_eda.png` | `extended_chapter_i` | Pertanyaan tidak dinyatakan sebagai penyebab |
| I | `outputs/bab_i/alur_pemeriksaan_data.png` | `extended_chapter_i` | Alur mencerminkan transkripsi aktual |
| I | `outputs/bab_i/kpi_cakupan_eda.png` | `extended_chapter_i` | 59 sumber, 58 unik, 16 kolom, gap, placeholder |
| II | `outputs/bab_ii/cakupan_waktu_rekaman.png` | `chapter_ii_source_coverage` | Timestamp aktual dan gap terlihat |
| II | `outputs/bab_ii/pipeline_akuisisi_data.png` | `extended_chapter_ii` | Transkripsi manual dinyatakan |
| II | `outputs/bab_ii/matriks_data_ke_pertanyaan.png` | `extended_chapter_ii` | Pertanyaan, kolom, teknik selaras |
| II | `outputs/bab_ii/ringkasan_skema_dataset.png` | `extended_chapter_ii` | 16 kolom terwakili |
| III | `outputs/bab_iii/kelengkapan_kolom.png` | `chapter_iii_profile` | Missing dan placeholder diperhitungkan |
| III | `outputs/bab_iii/scorecard_struktur_dataset.png` | `extended_chapter_iii` | Dimensi 58 × 16 |
| III | `outputs/bab_iii/cuplikan_data_mentah.png` | `extended_chapter_iii` | Raw dan placeholder terjaga |
| III | `outputs/bab_iii/distribusi_tipe_data_raw.png` | `extended_chapter_iii` | Label tipe analisis tepat |
| III | `outputs/bab_iii/rentang_minimum_maksimum.png` | `extended_chapter_iii` | Rentang dan satuan sesuai variabel |
| IV | `outputs/bab_iv/missingness_per_kolom.png` | `chapter_iv_missingness` | Sel kosong dan placeholder dibedakan |
| IV | `outputs/bab_iv/missingness_matrix.png` | `extended_chapter_iv` | Tiga keadaan sel dan pola baris/kolom |
| IV | `outputs/bab_iv/missingness_kolom_status.png` | `extended_chapter_iv` | Empat kolom masing-masing 26 kosong |
| IV | `outputs/bab_iv/dampak_deduplikasi.png` | `extended_chapter_iv` | 59 menjadi 58 karena satu duplikasi identik |
| V | `outputs/bab_v/distribusi_numerik.png` | `chapter_v_distributions` | Akselerasi n valid 51 |
| V | `outputs/bab_v/frekuensi_kategorikal.png` | `chapter_v_distributions` | Kategori status dan frekuensi tepat |
| V | `outputs/bab_v/boxplot_mean_median.png` | `extended_chapter_v` | Mean/median nilai valid |
| V | `outputs/bab_v/ecdf_variabel_numerik.png` | `extended_chapter_v` | ECDF dari observasi valid |
| V | `outputs/bab_v/skewness_kurtosis.png` | `extended_chapter_v` | Excess kurtosis dan momen terdokumentasi |
| V | `outputs/bab_v/ringkasan_momen_distribusi.csv` | `extended_chapter_v` | Angka sama dengan grafik/laporan |
| VI | `outputs/bab_vi/interval_temporal.png` | `chapter_vi_temporal_feature` | Gap waktu tidak dipadatkan |
| VI | `outputs/bab_vi/alur_transformasi_aktual.png` | `extended_chapter_vi` | Raw tidak ditimpa; tanpa imputasi |
| VI | `outputs/bab_vi/pemetaan_tipe_dan_konversi.png` | `extended_chapter_vi` | Pemetaan konsisten dengan `load_data` |
| VII | `outputs/bab_vii/grafik_kecepatan_waktu.png` | `chapter_vii_visuals` | Satuan km/jam dan urutan waktu |
| VII | `outputs/bab_vii/tekanan_bp_bc_waktu.png` | `chapter_vii_visuals` | Dua seri tekanan dalam psi |
| VII | `outputs/bab_vii/heatmap_spearman.png` | `chapter_vii_visuals` | Korelasi pairwise dan n valid |
| VII | `outputs/bab_vii/animasi_urutan_kecepatan.gif` | `chapter_vii_visuals` | Urutan titik, bukan simulasi fisik |
| VII | `outputs/bab_vii/deret_waktu_interaktif.html` | `chapter_vii_visuals` | Timestamp sumber |
| VII | `outputs/bab_vii/tekanan_bp_bc_interaktif.html` | `chapter_vii_visuals` | Unit psi |
| VII | `outputs/bab_vii/heatmap_spearman_interaktif.html` | `chapter_vii_visuals` | Korelasi bukan kausalitas |
| VII | `outputs/bab_vii/jumlah_pasangan_valid_korelasi.csv` | `chapter_vii_visuals` | n pairwise dapat diaudit |
| VII | `outputs/bab_vii/multi_panel_parameter_waktu.png` | `extended_chapter_vii` | Satuan per panel dan gap terputus |
| VII | `outputs/bab_vii/categorical_state_timeline.png` | `extended_chapter_vii` | Missing sebagai gap; titik bukan durasi |
| VII | `outputs/bab_vii/scatter_hubungan_parameter.png` | `extended_chapter_vii` | Pasangan valid; warna hanya urutan waktu |
| VIII | `outputs/bab_viii/boxplot_iqr.png` | `chapter_viii_outliers` | Pagar IQR nilai valid |
| VIII | `outputs/bab_viii/ringkasan_iqr.csv` | `chapter_viii_outliers` | n, pagar, kandidat dapat diaudit |
| VIII | `outputs/bab_viii/jumlah_kandidat_iqr.png` | `extended_chapter_viii` | Jumlah cocok dengan ringkasan IQR |
| VIII | `outputs/bab_viii/konteks_temporal_parameter.png` | `extended_chapter_viii` | Garis terputus saat gap |
| IX | `outputs/bab_ix/ikhtisar_temuan.png` | `chapter_ix_findings` | Ringkasan cocok dengan dataset |
| IX | `outputs/bab_ix/decision_matrix_bukti_lanjutan.png` | `extended_chapter_ix` | Bukti tambahan tidak diasumsikan tersedia |
| IX | `outputs/bab_ix/scorecard_keterbatasan.png` | `extended_chapter_ix` | Angka cakupan dan keterbatasan konsisten |

## Pemetaan angka penting ke sumber komputasi

| Klaim | Sumber komputasi / sumber primer | Validasi |
|---|---|---|
| 59 baris sumber, 58 rekaman unik, 16 kolom | Data_By_Source, CSV analitis, `load_data` | `test_dataset_integrity.py` |
| 26 kosong pada empat kolom status | CSV, `extended_chapter_iv` | `test_dataset_integrity.py` |
| 7 placeholder akselerasi | CSV, `load_data`, `extended_chapter_iv` | `test_dataset_integrity.py` |
| Gap 20:51:28–20:51:33 | Timestamp CSV dan interval aktual | `test_dataset_integrity.py`; `test_visualization.py` |
| Statistik deskriptif dan momen | Notebook 05, `statistics.py`, generator | `test_statistics.py` |
| Perubahan parameter waktu | CSV, Notebook 07, generator, tabel sumber KNKT | `test_visualization.py`; review silang |
| Kandidat IQR | `outputs/bab_viii/ringkasan_iqr.csv` | `test_statistics.py`; `test_bab_ix_audit.py` |
| Waktu perubahan parameter Bab IX | Tabel 5–10 KNKT, grafik Lampiran 7, dan CSV transkripsi | `test_bab_ix_audit.py`; pemeriksaan silang timestamp dan fase |

## Audit angka Bab IX (26 November 2026)\n\nAudit Bab IX menambahkan tabel per timestamp untuk 20:51:18 sampai 20:52:21, frekuensi kategori beserta denominator, ringkasan statistik deskriptif, serta pagar dan jumlah kandidat IQR. Tabel 5 KNKT menjelaskan koreksi timestamp Data Logger lokomotif +2 detik terhadap master time CCTV KA 5568A; EDA menggunakan timestamp yang sudah tercantum pada Tabel 6–10 dan tidak menerapkan koreksi ulang. Peristiwa tabrakan 20:52:12 (40 km/jam) dibedakan dari berhenti 20:52:19 (0 km/jam). Perbedaan waktu narasi fase service brake dengan waktu tabel/grafik dicatat sebagai penyesuaian waktu, bukan disembunyikan.\n\nPengujian `tests/test_bab_ix_audit.py` memeriksa nilai timestamp terpilih, frekuensi kategori, statistik deskriptif, hasil IQR, dan keterangan penyesuaian master time terhadap dataset repositori.\n\n## Pengujian otomatis wajib

CI harus memvalidasi:
- seluruh referensi gambar Markdown lokal pada laporan utama menunjuk file yang ada;
- seluruh artefak visual inventaris tersedia setelah generator berjalan;
- dataset tetap 58 × 16, tujuh placeholder akselerasi tetap dipertahankan, dan empat kolom status masing-masing memiliki 26 nilai kosong;
- timeline kategori tidak mengubah missing menjadi kategori dan tidak menghubungkan lintas gap;
- interval waktu enam detik tidak diinterpolasi;
- nilai statistik, satuan, dan frekuensi kategori ditinjau terhadap keluaran komputasi dan tabel sumber.

Pengujian otomatis memeriksa integritas logika dan file; pengujian tersebut tidak menggantikan inspeksi akademik terhadap keterbacaan grafik dan ketepatan interpretasi.

## Aturan konsistensi akademik

- Sebut dataset sebagai transkripsi tabel KNKT, bukan ekspor mentah perangkat logger.
- Bedakan 59 baris sumber dan 58 rekaman unik setelah deduplikasi.
- Pertahankan `---` sebagai placeholder, bukan nol.
- Jelaskan kekosongan empat kolom status sebagai ketidaktersediaan pada cakupan Tabel 9–10.
- Jangan menetapkan MCAR/MAR/MNAR tanpa bukti pengujian yang memadai.
- Jangan melakukan imputasi atau interpolasi tanpa dasar sumber.
- Jangan menyimpulkan sebab-akibat dari korelasi atau mengartikan kandidat IQR sebagai kegagalan operasional.
- Cantumkan satuan pada sumbu kuantitatif dan jelaskan skala panel.
- Setiap visual utama harus memuat tujuan, cara membaca, temuan yang didukung, dan batas interpretasi.

## Checklist rilis

- [ ] Notebook 01–09 dieksekusi ulang tanpa error.
- [ ] Ruff dan Black lulus.
- [ ] Generator menghasilkan semua artefak terdaftar.
- [ ] Semua tautan gambar laporan lolos pemeriksaan file.
- [ ] Pengujian integritas dataset, missingness, timeline, IQR, dan laporan lulus.
- [ ] `pytest` lulus.
- [ ] CI commit final sukses dan log diperiksa.
- [ ] Laporan, katalog, matriks penyelarasan, dan README menggunakan angka serta nama file yang sama.

## Catatan verifikasi jarak (26 November 2026)

Definisi dan bukti sumber untuk `distance_to_stop_m` didokumentasikan pada `docs/02_data_understanding/source_validation_distance.md`. Pipeline visual (`scripts/generate_visuals.py`) dan notebook 05–09 membentuk fitur tersebut pada salinan analisis. Kolom mentah `km` dan `m` tidak diubah. Generator menggunakan fitur jarak gabungan untuk statistik numerik, visualisasi, korelasi Spearman, dan IQR. Notebook 09 menghasilkan ringkasan temuan dari statistik dan frekuensi yang dihitung, bukan placeholder temuan.
