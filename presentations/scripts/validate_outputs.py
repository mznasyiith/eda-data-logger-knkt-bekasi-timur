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
# Reveal.js slide sections are emitted as HTML <section> elements.
slides = html_text.count("<section")
assert slides >= 15, f"Expected at least 15 slide sections, found {slides}"
assert "Eksplorasi Data Logger Lokomotif KA 4B" in html_text, "Presentation title missing"

# Quarto/reveal.js speaker notes are rendered as notes asides.
notes = html_text.count('class="notes"')
assert notes >= 15, f"Expected speaker notes on at least 15 slides, found {notes}"

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

assert "distance_to_stop_m" not in html_text, "Unsupported derived distance feature found"
assert "Load (amps)" in html_text, "Load unit label missing"

with pdf.open("rb") as stream:
    assert stream.read(5) == b"%PDF-", "Invalid PDF signature"

info = subprocess.run(
    ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True
).stdout
match = re.search(r"^Pages:\\s+(\\d+)", info, re.MULTILINE)
assert match and int(match.group(1)) >= 15, "PDF page count is missing or below 15"

print(
    f"Validated HTML ({slides} slide sections, {notes} speaker notes) "
    f"and PDF ({match.group(1)} pages)."
)
