from pathlib import Path
from argparse import ArgumentTypeError

import pytest

from dp_wizard.utils.argparse_helpers import _get_arg_parser, _existing_csv_type


fixtures_path = Path(__file__).parent.parent / "fixtures"


def test_help():
    help = (
        _get_arg_parser()
        .format_help()
        # argparse doesn't actually know the name of the script
        # and inserts the name of the running program instead.
        .replace("__main__.py", "dp-wizard")
        .replace("pytest", "dp-wizard")
        # Text is different under Python 3.9:
        .replace("optional arguments:", "options:")
    )
    print(help)

    root_path = Path(__file__).parent.parent.parent

    readme_md = (root_path / "README.md").read_text()
    assert help in readme_md

    readme_pypi_md = (root_path / "README-PYPI.md").read_text()
    assert help in readme_pypi_md


def test_arg_validation_no_file():
    with pytest.raises(ArgumentTypeError, match="No such file: no-such-file"):
        _existing_csv_type("no-such-file")


def test_arg_validation_not_csv():
    with pytest.raises(ArgumentTypeError, match='Must have ".csv" extension:'):
        _existing_csv_type(fixtures_path / "fake.ipynb")


def test_arg_validation_works():
    path = _existing_csv_type(fixtures_path / "fake.csv")
    assert path.name == "fake.csv"
