"""
Assuming we are able to generate code,
test that when a conditional is not met, we raise an
ExperimentConditionalFailedError
"""

from pathlib import Path

import pytest

from pyab_experiment.codegen.python.custom_exceptions import (
    ExperimentConditionalFailedError,
)
from pyab_experiment.experiment_evaluator import ExperimentEvaluator


def load_experiment(file_name):
    with open(f"{Path(__file__).absolute().parent}/test_programs/{file_name}") as fp:
        return ExperimentEvaluator(fp.read())


def sample_data(field1: str, field2: str, field3: str, field4: tuple[str] = ()) -> dict:
    return {"field1": field1, "field2": field2, "field3": field3, "field4": field4}


def test_eq_field_comparison():
    """
    the experiment is set up in such a way that conditionals will fire if
    field 1 is = to field 2 or field 3
    """
    experiment = load_experiment("conditional_with_idents.pyab")
    value = experiment(**sample_data("b", "b", "b"))
    assert value == "group 1.1"

    with pytest.raises(ExperimentConditionalFailedError):
        value = experiment(**sample_data("b1", "b", "b"))

    value = experiment(**sample_data("b1", "b", "b1"))
    assert value == "group 2.1"

    value = experiment(**sample_data("a", "x", "x", ("a", "b", "c")))
    assert value == "group 3.1"
    value = experiment(**sample_data("b", "x", "x", ("a", "b", "c")))
    assert value == "group 3.2"
    value = experiment(**sample_data("c", "x", "x", ("a", "b", "c")))
    assert value == "group 3.3"
