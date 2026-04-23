import numpy as np


def compute_risk_metrics(fatigue_results):

    fatigue_array = np.array(fatigue_results)

    avg_fatigue = np.mean(fatigue_array)

    max_fatigue = np.max(fatigue_array)

    min_fatigue = np.min(fatigue_array)

    critical_threshold = 180

    risk_probability = np.sum(fatigue_array > critical_threshold) / len(fatigue_array)

    return {
        "average_fatigue": avg_fatigue,
        "max_fatigue": max_fatigue,
        "min_fatigue": min_fatigue,
        "probability_critical_fatigue": risk_probability
    }