import numpy as np


def sleep_duration(profile="normal"):

    if profile == "normal":
        return np.random.normal(7, 0.7)

    if profile == "high_stress":
        return np.random.normal(5.5, 1.2)

    if profile == "emergency":
        return np.random.normal(4, 1.5)


def workload_level():

    return np.random.gamma(2, 2)


def motion_sickness_probability():

    return np.random.poisson(0.2)


def sleep_interruption_event():

    # 25% probability sleep gets interrupted
    return np.random.binomial(1, 0.25)


def eva_event():

    # ~10% probability of EVA on a mission day
    return np.random.binomial(1, 0.1)