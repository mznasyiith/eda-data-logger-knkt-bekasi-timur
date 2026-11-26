# Catatan Keputusan Analisis

| ID | Keputusan | Alasan / status |
|---|---|---|
| ADR-001 | Fokus pada EDA deskriptif dan eksploratif | Tidak mengklaim inferensi kausal atau prediksi |
| ADR-002 | Data mentah tidak diubah | Menjaga keterlacakan sumber |
| ADR-003 | Nilai kosong tidak otomatis menjadi nol | Makna simbol harus dikonfirmasi dari sumber |
| ADR-004 | Outlier tidak otomatis dihapus | Perlu pemeriksaan konteks operasional |
| ADR-005 | Skema 16 kolom telah diverifikasi pada CSV gabungan | Uji integritas memeriksa 58 × 16, nama kolom, placeholder, missingness, duplikasi, dan celah waktu yang diketahui |

| ADR-006 | Tabel 7 dan Tabel 8 memiliki satu rekaman identik pada 20:51:43 | Dipertahankan dua kali pada data per sumber, satu kali pada dataset gabungan; jumlah menjadi 59 baris sumber dan 58 rekaman unik |
| ADR-007 | Tujuh placeholder `---` pada akselerasi tidak diubah menjadi nol | Placeholder dipetakan menjadi missing hanya pada salinan analisis numerik |
| ADR-008 | Empat kolom status kosong pada 26 rekaman Tabel 9–10 | Kolom tidak ditampilkan pada dua tabel tersebut; bukan bukti kegagalan sensor |
| ADR-009 | Timestamp analitis dibentuk dengan format eksplisit `%d/%m/%Y %H.%M.%S` | Hanya menyatukan tanggal dan waktu dalam tabel yang sama; bukan sinkronisasi lintas-sumber |
| ADR-010 | Tidak melakukan imputasi, scaling, encoding, atau winsorization secara otomatis | Transformasi hanya dilakukan bila ada kebutuhan analitis dan justifikasi domain |

| ADR-011 | `km` dan `m` adalah komponen satu besaran jarak tersisa menuju titik henti akhir; buat `distance_to_stop_m = km * 1000 + m` pada salinan analisis | Didukung Gambar 36 dan Bagian II.3 serta Tabel 6–10 laporan KNKT. Kolom mentah dipertahankan; `km` dan `m` dikeluarkan dari analisis statistik terpisah. Besaran gabungan bukan chainage absolut. Lihat `docs/02_data_understanding/source_validation_distance.md`; beberapa narasi chainage sumber tidak konsisten dan tidak direkonstruksi. |
