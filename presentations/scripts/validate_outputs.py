from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[1]
dist = root / "dist"
html = dist / "eda-knkt-bekasi-timur.html"
pdf = dist / "eda-knkt-bekasi-timur.pdf"

assert html.is_file() and html.stat().st_size > 10_000, "HTML missing or unexpectedly small"
assert pdf.is_file() and pdf.stat().st_size > 10_000, "PDF missing or unexpectedly small"

html_text = html.read_text(encoding="utf-8")
slides = re.findall(r'<section(?:\\s|>)', html_text)
assert len(slides) >= 15, f"Expected at least 15 slide sections, found {len(slides)}"
assert "Eksplorasi Data Logger Lokomotif KA 4B" in html_text, "Presentation title missing"

# Speaker notes are a required part of this explanatory deck.
notes = re.findall(r'<aside class="notes">', html_text)
assert len(notes) >= 15, f"Expected speaker notes on at least 15 slides, found {len(notes)}"

# Guard source-critical semantics and values against accidental presentation drift.
for required in (
    "20:51:28–20:51:33",
    "20:52:12",
    "20:52:19",
    "amps (A)",
    "Acceleration (m/sec²)",
    "58 rekaman unik",
    "73 psi",
):
    assert required in html_text, f"Required source-aligned content missing: {required}"

forbidden = (
    "distance_to_stop_m",
    "168 A tercatat",
    "kW",
)
for token in forbidden:
    if token == "kW":
        # kW may appear only in explanatory negation, never as a Load unit.
        assert "Load (amps)" in html_text, "Load unit label missing"
    elif token == "168 A tercatat":
        assert token not in html_text, "Stale current value found"
    else:
        assert token not in html_text, "Unsupported derived distance feature found"

with pdf.open("rb") as stream:
    assert stream.read(5) == b"%PDF-", "Invalid PDF signature"

info = subprocess.run(
    ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True
).stdout
match = re.search(r"^Pages:\\s+(\\d+)", info, re.MULTILINE)
assert match and int(match.group(1)) >= 15, "PDF page count is missing or below 15"

print(
    f"Validated HTML ({len(slides)} slides, {len(notes)} speaker notes) "
    f"and PDF ({match.group(1)} pages)."
)
