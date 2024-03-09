import pytest

from pyab_experiment.binning.binning import deterministic_choice
from pyab_experiment.utils.stats import confidence_interval


@pytest.mark.parametrize(
    "trials, salt", [(100000, "_salt"), (200000, "_7"), (300000, "A"), (50000, "F")]
)
def test_deterministic_choice(trials, salt):
    """Test that groups are picked uniformly"""
    counter = {}
    groups = ["a", "b", "c"]

    for i in range(0, trials):
        group = deterministic_choice(f"{i}{salt}", population=groups)
        if group in counter:
            counter[group] += 1
        else:
            counter[group] = 1

    (low_estimate, hi_estimate) = confidence_interval(
        trials, p=1 / len(groups), confidence=0.999
    )
    for group in groups:
        assert low_estimate <= counter[group] / trials <= hi_estimate


@pytest.mark.parametrize(
    "trials, salt", [(100000, "_salt"), (200000, "_7"), (300000, "A"), (50000, "F")]
)
def test_weighted_deterministic_choice(trials, salt):
    """Test that groups are picked according to their weights"""
    counter = {}
    groups = ["a", "b", "c"]
    weights = [1, 2, 3]

    for i in range(0, trials):
        group = deterministic_choice(f"{i}{salt}", population=groups, weights=weights)
        if group in counter:
            counter[group] += 1
        else:
            counter[group] = 1

    for group, weight in zip(groups, weights):
        # different CI depending on weight
        (low_estimate, hi_estimate) = confidence_interval(
            trials, p=weight / sum(weights), confidence=0.999
        )
        assert low_estimate <= counter[group] / trials <= hi_estimate


def test_sequential_groups():
    """Test that groups that are picked with different salts (and same id) are
    uniformly distributted on sequential choices calls"""
    counter = {}
    groups1 = ["a1", "b1", "c1"]
    groups2 = ["a2", "b2", "c2"]
    groups3 = ["a3", "b3", "c3"]

    trials = 100000

    (low_estimate, hi_estimate) = confidence_interval(
        trials, p=1 / (len(groups1) * len(groups2) * len(groups3)), confidence=0.999
    )

    for i in range(0, trials):
        group1 = deterministic_choice(f"{i}_S1", population=groups1)
        group2 = deterministic_choice(f"{i}_S2", population=groups2)
        group3 = deterministic_choice(f"{i}_S3", population=groups3)

        group_key = f"{group1}{group2}{group3}"
        if group_key in counter:
            counter[group_key] += 1
        else:
            counter[group_key] = 1

    for group1 in groups1:
        for group2 in groups2:
            for group3 in groups3:
                assert (
                    low_estimate
                    <= counter[f"{group1}{group2}{group3}"] / trials
                    <= hi_estimate
                )


def test_not_random():
    """it goes without saying, but the same input_id
    should always give back the same group"""
    groups = ["a", "b", "c", "d", "e"]
    chosen_group = deterministic_choice("my_id_123", population=groups)

    for _ in range(100):
        assert chosen_group == deterministic_choice("my_id_123", population=groups)


@pytest.mark.parametrize(
    "trials, n_groups", [(1000000, 10), (1000000, 2000), (1000000, 10000)]
)
def test_large_group_numbers(trials, n_groups):
    """Test distr properties of larger number of groups"""
    counter = {}
    groups = [f"GRP_{i}" for i in range(n_groups)]

    (low_estimate, hi_estimate) = confidence_interval(
        trials, p=1 / len(groups), confidence=0.999
    )

    for i in range(0, trials):
        group = deterministic_choice(f"{i}_salted", population=groups)
        if group in counter:
            counter[group] += 1
        else:
            counter[group] = 1

    for group in groups:
        assert low_estimate <= counter[group] / trials <= hi_estimate
