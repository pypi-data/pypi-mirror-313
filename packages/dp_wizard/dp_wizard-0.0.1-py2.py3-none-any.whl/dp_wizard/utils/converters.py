from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess


def convert_py_to_nb(python_str: str, execute: bool = False):
    """
    Given Python code as a string, returns a notebook as a string.
    Calls jupytext as a subprocess:
    Not ideal, but only the CLI is documented well.
    """
    with TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        py_path = temp_dir_path / "input.py"
        py_path.write_text(python_str)
        argv = (
            [
                "jupytext",
                "--from",
                ".py",
                "--to",
                ".ipynb",
                "--output",
                "-",
            ]
            + (["--execute"] if execute else [])
            + [str(py_path.absolute())]  # Input
        )
        try:
            result = subprocess.run(argv, check=True, text=True, capture_output=True)
        except subprocess.CalledProcessError:
            if not execute:
                # Might reach here if jupytext is not installed.
                # Error quickly instead of trying to recover.
                raise  # pragma: no cover
            # Install kernel if missing
            # TODO: Is there a better way to do this?
            subprocess.run(
                "python -m ipykernel install --name kernel_name --user".split(" "),
                check=True,
            )
            result = subprocess.run(argv, check=True, text=True, capture_output=True)

        return result.stdout.strip()
