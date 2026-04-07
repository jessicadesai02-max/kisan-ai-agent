# graders.py

from data import SHOCK_TYPES, EASY_SCENARIOS, MEDIUM_SCENARIOS, HARD_SCENARIOS


def grade_easy_task(ai_action, scenario):
    correct = scenario["correct_action"]
    soil = scenario["soil_moisture"]
    rain = scenario["rain_coming_tomorrow"]
    budget = scenario["budget"]

    if ai_action == correct:
        return 1.0

    if ai_action == "irrigate" and correct == "wait":
        if budget < 500:
            return 0.0
        elif rain:
            return 0.1
        else:
            return 0.3

    if ai_action == "wait" and correct == "irrigate":
        if soil < 15:
            return 0.0
        elif soil < 25:
            return 0.2
        else:
            return 0.4

    return 0.0


def grade_medium_task(ai_actions, scenario):
    shock = SHOCK_TYPES[scenario["shock_type"]]
    budget = scenario["budget"]
    score = 0.0

    responded = any(
        action in shock["correct_actions"]
        for action in ai_actions
    )

    if not responded:
        return round(1.0 - shock["penalty_if_ignored"], 2)

    score += 0.2

    for i, action in enumerate(ai_actions):
        if action in shock["correct_actions"]:
            response_step = i + 1
            if response_step == 1:
                score += 0.3
            elif response_step == 2:
                score += 0.2
            elif response_step == 3:
                score += 0.1
            break

    correct_actions_taken = [
        a for a in ai_actions if a in shock["correct_actions"]
    ]
    wrong_actions_taken = [
        a for a in ai_actions if a in shock["wrong_actions"]
    ]

    if correct_actions_taken and not wrong_actions_taken:
        score += 0.3
    elif correct_actions_taken and wrong_actions_taken:
        score += 0.15

    if scenario["shock_type"] == "msp_spike":
        if "sell_crop" in ai_actions:
            sell_step = ai_actions.index("sell_crop") + 1
            spike_lasts = scenario.get("spike_lasts_days", 3)
            if sell_step <= spike_lasts:
                score += 0.2
    else:
        if budget > 3000:
            score += 0.2
        elif budget > 1000:
            score += 0.1
        else:
            score += 0.05

    return round(min(max(score, 0.0), 1.0), 2)


def grade_hard_task(episode_result, scenario):
    max_profit = scenario["maximum_possible_profit"]
    total_pests = len(scenario["pest_events"])
    score = 0.0

    if episode_result["final_profit"] <= 0:
        profit_score = 0.0
    else:
        profit_score = min(
            episode_result["final_profit"] / max_profit, 1.0
        ) * 0.5

    survival_score = 0.25 if episode_result["crop_survived"] else 0.0

    if total_pests == 0:
        pest_score = 0.15
    else:
        pest_ratio = episode_result["pests_handled"] / total_pests
        pest_score = pest_ratio * 0.15

    completion_ratio = (
        episode_result["days_completed"] / scenario["season_length_days"]
    )
    completion_score = completion_ratio * 0.1

    score = profit_score + survival_score + pest_score + completion_score

    return round(min(max(score, 0.0), 1.0), 2)