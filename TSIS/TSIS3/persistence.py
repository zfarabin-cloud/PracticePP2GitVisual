"""
persistence.py — Save / load leaderboard.json and settings.json.
"""

import json
import os
from datetime import datetime

SETTINGS_FILE    = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

DEFAULT_SETTINGS = {
    "sound":      True,
    "car_color":  [0, 120, 255],   # blue
    "difficulty": "Normal",
}

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

def load_settings() -> dict:
    try:
        with open(SETTINGS_FILE) as f:
            data = json.load(f)
        for k, v in DEFAULT_SETTINGS.items():
            data.setdefault(k, v)
        return data
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(cfg: dict):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(cfg, f, indent=4)
    except Exception as e:
        print(f"[Settings] Could not save: {e}")


# ---------------------------------------------------------------------------
# Leaderboard
# ---------------------------------------------------------------------------

def load_leaderboard() -> list[dict]:
    try:
        with open(LEADERBOARD_FILE) as f:
            return json.load(f)
    except Exception:
        return []


def save_leaderboard(entries: list[dict]):
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(entries, f, indent=4)
    except Exception as e:
        print(f"[Leaderboard] Could not save: {e}")


def add_score(username: str, score: int, distance: int, coins: int) -> list[dict]:
    """Insert a new run, keep top 10, return updated list."""
    entries = load_leaderboard()
    entries.append({
        "rank":     0,
        "username": username,
        "score":    score,
        "distance": distance,
        "coins":    coins,
        "date":     datetime.now().strftime("%Y-%m-%d"),
    })
    entries.sort(key=lambda x: x["score"], reverse=True)
    entries = entries[:10]
    for i, e in enumerate(entries):
        e["rank"] = i + 1
    save_leaderboard(entries)
    return entries
