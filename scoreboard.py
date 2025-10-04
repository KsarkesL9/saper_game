import json
import os
import config

RANKED_LEVELS = list(getattr(config, "DIFFICULTIES", {}).keys())

def _init_structure():
    if not RANKED_LEVELS:
        return {}
    return {lvl: [] for lvl in RANKED_LEVELS}

def load_high_scores():
    path = getattr(config, "SCORE_FILE", "highscores.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return _init_structure()
            for lvl in RANKED_LEVELS:
                if lvl not in data or not isinstance(data[lvl], list):
                    data[lvl] = []
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return _init_structure()

def save_player_score(level_name, time_seconds, player_name):
    if not RANKED_LEVELS:
        return
    if level_name not in RANKED_LEVELS:
        return
    path = getattr(config, "SCORE_FILE", "highscores.json")
    scores = load_high_scores()

    entry = {"time": round(float(time_seconds), 2), "name": str(player_name)[:32] or "Anon"}
    scores[level_name].append(entry)
    scores[level_name] = sorted(scores[level_name], key=lambda x: x.get("time", 0.0))[:5]

    tmp_path = path + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=4)
        os.replace(tmp_path, path)
    except OSError:
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(scores, f, ensure_ascii=False, indent=4)
        except OSError:
            pass