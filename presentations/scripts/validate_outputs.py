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
slides = re.findall(r'<section(?:\s|>)', html_text)
assert len(slides) >= 15, f"Expected at least 15 slide sections, found {len(slides)}"
assert "Eksplorasi Data Logger KA 4B" in html_text, "Presentation title missing"

with pdf.open("rb") as stream:
    assert stream.read(5) == b"%PDF-", "Invalid PDF signature"

info = subprocess.run(
    ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True
).stdout
match = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
assert match and int(match.group(1)) >= 15, "PDF page count is missing or below 15"

print(f"Validated HTML ({len(slides)} slide sections) and PDF ({match.group(1)} pages).")
