from simulation.astronaut_model import Astronaut
from simulation.event_engine import simulate_day

from analytics.monte_carlo import run_monte_carlo_simulation
from analytics.risk_analysis import compute_risk_metrics

import matplotlib.pyplot as plt
import csv


print("Starting astronaut fatigue simulation...\n")

astronaut = Astronaut()
days = 30
all_day_data = []


# ---------------- Mission Simulation ----------------

for day in range(days):

    data = simulate_day(astronaut, day)
    data["day"] = day + 1
    all_day_data.append(data)

    print("Day", day + 1, data)


# ---------------- Save to CSV for Unity ----------------

csv_keys = [
    "day", "phase", "sleep", "workload", "eva_event",
    "fatigue", "stress", "cognition",
    "heart_rate", "oxygen_saturation", "respiration_rate"
]

with open("simulation_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=csv_keys, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(all_day_data)

print("\nSimulation results saved to simulation_results.csv")
print("\nSimulation finished\n")


# ---------------- Monte Carlo Sensitivity Analysis ----------------

print("\nRunning Monte Carlo Sensitivity Analysis...\n")

nominal_results = run_monte_carlo_simulation(1000, mission_type="nominal")
highstress_results = run_monte_carlo_simulation(1000, mission_type="high_stress")


nominal_metrics = compute_risk_metrics(nominal_results)
highstress_metrics = compute_risk_metrics(highstress_results)


print("Nominal Mission Risk:")
print("Average fatigue:", nominal_metrics["average_fatigue"])
print("Maximum fatigue:", nominal_metrics["max_fatigue"])
print("Minimum fatigue:", nominal_metrics["min_fatigue"])
print("Critical fatigue probability:", nominal_metrics["probability_critical_fatigue"])


print("\nHigh-Stress Mission Risk:")
print("Average fatigue:", highstress_metrics["average_fatigue"])
print("Maximum fatigue:", highstress_metrics["max_fatigue"])
print("Minimum fatigue:", highstress_metrics["min_fatigue"])
print("Critical fatigue probability:", highstress_metrics["probability_critical_fatigue"])


# ---------------- Mission Timeline Visualization ----------------

plt.figure()

plt.plot(astronaut.history["fatigue"], label="Fatigue")
plt.plot(astronaut.history["stress"], label="Stress")
plt.plot(astronaut.history["cognition"], label="Cognitive Performance")

plt.axvline(x=5, linestyle="--", label="Adaptation Phase Start")
plt.axvline(x=15, linestyle="--", label="Normal Operations Start")
plt.axvline(x=25, linestyle="--", label="High Workload Phase Start")

plt.title("Astronaut Health State Over Mission")
plt.xlabel("Mission Day")
plt.ylabel("Value")
plt.legend()
plt.savefig("mission_timeline.png")
plt.show()


# ---------------- Sensitivity Analysis Distribution ----------------

plt.figure()

plt.hist(nominal_results, bins=30, alpha=0.6, label="Nominal Mission")
plt.hist(highstress_results, bins=30, alpha=0.6, label="High-Stress Mission")

plt.title("Fatigue Risk Comparison (Monte Carlo)")
plt.xlabel("Final Mission Fatigue")
plt.ylabel("Number of Missions")
plt.legend()
plt.savefig("monte_carlo_comparison.png")
plt.show()

print("\nCharts saved: mission_timeline.png, monte_carlo_comparison.png")