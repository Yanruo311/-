import json
import os


class GameStats:

    def __init__(self,ai_game):
        self.settings=ai_game.settings
        self.reset_stats()
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0

    def load_high_scores(self):
        try:
            if os.path.exists('high_score.json'):
                with open('high_score.json','r') as f:
                    data = json.load(f)
                    return data.get('high_score',0)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return 0

    def save_high_score(self):
        data = {"high_score":self.high_score}
        with open('high_score.json', 'w') as f:
            json.dump(data, f)


