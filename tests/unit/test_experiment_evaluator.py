"""Assuming we are able to generate code, test that the logic of the generated code works"""
from collections import Counter
from pathlib import Path

import pytest

from pyab_experiment.experiment_evaluator import ExperimentEvaluator
from pyab_experiment.utils.stats import confidence_interval


def load_experiment(file_name):
    with open(
        f"{Path(__file__).absolute().parent}/test_programs/{file_name}", "r"
    ) as fp:
        return ExperimentEvaluator(fp.read())


def sample_data(trials: int) -> list[dict]:
    return [
        {
            "groupping_id": f"id_{pid}",
            "groupping_id_1": f"subid_{pid+20}",
            "routing_field": pid % 10,
            "numeric_field": pid,
        }
        for pid in range(trials)
    ]


def test_conditional_1():
    """
    makes sure the router works with the conditional operations as intended
    no AB tests in this source file
    """
    experiment = load_experiment("conditional_test_1.pyab")
    group_ctr = Counter()

    for datapoint in sample_data(10000):
        group_ctr[experiment(**datapoint)] += 1

    assert group_ctr["G0"] == 1000
    assert group_ctr["G1"] == 1000
    assert group_ctr["G2-5"] == 4000
    assert group_ctr["G6+"] == 4000
    assert group_ctr["default_grp"] == 0  # to test all data points have been assigned


def test_splitter_test():
    """
    file has simple definition that conditions the weights of the splitter
    """
    experiment = load_experiment("splitter_test.pyab")
    group_ctr_a = Counter()
    group_ctr_other = Counter()
    trials = 10000
    for datapoint in sample_data(trials):
        group_ctr_a[experiment(my_id=datapoint.get("groupping_id"), field_1="a")] += 1
        group_ctr_other[
            experiment(my_id=datapoint.get("groupping_id"), field_1="sth_else")
        ] += 1

    (low_estimate, hi_estimate) = confidence_interval(trials, p=4 / 5, confidence=0.999)
    assert low_estimate <= group_ctr_a["Setting 1"] / trials <= hi_estimate
    (low_estimate, hi_estimate) = confidence_interval(trials, p=1 / 5, confidence=0.999)
    assert low_estimate <= group_ctr_a["Setting 2"] / trials <= hi_estimate

    (low_estimate, hi_estimate) = confidence_interval(trials, p=1 / 2, confidence=0.999)
    assert low_estimate <= group_ctr_other["Setting 1"] / trials <= hi_estimate
    (low_estimate, hi_estimate) = confidence_interval(trials, p=1 / 2, confidence=0.999)
    assert low_estimate <= group_ctr_other["Setting 2"] / trials <= hi_estimate
