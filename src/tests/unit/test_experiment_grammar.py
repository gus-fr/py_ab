from pathlib import Path

import pytest

from pyab_experiment.parser import parse


@pytest.mark.parametrize(
    "file_name",
    [
        "basic_experiment.pyab",
        "comments.pyab",
        "full_grammar.pyab",
        "salt.pyab",
        "splitters.pyab",
        "conditional.pyab"
    ],
)
def test_parsable_programs(file_name):
    """all files should parse withour syntaxerrors"""
    with open(
        f"{Path(__file__).absolute().parent}/test_programs/{file_name}", "r"
    ) as fp:
        ast = parse(fp.read())
        assert ast is not None
