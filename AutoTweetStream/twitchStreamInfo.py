from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class Category:
    id: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'Category':
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        return Category(_id, _name)

@dataclass
class Segment:
    id: str
    start_time: str
    end_time: str
    title: str
    category: Category
    is_recurring: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Segment':
        _id = str(obj.get("id"))
        _start_time = str(obj.get("start_time"))
        _end_time = str(obj.get("end_time"))
        _title = str(obj.get("title"))
        _category = Category.from_dict(obj.get("category"))
        _is_recurring = str(obj.get("is_recurring"))
        return Segment(_id, _start_time, _end_time, _title, _category, _is_recurring)

@dataclass
class Data:
    segments: List[Segment]
    broadcaster_id: str
    broadcaster_name: str
    broadcaster_login: str

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        _segments = [Segment.from_dict(y) for y in obj.get("segments")]
        _broadcaster_id = str(obj.get("broadcaster_id"))
        _broadcaster_name = str(obj.get("broadcaster_name"))
        _broadcaster_login = str(obj.get("broadcaster_login"))
        return Data(_segments, _broadcaster_id, _broadcaster_name, _broadcaster_login)


@dataclass
class TwitchStreamInfo:
    data: Data

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _data = Data.from_dict(obj.get("data"))
        return TwitchStreamInfo(_data)


# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
