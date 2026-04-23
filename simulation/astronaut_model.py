class Astronaut:

    def __init__(self):

        # physiological states
        self.fatigue = 0
        self.sleep_debt = 0
        self.stress = 0

        # performance state
        self.cognitive_performance = 100

        # history storage
        self.history = {
            "fatigue": [],
            "sleep_debt": [],
            "stress": [],
            "cognition": []
        }


    def apply_sleep(self, sleep_hours):

        optimal_sleep = 8
        deficit = optimal_sleep - sleep_hours

        if deficit > 0:
            self.sleep_debt += deficit
            self.fatigue += deficit * 1.5
        else:
            self.fatigue *= 0.9


    def apply_work(self, workload):

        self.fatigue += workload
        self.stress += workload * 0.5


    def apply_motion_sickness(self):

        self.fatigue += 2
        self.stress += 3


    def update_cognition(self):

        fatigue_effect = self.fatigue * 0.4
        stress_effect = self.stress * 0.6

        cognition = 100 - fatigue_effect - stress_effect

        self.cognitive_performance = max(0, cognition)


    def record_state(self):

        self.history["fatigue"].append(self.fatigue)
        self.history["sleep_debt"].append(self.sleep_debt)
        self.history["stress"].append(self.stress)
        self.history["cognition"].append(self.cognitive_performance)