import json
from enum import Enum


class RumorzJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, dict):
            return {key: self.default(value) for key, value in obj.items()}
        if isinstance(obj, list):
            return [self.default(element) for element in obj]
        return super().default(obj)
