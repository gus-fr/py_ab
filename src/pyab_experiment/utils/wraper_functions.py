"""parsing module"""
from pyab_experiment.data_structures.syntax_tree import ExperimentAST
from pyab_experiment.language.grammar import ExperimentParser
from pyab_experiment.language.lexer import ExperimentLexer
from pyab_experiment.codegen.python_generator import PythonCodeGen


def parse(text: str) -> ExperimentAST:
    lexer = ExperimentLexer()
    parser = ExperimentParser()
    return parser.parse(lexer.tokenize(text))

def generate_code(text:str)->str:
    """end to end code generation
    high level spec comes in and python
    function comes out"""

    generator = PythonCodeGen(parse(text))
    return generator.generate()

