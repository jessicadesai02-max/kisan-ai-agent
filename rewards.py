# rewards.py
# Person 2 owns this file

def calculate_step_reward(action, farm_state, result):

    reward = 0.0

    if action == "irrigate":
        if farm_state.get("rain_coming_tomorrow"):
            reward -= 0.2
        elif farm_state.get("soil_moisture", 50) < 20:
            reward += 0.3
        elif farm_state.get("soil_moisture", 50) < 40:
            reward += 0.1
        else:
            reward -= 0.1

    if action == "apply_pesticide":
        if farm_state.get("pest_alert"):
            reward += 0.4
        else:
            reward -= 0.2

    if action == "sell_crop":
        if result.get("sold_at_peak_price"):
            reward += 0.5
        elif result.get("price_above_base"):
            reward += 0.2
        else:
            reward -= 0.1

    if farm_state.get("budget", 1) <= 0:
        reward -= 0.4

    if farm_state.get("crop_health", 100) < 30:
        reward -= 0.3

    if farm_state.get("shock_active"):
        if action in ["drain_field", "irrigate", "apply_pesticide"]:
            reward += 0.3
        else:
            reward -= 0.3

    return round(min(max(reward, -1.0), 1.0), 2)