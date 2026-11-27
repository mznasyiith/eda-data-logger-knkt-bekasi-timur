from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import tempfile

from PIL import Image, ImageStat


class PresentationHTMLParser(HTMLParser):
    """Collect rendered slide text and structural counts from reveal.js HTML."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.section_count = 0
        self.notes_count = 0
        self._section_depth = 0
        self.slide_parts = []
        self._current_slide_parts = None
        self.visible_parts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        if tag == "section":
            self.section_count += 1
            if self._section_depth == 0:
                self._current_slide_parts = []
                self.slide_parts.append(self._current_slide_parts)
            self._section_depth += 1
        if "notes" in classes:
            self.notes_count += 1

    def handle_endtag(self, tag):
        if tag == "section" and self._section_depth:
            self._section_depth -= 1
            if self._section_depth == 0:
                self._current_slide_parts = None

    def handle_data(self, data):
        self.visible_parts.append(data)
        if self._current_slide_parts is not None:
            self._current_slide_parts.append(data)


def normalized_text(parts):
    return " ".join(" ".join(parts).split())


root = Path(__file__).resolve().parents[1]
dist = root / "dist"
html = dist / "eda-knkt-bekasi-timur.html"
pdf = dist / "eda-knkt-bekasi-timur.pdf"

assert html.is_file() and html.stat().st_size > 10_000, "HTML missing or unexpectedly small"
assert pdf.is_file() and pdf.stat().st_size > 10_000, "PDF missing or unexpectedly small"

html_source = html.read_text(encoding="utf-8")
parser = PresentationHTMLParser()
parser.feed(html_source)
parser.close()

slides = parser.section_count
notes = parser.notes_count
all_text = normalized_text(parser.visible_parts)
cover_slides = [
    normalized_text(parts)
    for parts in parser.slide_parts
    if "Analisis Data Logger Lokomotif KA 4B" in normalized_text(parts)
]
assert len(cover_slides) == 1, (
    f"Expected exactly one authored cover slide, found {len(cover_slides)}"
)
cover_text = cover_slides[0]

assert slides >= 30, f"Expected at least 30 slide sections, found {slides}"
assert "Laporan Exploratory Data Analysis (EDA)" in html_source, "HTML document title missing"
assert "Dosen:" in cover_text and "Dr. Giat Karyono, M.Kom" in cover_text, "Lecturer credit missing from cover"
assert "Disusun oleh:" in cover_text and "MUHAMMAD ZA’IIMUN NASYIITH" in cover_text, "Author credit missing from cover"
assert notes >= 30, f"Expected speaker notes on at least 30 slides, found {notes}"

for forbidden in ("::: {.column", ":::: {.columns", "::: {.notes}"):
    assert forbidden not in all_text, f"Raw Markdown fence leaked into HTML: {forbidden}"

raw_html_pattern = re.compile(
    r"</?(?:div|p|span|strong|em|ul|ol|li|img|figure|figcaption|br|hr)(?:[ >])[^>]*>",
    re.IGNORECASE,
)
html_markup_leaks = raw_html_pattern.findall(all_text)
assert not html_markup_leaks, (
    "Raw HTML markup leaked into visible HTML slide text: "
    + ", ".join(html_markup_leaks[:5])
)

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
    "Load (A)",
):
    assert required in all_text, f"Required source-aligned content missing: {required}"

assert "distance_to_stop_m" not in all_text, "Unsupported derived distance feature found"

with pdf.open("rb") as stream:
    assert stream.read(5) == b"%PDF-", "Invalid PDF signature"

info = subprocess.run(
    ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True
).stdout
match = re.search(r"^Pages:[ \\t]+([0-9]+)$", info, re.MULTILINE)
assert match, "PDF page count is missing"
page_count = int(match.group(1))
assert 30 <= page_count <= slides + 2, (
    f"Unexpected PDF page count {page_count} for {slides} slide sections"
)

pdf_text = subprocess.run(
    ["pdftotext", "-layout", str(pdf), "-"], check=True, capture_output=True, text=True
).stdout
for leaked in ("::: {.column", ":::: {.columns", "::: {.notes}"):
    assert leaked not in pdf_text, f"Raw Markdown syntax leaked into PDF: {leaked}"

pdf_markup_leaks = raw_html_pattern.findall(pdf_text)
assert not pdf_markup_leaks, (
    "Raw HTML markup leaked into PDF text: "
    + ", ".join(pdf_markup_leaks[:8])
)

pdf_pages = [normalized_text(page.splitlines()) for page in pdf_text.split("\f") if page.strip()]
assert len(pdf_pages) == page_count, (
    f"Expected text extraction for all {page_count} PDF pages, found {len(pdf_pages)}"
)
assert "Analisis Data Logger Lokomotif KA 4B" in pdf_pages[0], (
    "PDF first page is not the authored cover"
)
assert sum("Analisis Data Logger Lokomotif KA 4B" in page for page in pdf_pages) == 1, (
    "Duplicate cover/title detected in PDF"
)

with tempfile.TemporaryDirectory(prefix="eda-pdf-audit-") as temp_dir:
    prefix = str(Path(temp_dir) / "page")
    subprocess.run(
        ["pdftoppm", "-r", "36", "-png", str(pdf), prefix],
        check=True, capture_output=True,
    )
    rendered_pages = sorted(Path(temp_dir).glob("page-*.png"))
    assert len(rendered_pages) == page_count, "Not all PDF pages could be rasterized"

    for index, page_path in enumerate(rendered_pages, start=1):
        with Image.open(page_path) as image:
            rgb = image.convert("RGB")
            width, height = rgb.size
            ratio = width / height
            assert 1.72 <= ratio <= 1.84, (
                f"Page {index} has unexpected aspect ratio {ratio:.3f}"
            )
            gray = rgb.convert("L")
            extrema = ImageStat.Stat(gray).extrema[0]
            dark_pixels = sum(1 for value in gray.getdata() if value < 235)
            dark_ratio = dark_pixels / (width * height)
            assert extrema[0] < 220 and dark_ratio > 0.002, (
                f"Page {index} appears blank or nearly blank "
                f"(dark-pixel ratio={dark_ratio:.4f})"
            )

print(
    f"Validated HTML ({slides} sections, {notes} speaker notes) and "
    f"PDF ({page_count} nonblank 16:9 pages; raw Markdown/HTML leakage and duplicate cover checked)."
)
