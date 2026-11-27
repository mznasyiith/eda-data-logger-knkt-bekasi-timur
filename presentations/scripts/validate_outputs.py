from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess


class PresentationHTMLParser(HTMLParser):
    """Collect rendered slide text and structural counts from reveal.js HTML."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.section_count = 0
        self.notes_count = 0
        self._section_depth = 0
        self._first_slide_depth = None
        self.first_slide_parts = []
        self.visible_parts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())

        if tag == "section":
            self.section_count += 1
            self._section_depth += 1
            if self._first_slide_depth is None:
                self._first_slide_depth = self._section_depth

        if "notes" in classes:
            self.notes_count += 1

    def handle_endtag(self, tag):
        if tag == "section" and self._section_depth:
            self._section_depth -= 1

    def handle_data(self, data):
        self.visible_parts.append(data)
        if self._first_slide_depth is not None and self._section_depth >= self._first_slide_depth:
            self.first_slide_parts.append(data)


def normalized_text(parts):
    return " ".join(" ".join(parts).split())


root = Path(__file__).resolve().parents[1]
dist = root / "dist"
html = dist / "eda-knkt-bekasi-timur.html"
pdf = dist / "eda-knkt-bekasi-timur.pdf"

assert html.is_file() and html.stat().st_size > 10_000, "HTML missing or unexpectedly small"
assert pdf.is_file() and pdf.stat().st_size > 10_000, "PDF missing or unexpectedly small"

parser = PresentationHTMLParser()
parser.feed(html.read_text(encoding="utf-8"))
parser.close()

slides = parser.section_count
notes = parser.notes_count
all_text = normalized_text(parser.visible_parts)
cover_text = normalized_text(parser.first_slide_parts)

assert slides >= 30, f"Expected at least 30 slide sections, found {slides}"
assert "Laporan Exploratory Data Analysis (EDA)" in all_text, "Presentation title missing"
assert "Dosen:" in cover_text, "Lecturer label missing from rendered cover"\nassert "Dr. Giat Karyono, M.Kom" in cover_text, "Lecturer name missing from rendered cover"
assert "Disusun oleh:" in cover_text, "Author label missing from rendered cover"\nassert "MUHAMMAD ZA’IIMUN NASYIITH" in cover_text, "Author name missing from rendered cover"

assert notes >= 30, f"Expected speaker notes on at least 30 slides, found {notes}"

# Guard source-critical semantics and values against accidental presentation drift.
for required in (
    "Bab 1 — Pendahuluan & memahami masalah",
    "Bab 2 — Memahami data",
    "Bab 3 — Memuat & memeriksa data",
    "Bab 4 — Penanganan data yang hilang",
    "Bab 5 — Mengeksplorasi karakteristik data",
    "Bab 6 — Transformasi data: kapan diperlukan?",
    "Bab 7 — Visualisasi hubungan data",
    "Bab 8 — Penanganan pencilan",
    "Bab 9 — Komunikasi temuan dan insight",
    "20:51:28–20:51:33",
    "20:52:12",
    "20:52:19",
    "ampere",
    "Acceleration (m/sec²)",
    "58 rekaman unik",
    "73 psi",
):
    assert required in all_text, f"Required source-aligned content missing: {required}"

assert "distance_to_stop_m" not in all_text, "Unsupported derived distance feature found"
assert "Load (A)" in all_text, "Load unit label missing"

with pdf.open("rb") as stream:
    assert stream.read(5) == b"%PDF-", "Invalid PDF signature"

info = subprocess.run(
    ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True
).stdout
match = re.search(r"^Pages:[ \\t]+([0-9]+)$", info, re.MULTILINE)
assert match and int(match.group(1)) >= 15, "PDF page count is missing or below 15"

print(
    f"Validated HTML ({slides} slide sections, {notes} speaker notes) "
    f"and PDF ({match.group(1)} pages)."
)
