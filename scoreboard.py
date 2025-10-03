# scoreboard.py
import json
import config


def load_high_scores():
    try:
        with open(config.SCORE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return empty dict if file not found or corrupted


def save_player_score(level_name, time_seconds):
    scores = load_high_scores()

    if level_name not in scores:
        scores[level_name] = []

    # Store time as a float, formatted to two decimal places when reading if necessary
    scores[level_name].append(round(time_seconds, 2))
    scores[level_name] = sorted(scores[level_name])[:5]  # Keep top 5 scores

    try:
        with open(config.SCORE_FILE, "w") as f:
            json.dump(scores, f, indent=4)
    except IOError:
        print(f"Error: Could not save scores to {config.SCORE_FILE}")