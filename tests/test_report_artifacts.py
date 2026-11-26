from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT = REPO_ROOT / "reports" / "Laporan_EDA_KNKT_Bekasi_Timur.md"
OUTPUTS = REPO_ROOT / "outputs"


def test_every_local_report_image_reference_exists():
    text = REPORT.read_text(encoding="utf-8")
    references = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    local_images = [item for item in references if not item.startswith(("http://", "https://"))]
    assert local_images, "The report should contain local generated-image references."
    missing = [item for item in local_images if not (REPORT.parent / item).is_file()]
    assert not missing, f"Missing report image artifacts: {missing}"


def test_required_visuals_are_generated():
    required = [
        "bab_ii/pipeline_akuisisi_data.png",
        "bab_ii/matriks_data_ke_pertanyaan.png",
        "bab_ii/ringkasan_skema_dataset.png",
        "bab_iii/scorecard_struktur_dataset.png",
        "bab_iii/cuplikan_data_mentah.png",
        "bab_iii/distribusi_tipe_data_raw.png",
        "bab_iii/rentang_minimum_maksimum.png",
        "bab_iv/missingness_matrix.png",
        "bab_iv/missingness_kolom_status.png",
        "bab_iv/dampak_deduplikasi.png",
        "bab_v/boxplot_mean_median.png",
        "bab_v/ecdf_variabel_numerik.png",
        "bab_v/skewness_kurtosis.png",
        "bab_vi/alur_transformasi_aktual.png",
        "bab_vi/pemetaan_tipe_dan_konversi.png",
        "bab_vii/multi_panel_parameter_waktu.png",
        "bab_vii/categorical_state_timeline.png",
        "bab_vii/scatter_hubungan_parameter.png",
        "bab_viii/jumlah_kandidat_iqr.png",
        "bab_viii/konteks_temporal_parameter.png",
        "bab_ix/decision_matrix_bukti_lanjutan.png",
        "bab_ix/scorecard_keterbatasan.png",
    ]
    missing = [item for item in required if not (OUTPUTS / item).is_file()]
    assert not missing, f"Required visual artifacts were not generated: {missing}"


def test_categorical_timeline_generator_does_not_create_missing_category():
    source = (REPO_ROOT / "scripts" / "generate_visuals.py").read_text(encoding="utf-8")
    assert 'df[col].fillna("Tidak tersedia")' not in source
    assert "observed = df[col].notna()" in source
    assert "Nilai kosong ditampilkan sebagai gap" in source
    assert "intervals[position] == 1" in source

def test_local_markdown_and_html_links_resolve():
    from urllib.parse import unquote, urlsplit

    import re

    markdown_files = list(REPO_ROOT.rglob("*.md"))
    broken = []
    markdown_link = re.compile(r"(?<!!)\\[[^\\]]+\\]\\(([^)]+)\\)")
    html_link = re.compile(r"""(?:href|src)=["']([^"']+)["']""", re.IGNORECASE)

    for source in markdown_files:
        content = source.read_text(encoding="utf-8")
        targets = markdown_link.findall(content) + html_link.findall(content)
        for raw_target in targets:
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            resolved = (source.parent / unquote(parsed.path)).resolve()
            if not resolved.exists():
                broken.append(f"{source.relative_to(REPO_ROOT)} -> {target}")

    assert not broken, "Broken local documentation links: " + "; ".join(broken)
