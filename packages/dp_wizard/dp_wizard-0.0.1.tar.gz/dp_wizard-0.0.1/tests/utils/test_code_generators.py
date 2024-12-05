from tempfile import NamedTemporaryFile
import subprocess
from pathlib import Path
import pytest
import opendp.prelude as dp
from dp_wizard.utils.code_generators import (
    Template,
    ScriptGenerator,
    NotebookGenerator,
    AnalysisPlan,
    AnalysisPlanColumn,
)


fixtures_path = Path(__file__).parent.parent / "fixtures"
fake_csv = "tests/fixtures/fake.csv"


def test_param_conflict():
    with pytest.raises(Exception, match=r"mutually exclusive"):
        Template("context", template="Not allowed if path present")


def test_fill_expressions():
    template = Template(None, template="No one VERB the ADJ NOUN!")
    filled = template.fill_expressions(
        VERB="expects",
        ADJ="Spanish",
        NOUN="Inquisition",
    ).finish()
    assert filled == "No one expects the Spanish Inquisition!"


def test_fill_expressions_missing_slot_in_template():
    template = Template(None, template="No one ... the ADJ NOUN!")
    with pytest.raises(Exception, match=r"No 'VERB' slot to fill with 'expects'"):
        template.fill_expressions(
            VERB="expects",
            ADJ="Spanish",
            NOUN="Inquisition",
        ).finish()


def test_fill_expressions_extra_slot_in_template():
    template = Template(None, template="No one VERB ARTICLE ADJ NOUN!")
    with pytest.raises(Exception, match=r"'ARTICLE' slot not filled"):
        template.fill_expressions(
            VERB="expects",
            ADJ="Spanish",
            NOUN="Inquisition",
        ).finish()


def test_fill_values():
    template = Template(None, template="assert [STRING] * NUM == LIST")
    filled = template.fill_values(
        STRING="🙂",
        NUM=3,
        LIST=["🙂", "🙂", "🙂"],
    ).finish()
    assert filled == "assert ['🙂'] * 3 == ['🙂', '🙂', '🙂']"


def test_fill_values_missing_slot_in_template():
    template = Template(None, template="assert [STRING] * ... == LIST")
    with pytest.raises(Exception, match=r"No 'NUM' slot to fill with '3'"):
        template.fill_values(
            STRING="🙂",
            NUM=3,
            LIST=["🙂", "🙂", "🙂"],
        ).finish()


def test_fill_values_extra_slot_in_template():
    template = Template(None, template="CMD [STRING] * NUM == LIST")
    with pytest.raises(Exception, match=r"'CMD' slot not filled"):
        template.fill_values(
            STRING="🙂",
            NUM=3,
            LIST=["🙂", "🙂", "🙂"],
        ).finish()


def test_fill_blocks():
    # "OK" is less than three characters, so it is not a slot.
    template = Template(
        None,
        template="""# MixedCase is OK

FIRST

with fake:
    SECOND
    if True:
        THIRD
""",
    )
    template.fill_blocks(
        FIRST="\n".join(f"import {i}" for i in "abc"),
        SECOND="\n".join(f"f({i})" for i in "123"),
        THIRD="\n".join(f"{i}()" for i in "xyz"),
    )
    assert (
        template.finish()
        == """# MixedCase is OK

import a
import b
import c

with fake:
    f(1)
    f(2)
    f(3)
    if True:
        x()
        y()
        z()
"""
    )


def test_fill_blocks_missing_slot_in_template_alone():
    template = Template(None, template="No block slot")
    with pytest.raises(Exception, match=r"No 'SLOT' slot"):
        template.fill_blocks(SLOT="placeholder").finish()


def test_fill_blocks_missing_slot_in_template_not_alone():
    template = Template(None, template="No block SLOT")
    with pytest.raises(
        Exception, match=r"Block slots must be alone on line; No 'SLOT' slot"
    ):
        template.fill_blocks(SLOT="placeholder").finish()


def test_fill_blocks_extra_slot_in_template():
    template = Template(None, template="EXTRA\nSLOT")
    with pytest.raises(Exception, match=r"'EXTRA' slot not filled"):
        template.fill_blocks(SLOT="placeholder").finish()


def test_make_notebook():
    notebook = NotebookGenerator(
        AnalysisPlan(
            csv_path=fake_csv,
            contributions=1,
            epsilon=1,
            columns={
                # For a strong test, use a column whose name
                # doesn't work as a python identifier.
                "hw-number": AnalysisPlanColumn(
                    lower_bound=5,
                    upper_bound=15,
                    bin_count=20,
                    weight=4,
                )
            },
        )
    ).make_py()
    print(notebook)
    globals = {}
    exec(notebook, globals)
    assert isinstance(globals["context"], dp.Context)


def test_make_script():
    script = ScriptGenerator(
        AnalysisPlan(
            csv_path=None,
            contributions=1,
            epsilon=1,
            columns={
                "hw-number": AnalysisPlanColumn(
                    lower_bound=5,
                    upper_bound=15,
                    bin_count=20,
                    weight=4,
                )
            },
        )
    ).make_py()
    print(script)

    # Make sure jupytext formatting doesn't bleed into the script.
    # https://jupytext.readthedocs.io/en/latest/formats-scripts.html#the-light-format
    assert "# -" not in script
    assert "# +" not in script

    with NamedTemporaryFile(mode="w") as fp:
        fp.write(script)
        fp.flush()

        result = subprocess.run(
            ["python", fp.name, "--csv", fake_csv], capture_output=True
        )
        assert result.returncode == 0
        output = result.stdout.decode()
        print(output)
        assert "DP counts for hw-number" in output
        assert "95% confidence interval 3.3" in output
        assert "hw_number_bin" in output
