from typing import Any
from dataclasses import dataclass


@dataclass
class Segment:
    id: str
    start_time: str
    end_time: str
    title: str
    category: str
    is_recurring: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Segment':
        _id = str(obj.get("id"))
        _start_time = str(obj.get("start_time"))
        _end_time = str(obj.get("end_time"))
        _title = str(obj.get("title"))
        _category = str(obj.get("game_name"))
        _is_recurring = str(obj.get("is_recurring"))
        return Segment(_id, _start_time, _end_time, _title, _category, _is_recurring)


@dataclass
class TwitchStreamInfo:
    data: Segment

    @staticmethod
    def from_api_response(api_response: Any) -> 'TwitchStreamInfo':
        if api_response is None:  # Vérifie si les données sont None
            return None
        _data = Segment.from_dict(api_response)
        return TwitchStreamInfo(_data)



# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
