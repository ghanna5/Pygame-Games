"""Leaderboard for Galaga."""

import pickle
import os

LEADERBOARD_FILE = os.path.join(os.path.dirname(__file__), 'data', 'leaderboard.pkl')


def load():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'rb') as f:
            return pickle.load(f)
    return []


def save(name, score):
    scores = load()
    scores.append({'name': name, 'score': score})
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:3]
    with open(LEADERBOARD_FILE, 'wb') as f:
        pickle.dump(scores, f)