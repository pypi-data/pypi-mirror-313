import json
import random
import os

class WatchData:
    def __init__(self):
        self.watches = self._load_data()

    def _load_data(self):
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'db.json')
            with open(db_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            return [
                {"name": "Submariner", "brand": "Rolex"},
                {"name": "Speedmaster", "brand": "Omega"}
            ]

    def get_watch(self):
        return random.choice(self.watches)

    def get_watch_name(self):
        watch = self.get_watch()
        return f"{watch['brand']} {watch['name']}"

# Create single instance
_watch_data = WatchData()

# Public API functions
def get_watch():
    return _watch_data.get_watch()

def get_watch_name():
    return _watch_data.get_watch_name()