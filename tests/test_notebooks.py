from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"
EXPECTED_NOTEBOOKS = [
    "00_project_setup.ipynb",
    "01_problem_understanding.ipynb",
    "02_data_understanding.ipynb",
    "03_importing_and_inspecting.ipynb",
    "04_handling_missing_data.ipynb",
    "05_exploring_characteristics.ipynb",
    "06_data_transformation.ipynb",
    "07_visualizing_relationships.ipynb",
    "08_handling_outliers.ipynb",
    "09_findings_and_insights.ipynb",
]


@pytest.mark.parametrize("filename", EXPECTED_NOTEBOOKS)
def test_notebook_is_valid_json_and_python_cells_parse(filename):
    path = NOTEBOOK_DIR / filename
    notebook = json.loads(path.read_text(encoding="utf-8"))

    assert notebook["nbformat"] == 4
    assert isinstance(notebook["cells"], list)
    assert notebook["cells"]

    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            ast.parse("".join(cell["source"]), filename=f"{filename}:code-cell")


def test_all_expected_notebooks_exist():
    assert all((NOTEBOOK_DIR / name).is_file() for name in EXPECTED_NOTEBOOKS)
