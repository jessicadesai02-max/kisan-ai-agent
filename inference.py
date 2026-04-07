from env.farm_env import FarmEnv
import random
import time


def choose_action(state):

    if state["soil_moisture"] < 30:
        return {"tool": "irrigate", "params": {"amount": 10}}

    if state["pest_alert"]:
        return {"tool": "apply_pesticide", "params": {"type": "basic"}}

    if state["days_to_harvest"] <= 1:
        return {"tool": "sell_crop", "params": {"quantity": 50}}

    if state["budget"] > 1000:
        return {"tool": "apply_fertilizer", "params": {"type": "basic", "amount": 5}}

    return random.choice([
        {"tool": "check_weather"},
        {"tool": "check_soil_moisture"}
    ])


def run():

    env = FarmEnv()

    state = env.reset()
    total_reward = 0

    print("\n[START] AI Agent Running\n")

    # ✅ LOOP MUST BE INSIDE FUNCTION
    for step in range(1, 20):

        action = choose_action(state)

        state, reward, done, _ = env.step(action)

        total_reward += reward

        print(f"[STEP {step}] Action: {action} | Reward: {reward}")

        time.sleep(1)

        if done:
            print("🌾 Harvest Done")
            break

    print("\n[END] Total Score:", total_reward)


# ✅ ENTRY POINT
if __name__ == "__main__":
    run()
