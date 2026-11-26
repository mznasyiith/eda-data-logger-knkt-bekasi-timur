# Ringkasan Hasil EDA Data Logger KNKT

## Sumber dan versi data
Transkripsi manual Tabel 6–10 Laporan KNKT KNKT.26.04.03.02.
Dataset analitis: 58 rekaman unik dan 16 kolom sumber.
Rentang waktu: 2026-04-27 20:51:18 sampai 2026-04-27 20:52:21.

## Definisi jarak
Kolom sumber km dan m digabung menjadi distance_to_stop_m = km × 1.000 + m.
Besaran ini adalah jarak tersisa menuju titik henti akhir, bukan chainage absolut atau jarak pengereman murni.

## Statistik deskriptif


                       n_valid     mean     50%      std   min      max
distance_to_stop_m          58  472.897  378.50  421.531  0.00  1341.00
Speed (km/h)                58   73.638   82.50   33.077  0.00   109.00
Acceleration (m/sec²)       51   -0.336   -0.38    0.203 -0.84     0.05
Load (amps)                 58   86.207  136.00   76.587  0.00   168.00
EAB BP (psi)                58   31.897   49.00   28.264  0.00    71.00
EAB BC (psi)                58   26.000    2.00   31.191  0.00    73.00

## Frekuensi kategori


- Throttle: {'T5': 17, 'Idle': 13, 'T7': 11, 'Off': 10, 'T4': 4, 'T6': 2, 'T1': 1}
- PCS Open: {'Closed': 32, 'Open': 26}
- IBS: {'Rel': 39, 'Appl': 19}
- DB Excit: {'Off': 32}
- Dir Call: {'For': 32}
- DB Set: {'No': 32}
- DB Star: {'No': 32}

## Kualitas dan keterbatasan data
Tujuh placeholder akselerasi tidak dihitung sebagai angka. Empat kolom status memiliki missingness struktural pada Tabel 9–10. Gap waktu 20:51:28–20:51:33 tidak diinterpolasi. Data merupakan satu kejadian dan satu sumber logger; hasil bersifat deskriptif dan tidak membuktikan hubungan kausal.

## Keputusan pembersihan dan transformasi
Data sumber tidak ditimpa. Kolom km dan m dipertahankan; fitur jarak gabungan dihitung pada salinan analisis. Tidak dilakukan imputasi atau winsorization.

## Kesimpulan eksploratif
Ringkasan ini menyajikan statistik dan frekuensi aktual dari pipeline yang dijalankan. Interpretasi operasional harus dibaca bersama laporan KNKT dan batas bukti proyek.
