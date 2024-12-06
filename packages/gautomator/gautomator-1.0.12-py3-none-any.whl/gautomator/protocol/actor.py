from .common import CMD_DICT, RespStatus
import typing
from typing import Tuple

def yaw( 
        value: float,
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, bool]:
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "actor", 'command': 'yaw', 
                     'body': {'value': value}}
    json = yield request
    return json["status"] == RespStatus.SuccessJson.value

def roll( 
        value: float,
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, bool]:
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "actor", 'command': 'roll', 
                     'body': {'value': value}}
    json = yield request
    return json["status"] == RespStatus.SuccessJson.value

def pitch( 
        value: float,
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, bool]:
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "actor", 'command': 'pitch', 
                     'body': {'value': value}}
    json = yield request
    return json["status"] == RespStatus.SuccessJson.value

def get_rotation( 
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "actor", 'command': 'getRotation'}
    json = yield request
    return (json["status"], json["body"])

def get_location( 
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "actor", 'command': 'getLocation'}
    json = yield request
    return (json["status"], json["body"])

def set_location( 
        pos: Tuple[float, float, float],
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, bool]:
  
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "actor", 'command': 'setLocation', 
                     'body': {'x': pos[0], 'y': pos[1], 'z': pos[2]}}
    json = yield request
    return json["status"] == RespStatus.SuccessJson.value

def line_trace( 
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
  
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "actor", 'command': 'lineTrace'}
    json = yield request
    return (json["status"], json["body"])

def move_forward( 
        value: float,
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, bool]:
  
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "actor", 'command': 'moveForward', 
                     'body': {'value': value}}
    json = yield request
    return json["status"] == RespStatus.SuccessJson.value

def move_right( 
        value: float,
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, bool]:
  
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "actor", 'command': 'lineTrace', 
                     'body': {'value': value}}
    json = yield request
    return json["status"] == RespStatus.SuccessJson.value