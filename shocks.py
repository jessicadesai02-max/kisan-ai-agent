# shocks.py
# Person 2 owns this file

import random
from data import SHOCK_TYPES

class MausamShock:

    def __init__(self):
        self.shock_type = None
        self.active = False
        self.steps_remaining = 0
        self.severity = 0.0

    def trigger_random_shock(self, farm_state, difficulty):

        if difficulty == "easy":
            return None  # no shocks in easy task

        if difficulty == "medium":
            if random.random() < 0.8:  # 80% chance of shock
                shock = random.choice(list(SHOCK_TYPES.keys()))
                self.shock_type = shock
                self.active = True
                self.steps_remaining = SHOCK_TYPES[shock]["steps_to_respond"]
                self.severity = round(random.uniform(0.5, 1.0), 2)
                farm_state["shock_active"] = True
                farm_state["shock_type"] = shock
                return shock

        if difficulty == "hard":
            if random.random() < 0.5:  # 50% chance each step
                shock = random.choice(list(SHOCK_TYPES.keys()))
                self.shock_type = shock
                self.active = True
                self.steps_remaining = SHOCK_TYPES[shock]["steps_to_respond"]
                self.severity = round(random.uniform(0.7, 1.0), 2)
                farm_state["shock_active"] = True
                farm_state["shock_type"] = shock
                return shock

        return None

    def update(self, farm_state):
        if self.active:
            self.steps_remaining -= 1
            if self.steps_remaining <= 0:
                self.active = False
                farm_state["shock_active"] = False
                farm_state["shock_type"] = None