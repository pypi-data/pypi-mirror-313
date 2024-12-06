from .common import CMD_DICT, T_JSON_DICT, RespStatus

from dataclasses import dataclass
import typing

@dataclass
class Point:
    #: position x
    x: float

    #: position y
    y: float

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['X'] = self.x
        json['Y'] = self.y
        return json

@dataclass
class ScreenSize:
    #: screen width
    width: int

    #: screen height
    height: int

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['X'] = self.width
        json['Y'] = self.height
        return json

@dataclass
class Position:
    #: point
    point: Point

    #: screen size
    screen_size: ScreenSize

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['point'] = self.point.to_json()
        json['screenSize'] = self.screen_size.to_json()
        return json

def scrcpy_touch_event( 
        action: int,
        pointerId: int,
        position: Position,
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, bool]:
    """
    Handles touch events from the user.

    Parameters:
    - action (int): The type of touch action (e.g. down, move, up)
    - pointerId (int): The ID of the pointer associated with the touch event
    - position (Position): The position of the touch event
    - timeout_seconds (int): The number of seconds to wait for a response before timing out (default 15)

    Returns:
    - A generator that yields a tuple containing the response code, a dictionary of command data, and the response body
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "touch", 'command': 'touchEvent', 
                     'body': {'action': action, 'pointerId': pointerId, 'position': position.to_json()}}
    json = yield request
    return json["status"] == RespStatus.SuccessJson.value
