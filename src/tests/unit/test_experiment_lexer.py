from pathlib import Path

import pytest

from pyab_experiment.language.lexer import ExperimentLexer


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
def test_lexer(file_name):
    """all files should lex without token errors (strange chars) errors"""
    with open(
        f"{Path(__file__).absolute().parent}/test_programs/{file_name}", "r"
    ) as fp:
        lexer = ExperimentLexer()
        assert len([token for token in lexer.tokenize(fp.read())])>0
