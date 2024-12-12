"""
Assuming we are able to generate code,
test that the logic of the generated code works
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


def sample_data(routing_field: int) -> dict:
    return {
        "groupping_id": "id_123",
        "groupping_id_1": "subid_456",
        "routing_field": routing_field,
        "numeric_field": "random_num",
    }


def test_conditional_1():
    """
    makes sure the router works with the conditional operations as intended
    no AB tests in this source file
    """
    experiment = load_experiment("unroutable_conditional.pyab")
    experiment(**sample_data(1))

    with pytest.raises(ExperimentConditionalFailedError):
        experiment(**sample_data(2))
