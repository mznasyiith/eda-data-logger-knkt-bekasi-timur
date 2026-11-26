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
- The selected Tables 6–10 do not include timestamps 20:51:28–20:51:33. These six records are present in Appendix 7, the full Data Logger table after master-time adjustment, but are intentionally outside this CSV's scope. The seven-second interval is therefore a boundary of the selected-table subset, not proof that the records are absent from the complete KNKT report.
- Appendix 7 also presents the four status fields for the complete logger sequence. In this selected-table CSV, `DB Excit`, `Dir Call`, `DB Set`, and `DB Star` are blank for 26 rows because Tables 9–10 omit those columns. Appendix 7 uses the header `DB Start`; this naming difference must be reconciled before importing its values.
- No interpolation or synthetic rows were added.
- Seven acceleration cells contain the source placeholder `---`; the token is preserved in the CSV.
- No values are scaled, winsorized, or imputed. The transcription correction at 20:51:36 is 160 A as shown in the KNKT source table.

## Reproduction

```python
import pandas as pd

df = pd.read_csv("data/processed/data_logger_knkt_tabel_6_10.csv")
print(df.shape)  # (58, 16)
```

The CSV is a transcription of Tables 6–10 printed in the KNKT report, not a raw export from the onboard logger and not the complete 64-record Appendix 7 table. Cite the report and retain its original context when interpreting these records.
