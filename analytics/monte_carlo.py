from simulation.astronaut_model import Astronaut
from simulation.event_engine import simulate_day
import biogears.biogears_interface as bg_iface


def run_monte_carlo_simulation(num_runs=1000, mission_days=30, mission_type="nominal"):

    fatigue_results = []

    # Force fallback mode for Monte Carlo — 1000 SSH calls would take hours
    # Real BioGears is used only for the main 30-day mission simulation
    bg_iface.SIMULATION_MODE = True

    for run in range(num_runs):

        astronaut = Astronaut()

        for day in range(mission_days):

            # High-stress missions amplify workload
            if mission_type == "high_stress":
                astronaut.stress += 1

            simulate_day(astronaut, day)

        fatigue_results.append(astronaut.fatigue)

    # Restore real BioGears mode after Monte Carlo
    bg_iface.SIMULATION_MODE = False

    return fatigue_results