from pathlib import Path

import pytest

from pyab_experiment.utils.wraper_functions import generate_code


@pytest.mark.parametrize(
    "file_name",
    [
        "basic_experiment.pyab",
        "comments.pyab",
        "full_grammar.pyab",
        "salt.pyab",
        "splitters.pyab",
        "conditional.pyab",
    ],
)
def test_generator(file_name):
    """all files should generate some code without problems"""
    with open(
        f"{Path(__file__).absolute().parent}/test_programs/{file_name}", "r"
    ) as fp:
        python_code = generate_code(fp.read())
        assert python_code is not None
