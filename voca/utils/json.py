import json
from typing import Any

class vocaJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, set):
            return list(o)
        return super().default(o)

def load(*args ,**kwargs):
    return json.load(*args, **kwargs)

def dump(*args, **kwargs):
    kwargs.pop('cls', '')
    return json.dump(*args, cls=vocaJSONEncoder, **kwargs)