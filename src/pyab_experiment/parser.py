"""parsing module"""
from pyab_experiment.data_structures.syntax_tree import ExperimentAST
from pyab_experiment.language.grammar import ExperimentParser
from pyab_experiment.language.lexer import ExperimentLexer


def parse(text: str) -> ExperimentAST:
    lexer = ExperimentLexer()
    parser = ExperimentParser()
    return parser.parse(lexer.tokenize(text))
