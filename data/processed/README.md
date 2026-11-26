# Processed Data

## Dataset
- File: `data_logger_knkt_tabel_6_10.csv`
- Source: KNKT Final Investigation Report `KNKT.26.04.03.02`
- Source tables: 6, 7, 8, 9, and 10 (printed pages 65–68).
- Schema: 16 columns.
- Source rows transcribed: 59.
- Unique merged rows: 58.

## Merge and provenance rules
- Table 7 and Table 8 both contain the same record at 20:51:43. The record is retained in the workbook's `Data_By_Source` sheet for source traceability and represented once in the merged CSV.
- There is no published record in these tables for 20:51:28–20:51:33. No interpolation or synthetic rows were added.
- Four status columns (`DB Excit`, `Dir Call`, `DB Set`, `DB Star`) are absent from Tables 9–10 and therefore null for those 26 rows. They are not imputed.
- Seven acceleration cells contain the source placeholder `---`; the token is preserved in the CSV.
- No values are changed, scaled, winsorized, or imputed.

## Reproduction
```python
import pandas as pd

df = pd.read_csv("data/processed/data_logger_knkt_tabel_6_10.csv")
print(df.shape)  # (58, 16)
```

The CSV is a transcription of tables printed in the KNKT report, not a raw export from the onboard logger. Cite the report and retain its original context when interpreting these records.
