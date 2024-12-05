import re
from pathlib import Path
import subprocess
import pytest
from dp_wizard.utils.converters import convert_py_to_nb


fixtures_path = Path(__file__).parent.parent / "fixtures"


def norm_nb(nb_str):
    normed_nb_str = nb_str
    normed_nb_str = re.sub(r'"id": "[^"]+"', '"id": "12345678"', normed_nb_str)
    normed_nb_str = re.sub(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z",
        "2024-01-01T00:00:00.000000Z",
        normed_nb_str,
    )
    # language_info added when saved by VSCode:
    normed_nb_str = re.sub(r',\s+"language_info": \{[^}]*\}', "", normed_nb_str)
    # version will be different between dev environment and CI:
    normed_nb_str = re.sub(r'"version": "[^"]+"', '"version": "3.0.0"', normed_nb_str)
    return normed_nb_str.strip()


def test_convert_py_to_nb():
    python_str = (fixtures_path / "fake.py").read_text()
    actual_nb_str = convert_py_to_nb(python_str)
    expected_nb_str = (fixtures_path / "fake.ipynb").read_text()

    normed_actual_nb_str = norm_nb(actual_nb_str)
    normed_expected_nb_str = norm_nb(expected_nb_str)
    assert normed_actual_nb_str == normed_expected_nb_str


def test_convert_py_to_nb_execute():
    python_str = (fixtures_path / "fake.py").read_text()
    actual_nb_str = convert_py_to_nb(python_str, execute=True)
    expected_nb_str = (fixtures_path / "fake-executed.ipynb").read_text()

    normed_actual_nb_str = norm_nb(actual_nb_str)
    normed_expected_nb_str = norm_nb(expected_nb_str)
    assert normed_actual_nb_str == normed_expected_nb_str


def test_convert_py_to_nb_error():
    python_str = "Invalid python!"
    with pytest.raises(subprocess.CalledProcessError):
        convert_py_to_nb(python_str, execute=True)
