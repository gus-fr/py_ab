"""Binomial CI estimates"""
from math import log, pi


def probit(alpha: float = 0.5) -> float:
    """Return the probit function.

    The probit function is the quantile function associated with
    the standard normal distribution.

    See `https://en.wikipedia.org/wiki/Probit for the approximation`_
    of using the logit function."""

    # our version of mypy doesn't have proper types on pow
    # ignore for now until we upgrade
    # see https://github.com/python/typeshed/issues/7733
    return (pi / 8) ** 0.5 * abs(log(alpha / (1 - alpha)))  # type: ignore


def confidence_interval(
    n: int = 10, p: float = 0.5, confidence: float = 0.95, method: str = "agresti-coull"
) -> tuple[float, float]:
    """Return the mean and the confidence interval of Bernoulli trials.
    See `https://en.wikipedia.org/wiki/Binomial_distribution#Confidence_intervals`_
    """
    alpha = 1 - confidence
    z = probit(alpha / 2)

    est_succ = p * n
    if method.lower() == "agresti-coull":
        n_prime = n + z**2
        p_prime = 1 / n_prime * (est_succ + (1 / 2) * z**2)
        interval = z * (p_prime * (1 - p_prime) / n_prime) ** 0.5
        return (p_prime - interval, p_prime + interval)
    elif method.lower() == "wald":
        interval = z * ((p * (1 - p)) / n) ** 0.5
        return p - interval, p + interval
    else:
        raise NotImplementedError(f"The method '{method}' is not implemented")
