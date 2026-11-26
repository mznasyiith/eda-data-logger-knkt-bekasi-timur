# Validasi Visualisasi EDA

Checklist pemeriksaan keluaran setelah menjalankan `python scripts/generate_visuals.py`.

## Pemeriksaan teknis
- [ ] Generator selesai tanpa exception.
- [ ] Semua keluaran Bab I–IX tersimpan pada folder yang sesuai.
- [ ] PNG dapat dibuka dan memiliki ukuran bukan nol.
- [ ] GIF memiliki lebih dari satu frame.
- [ ] HTML interaktif dapat dibuka; koneksi internet diperlukan untuk Plotly CDN.
- [ ] CSV ringkasan dapat dibaca ulang oleh Pandas.

## Pemeriksaan analitis
- [ ] Dataset tetap 58 rekaman × 16 kolom.
- [ ] Jeda 20:51:28–20:51:33 dijelaskan sebagai batas subset Tabel 6–10; enam rekaman pada Lampiran 7 tidak dicampurkan atau diinterpolasi.
- [ ] Placeholder akselerasi `---` tidak dikonversi menjadi nol.
- [ ] Missingness struktural empat kolom status tidak disebut sebagai kegagalan sensor.
- [ ] Korelasi tidak ditafsirkan sebagai sebab-akibat.
- [ ] Tidak ada grafik evaluasi model, imputasi, scaling, encoding, atau perlakuan pencilan yang tidak dilakukan.

## Pemeriksaan visual
- [ ] Judul, satuan, label sumbu, legenda, dan sumber terbaca.
- [ ] Garis runtun waktu terputus pada interval yang lebih dari satu detik.
- [ ] Timeline kategori hanya menghubungkan observasi berurutan yang sesuai.
- [ ] Setiap gambar memiliki penjelasan dan batas interpretasi di katalog.
- [ ] Semua tautan gambar di laporan/katalog mengarah ke file yang tersedia.

Checklist ini melengkapi CI otomatis; inspeksi visual manual tetap diperlukan sebelum rilis laporan final.
