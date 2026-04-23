from simulation.distributions import (
    sleep_duration,
    workload_level,
    motion_sickness_probability,
    sleep_interruption_event,
    eva_event
)

from simulation.mission_profile import get_mission_phase
from biogears.biogears_interface import generate_physiological_state


def simulate_day(astronaut, day):

    phase = get_mission_phase(day)

    if phase == "launch_phase":
        profile = "high_stress"

    elif phase == "adaptation_phase":
        profile = "normal"

    elif phase == "normal_operations":
        profile = "normal"

    else:
        profile = "high_stress"


    # ---------------- Sleep ----------------

    sleep = sleep_duration(profile)

    # Sleep interruption event
    if sleep_interruption_event():
        sleep -= 1.5
        astronaut.stress += 2

    astronaut.apply_sleep(sleep)


    # ---------------- Work ----------------

    workload = workload_level()

    if phase == "high_workload_phase":
        workload *= 1.5

    astronaut.apply_work(workload)


    # ---------------- EVA Event ----------------

    eva = False

    if eva_event():

        eva = True

        astronaut.fatigue += 8
        astronaut.stress += 5

        workload += 3


    # ---------------- Motion Sickness ----------------

    if motion_sickness_probability() > 0 and phase != "normal_operations":
        astronaut.apply_motion_sickness()


    # ---------------- Cognitive Update ----------------

    astronaut.update_cognition()

    astronaut.record_state()


    # ---------------- Physiology (BioGears Layer) ----------------

    physiology = generate_physiological_state(
        astronaut.fatigue,
        astronaut.stress
    )


    return {
        "phase": phase,
        "sleep": sleep,
        "workload": workload,
        "eva_event": eva,
        "fatigue": astronaut.fatigue,
        "stress": astronaut.stress,
        "cognition": astronaut.cognitive_performance,
        "heart_rate": physiology["heart_rate"],
        "oxygen_saturation": physiology["oxygen_saturation"],
        "respiration_rate": physiology["respiration_rate"]
    }