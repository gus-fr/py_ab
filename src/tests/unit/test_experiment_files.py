"""test the parsing, lexing, and codegen of the sample files created
the test only checks for errors, not the logic itself"""
from pathlib import Path

import pytest

from pyab_experiment.language.lexer import ExperimentLexer
from pyab_experiment.utils.wraper_functions import generate_code, parse_source

files_to_test = [
    "basic_experiment.pyab",
    "comments.pyab",
    "full_grammar.pyab",
    "salt.pyab",
    "splitters.pyab",
    "conditional.pyab",
    "conditional_test_1.pyab",
]


@pytest.mark.parametrize("file_name", files_to_test)
def test_generator(file_name):
    """all files should generate some code without problems"""
    with open(
        f"{Path(__file__).absolute().parent}/test_programs/{file_name}", "r"
    ) as fp:
        python_code = generate_code(fp.read())
        assert python_code is not None


@pytest.mark.parametrize("file_name", files_to_test)
def test_parsable_programs(file_name):
    """all files should parse withour syntaxerrors"""
    with open(
        f"{Path(__file__).absolute().parent}/test_programs/{file_name}", "r"
    ) as fp:
        ast = parse_source(fp.read())
        assert ast is not None


@pytest.mark.parametrize("file_name", files_to_test)
def test_lexer(file_name):
    """all files should lex without token errors (strange chars) errors"""
    with open(
        f"{Path(__file__).absolute().parent}/test_programs/{file_name}", "r"
    ) as fp:
        lexer = ExperimentLexer()
        assert len([token for token in lexer.tokenize(fp.read())]) > 0
