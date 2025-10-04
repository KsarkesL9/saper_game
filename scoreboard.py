import json
import config

RANKED_LEVELS = list(config.DIFFICULTIES.keys())


def load_high_scores():
    try:
        with open(config.SCORE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_player_score(level_name, time_seconds, player_name):
    if level_name not in RANKED_LEVELS:
        return

    scores = load_high_scores()

    if level_name not in scores:
        scores[level_name] = []

    new_score_entry = {
        "time": round(time_seconds, 2),
        "name": player_name
    }

    scores[level_name].append(new_score_entry)

    scores[level_name] = sorted(scores[level_name], key=lambda x: x['time'])[:5]

    try:
        with open(config.SCORE_FILE, "w") as f:
            json.dump(scores, f, indent=4)
    except IOError:
        print(f"Error: Could not save scores to {config.SCORE_FILE}")