import random
from dataclasses import dataclass
from rewards import calculate_step_reward
from shocks import MausamShock


@dataclass
class FarmState:
    soil_moisture: int
    budget: int
    weather: str
    season: str
    crop: str
    pest_alert: bool
    days_to_harvest: int
    mandi_price: int


class FarmEnv:

    def __init__(self):
        self.reset()

    # Crop database
    CROP_DATA = {
        "winter": {
            "wheat": {"days": 90, "price": (18, 25)},
            "potato": {"days": 80, "price": (15, 22)}
        },
        "monsoon": {
            "rice": {"days": 100, "price": (20, 30)}
        },
        "summer": {
            "maize": {"days": 85, "price": (18, 26)},
            "tomato": {"days": 70, "price": (25, 40)},
            "mango": {"days": 120, "price": (40, 70)}
        }
    }

    # Start new farm
    def reset(self):

        season = random.choice(["winter", "summer", "monsoon"])
        crop = random.choice(list(self.CROP_DATA[season].keys()))

        crop_info = self.CROP_DATA[season][crop]

        self.state_data = FarmState(
            soil_moisture=50,
            budget=5000,
            weather="sunny",
            season=season,
            crop=crop,
            pest_alert=False,
            days_to_harvest=crop_info["days"],
            mandi_price=random.randint(*crop_info["price"])
        )

        return self.state()

    def state(self):
        return self.state_data.__dict__

    # RL Step
    def step(self, action):

        reward = 0
        done = False

        tool = action.get("tool")
        params = action.get("params", {})

        if tool == "irrigate":
            reward += self.irrigate(**params)

        elif tool == "apply_pesticide":
            reward += self.apply_pesticide(**params)

        elif tool == "apply_fertilizer":
            reward += self.apply_fertilizer(**params)

        elif tool == "sell_crop":
            reward += self.sell_crop(**params)

        self.update_environment()

        if self.state_data.days_to_harvest <= 0:
            done = True

        return self.state(), reward, done, {}

    # ---------------- TOOLS ----------------

    def check_weather(self):
        return self.state_data.weather

    def check_soil_moisture(self):
        return self.state_data.soil_moisture

    def irrigate(self, amount):

        cost = amount * 2

        if self.state_data.budget < cost:
            return -2

        self.state_data.soil_moisture += amount
        self.state_data.budget -= cost

        return 2

    def apply_fertilizer(self, type, amount):

        cost = amount * 5

        if self.state_data.budget < cost:
            return -3

        self.state_data.budget -= cost
        return 3

    def check_pest_alert(self):
        return self.state_data.pest_alert

    def apply_pesticide(self, type):

        cost = 200

        if self.state_data.budget < cost:
            return -3

        self.state_data.budget -= cost
        self.state_data.pest_alert = False

        return 4

    def check_mandi_price(self, crop):
        return self.state_data.mandi_price

    def sell_crop(self, quantity):

        profit = quantity * self.state_data.mandi_price
        self.state_data.budget += profit

        return profit

    # ---------- DYNAMIC WORLD ----------

    def update_environment(self):

        self.state_data.days_to_harvest -= 1

        self.state_data.weather = random.choice(
            ["sunny", "rain", "cloudy"]
        )

        if self.state_data.weather == "rain":
            self.state_data.soil_moisture += 10

        self.state_data.soil_moisture -= 5

        if random.random() < 0.2:
            self.state_data.pest_alert = True

        # price fluctuation
        crop_info = self.CROP_DATA[self.state_data.season][self.state_data.crop]
        self.state_data.mandi_price = random.randint(*crop_info["price"])

        self.state_data.soil_moisture = max(
            0, min(100, self.state_data.soil_moisture)
        )