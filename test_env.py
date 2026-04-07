from env.farm_env import FarmEnv


def print_dashboard(state):

    print("\n🌾 FARM DASHBOARD")
    print("-----------------------------")
    print("🌦 Season        :", state["season"])
    print("🌾 Crop          :", state["crop"])
    print("🌱 Soil Moisture :", state["soil_moisture"])
    print("💰 Budget        : ₹", state["budget"])
    print("☁ Weather        :", state["weather"])
    print("🐛 Pest Alert    :", state["pest_alert"])
    print("⏳ Days Harvest  :", state["days_to_harvest"])
    print("🏪 Mandi Price   : ₹", state["mandi_price"])
    print("-----------------------------")


env = FarmEnv()

print("\nRESET FARM")
state = env.reset()
print_dashboard(state)

print("\nSTEP 1 — IRRIGATE")

state, reward, done, _ = env.step({
    "tool": "irrigate",
    "params": {"amount": 10}
})

print_dashboard(state)
print("Reward:", reward)

print("\nSTEP 2 — APPLY PESTICIDE")

state, reward, done, _ = env.step({
    "tool": "apply_pesticide",
    "params": {"type": "basic"}
})

print_dashboard(state)
print("Reward:", reward)

print("\nSTEP 3 — SELL CROP")

state, reward, done, _ = env.step({
    "tool": "sell_crop",
    "params": {"quantity": 50}
})

print_dashboard(state)
print("Reward:", reward)