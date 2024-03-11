"""module that has the group splitting functions"""

import hashlib
from bisect import bisect
from itertools import accumulate
from math import floor as _floor
from math import isfinite
from random import choices
from typing import TypeVar

T = TypeVar("T")


def deterministic_proba(input_string: str) -> float:
    """gives a deterministic number in the range [0.0, 1.0) based on
    the input string. The idea is that if we give different strings
    we'll get a float in [0.0, 1.0), based on an uniform distribution

    Args:
        input_string: the string to derive a float from
    Returns:
        float: a number in the range [0.0, 1.0), picked uniformly
        from the space of all strings
    """
    digest = hashlib.md5(input_string.encode("ascii")).hexdigest()
    max_int = 0x100000000
    high_bits = int(digest[:8], 16)  # make an int of the highest 8 hex chars
    return (
        high_bits / max_int
    )  # divide by 1 over the fully packed 4 byte hex chars (FFFFFFFF)


def deterministic_choice(
    input_id: str | None,
    population: list[T],
    weights: list[float] | None = None,
    *,
    cum_weights: list[float] | None = None,
) -> T:
    """like random.choices, but for a
        deterministic hash function instead of a random number generator
        Implementation details follows the random.choices one very closely

        as a cute feature, if no input_id is given, the fn falls back to the
        classic choices call

        N.B - since this function is deterministic, we can only sensibly choose 1
        item with replacement from the population (all other items would be identical
        to the first) so the k parameter is fixed at 1, and we return a single item
        vs a collection like in random.choices
    Args:
        input_id: str|None: if None returns the classic random.choices. otherwise
        computes a deterministic number of k groups (based on the input_id).
        groups are chosen proportional to the weight, and uniformly across the space
        of all input_ids
        population (list[str]): list of items to choose from
        weights (list[float] | None, optional): how much weight
            to give to each item in the population
        cum_weights (list[float]| None, optional): like weights but cumulative
    """

    n = len(population)
    if input_id is None:
        return choices(
            population=population, weights=weights, cum_weights=cum_weights, k=1
        )[0]

    if cum_weights is None:
        if weights is None:
            return population[_floor(deterministic_proba(input_id) * n)]

        cum_weights = list(accumulate(weights))
    elif weights is not None:
        raise TypeError("Cannot specify both weights and cumulative weights")

    if len(cum_weights) != n:
        raise ValueError("The number of weights does not match the population")

    total = cum_weights[-1] + 0.0  # convert to float
    if total <= 0.0:
        raise ValueError("Total of weights must be greater than zero")

    if not isfinite(total):
        raise ValueError("Total of weights must be finite")
    hi = n - 1
    return population[bisect(cum_weights, deterministic_proba(input_id) * total, 0, hi)]
