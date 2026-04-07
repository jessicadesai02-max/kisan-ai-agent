from env.farm_env import FarmEnv# test_run.py
import sys
import os

sys.path.append(os.path.dirname(__file__))

print("Starting test...")

try:
    from env.farm_env import FarmEnv
    print("✅ farm_env imported successfully")
except Exception as e:
    print(f"❌ farm_env import failed: {e}")

try:
    from graders import grade_easy_task, grade_medium_task, grade_hard_task
    print("✅ graders imported successfully")
except Exception as e:
    print(f"❌ graders import failed: {e}")

try:
    from data import EASY_SCENARIOS, MEDIUM_SCENARIOS, HARD_SCENARIOS
    print("✅ data imported successfully")
except Exception as e:
    print(f"❌ data import failed: {e}")

try:
    from rewards import calculate_step_reward
    print("✅ rewards imported successfully")
except Exception as e:
    print(f"❌ rewards import failed: {e}")

print("\n=== Testing Farm Environment ===")
try:
    env = FarmEnv()
    state = env.reset()
    print("✅ reset() works:", state)
except Exception as e:
    print(f"❌ reset() failed: {e}")

try:
    state, reward, done, info = env.step({"tool": "irrigate", "params": {"amount": 20}})
    print("✅ step() works — reward:", reward, "done:", done)
except Exception as e:
    print(f"❌ step() failed: {e}")

print("\n=== Testing Easy Grader ===")
try:
    score1 = grade_easy_task("wait", EASY_SCENARIOS[0])
    score2 = grade_easy_task("irrigate", EASY_SCENARIOS[0])
    print("✅ Easy grader works:", score1, score2)
except Exception as e:
    print(f"❌ Easy grader failed: {e}")

print("\n=== Testing Medium Grader ===")
try:
    score3 = grade_medium_task(["drain_field"], MEDIUM_SCENARIOS[0])
    score4 = grade_medium_task(["do_nothing"], MEDIUM_SCENARIOS[0])
    print("✅ Medium grader works:", score3, score4)
except Exception as e:
    print(f"❌ Medium grader failed: {e}")

print("\n=== Testing Hard Grader ===")
try:
    good = {
        "final_profit": 8000,
        "crop_survived": True,
        "pests_handled": 1,
        "days_completed": 30
    }
    bad = {
        "final_profit": 0,
        "crop_survived": False,
        "pests_handled": 0,
        "days_completed": 10
    }
    score5 = grade_hard_task(good, HARD_SCENARIOS[0])
    score6 = grade_hard_task(bad, HARD_SCENARIOS[0])
    print("✅ Hard grader works:", score5, score6)
except Exception as e:
    print(f"❌ Hard grader failed: {e}")

print("\nDone!")