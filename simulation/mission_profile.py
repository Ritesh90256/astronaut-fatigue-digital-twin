def get_mission_phase(day):

    if day < 5:
        return "launch_phase"

    elif day < 15:
        return "adaptation_phase"

    elif day < 25:
        return "normal_operations"

    else:
        return "high_workload_phase"



def get_mission_parameters(mission_type="nominal"):

    if mission_type == "nominal":

        return {
            "sleep_interruption_prob": 0.25,
            "eva_probability": 0.1,
            "workload_multiplier": 1.0
        }

    elif mission_type == "high_stress":

        return {
            "sleep_interruption_prob": 0.45,
            "eva_probability": 0.2,
            "workload_multiplier": 1.4
        }