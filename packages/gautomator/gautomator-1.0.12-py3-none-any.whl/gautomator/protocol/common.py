from enum import Enum
from gautomator.by import *
from dataclasses import dataclass,field

import typing

CMD_DICT = typing.Dict[str, typing.Any]
T_JSON_DICT = typing.Dict[str, typing.Any]

class RespStatus(Enum):
    Init = 100
    Error = 101
    SuccessJson = 102
    SuccessBinary = 103

@dataclass
class OPFunction:
    is_static: bool

    def __post_init__(self):
        self.validate()
        for i in range(len(self.params)):
            self.params[i] = str(self.params[i])

    def validate(self):
        assert isinstance(self.params, list), 'params should be list'

@dataclass
class OPStaticFunction(OPFunction):
    package_name: str
    class_name: str
    function_name: str
    params: typing.List[str] = field(default_factory=list)
    op_name: str = ""

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['opName'] = self.op_name
        json['isStatic'] = self.is_static
        json['packageName'] = self.package_name
        json['className'] = self.class_name
        json['functionName'] = self.function_name
        json['params'] = self.params
        return json

@dataclass
class OPNonStaticFunction(OPFunction):
    object_name: str
    function_name: str
    params: typing.List[str] = field(default_factory=list)
    op_name: str = ""

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['opName'] = self.op_name
        json['isStatic'] = self.is_static
        json['objectName'] = self.object_name
        json['functionName'] = self.function_name
        json['params'] = self.params
        return json

def get_engine_info(timeout_seconds: int = 15) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
    """This function retrieves SDK information with a specified timeout and returns the status and body of the response.
       Args:
          timeout_seconds: time in seconds to wait before timing out.

       Returns:
          status: RespStatus code
          body: the sdk info
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': 'status', 'command': 'engine'}
    json = yield request
    return (json["status"], json["body"]["version"])

def call_user_command(msg: str, event_name: str, timeout_seconds: int = 15) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[bool, str]]:
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': 'gameLogic', 'command': 'callUserEvent','body': {'userEvent': event_name, 'param': msg}}
    json = yield request
    body = json["body"]
    if json["status"] == RespStatus.SuccessJson.value:
       
        return (body["result"], body["response"])
    elif json["status"] == RespStatus.Error.value:
        return (False, body["response"])
    else:
        return (False, body)
    
def enable_user_event(timeout_seconds: int = 15) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
    """This function enables user events with a specified timeout and returns a generator.
       The generator yields the timeout and a request dictionary, 
       and returns a tuple containing the status and body of the response.
       Args:
          timeout_seconds: time in seconds to wait before timing out.

       Returns:
          status: RespStatus code
          body: the sdk info
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': 'gameLogic', 'command': 'enableUserEvent'}
    json = yield request
    return (json["status"], json["body"])


def screenshot(object:str, save_path:str, timeout_seconds: int = 15) -> typing.Generator[typing.Any, typing.Any, typing.Tuple[int]]:
    """ This function takes an object and an optional timeout_seconds parameter.
        It returns a generator that yields the timeout_seconds and a request dictionary.
        The generator then yields the JSON response containing the status and body of the screenshot.
        
        Args:
            object (str): The name of the object to take a screenshot of. either slate or umg object.
            save_path (str): The path to save the screenshot to.
            timeout_seconds (int, optional): The number of seconds to wait for the object to appear on the screen before timing out. Defaults to 15.

        Returns:
            A generator that yields a tuple containing the exit code, the output of the command, and the receive status.
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': 'slate', 'command': 'screenshot'}
    json = yield request
    data = yield request
    img_file = open(save_path, 'wb')
    img_file.write(data)
    img_file.close()
    return (json["status"])

def get_source(object:str, timeout_seconds: int = 15) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
    # Function to get the source code of an object with a specified timeout
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': object, 'command': 'getSource'}
    json = yield request
    return (json["status"], json["body"])

def is_alive(timeout_seconds: int = 15) -> typing.Generator[typing.Any, CMD_DICT, int]:
    # This function checks if the device is alive by sending a ping command and waiting for a response.
    # If the device is alive, it yields the response code and the CMD_DICT.
    # If the device is not alive after the timeout period, it raises a TimeoutError.
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': 'status', 'command': 'isAlive'}
    json = yield request
    return (json["status"])

def subscribe(event_name: str, timeout_seconds: int = 15) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "gameLogic", 'command': 'subscribeUserEvent', 'body': {'str': event_name}}
    json = yield request
    return (json["status"], json["body"])

def unsubscribe(event_name: str, timeout_seconds: int = 15) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "gameLogic", 'command': "unSubscribeUserEvent", "body": {'str': event_name}}
    json = yield request
    return (json["status"], json["body"])

def set_filter(object:str, show_invisilbe: bool, timeout_seconds: int = 15) -> bool:
    # Function to get the source code of an object with a specified timeout
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': object, 'command': 'setFilter', "body": {"showInvisibleWgt": show_invisilbe}}
    json = yield request
    return json["status"] == RespStatus.SuccessJson.value

def exec_console_cmd(cmd:str, timeout_seconds: int = 15) -> bool:
    # Function to get the source code of an object with a specified timeout
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "gameLogic", 'command': 'execCmd', "body": {"str": cmd}}
    json = yield request
    return json["status"] == RespStatus.SuccessJson.value

def get_screen_size(timeout_seconds: int = 15) -> typing.Tuple[int, int]:

    """
        This function is used to get the screen size of the device. 
        It returns a tuple containing a boolean value indicating whether the screen size was successfully retrieved, 
        and the width and height of the screen in pixels.

        Args:
            timeout_seconds: An integer representing the maximum time to wait for the screen size to be retrieved. Default value is 15 seconds.

        Returns：
            A tuple containing a boolean value indicating whether the screen size was successfully retrieved, and the width and height of the screen in pixels.

        Exceptions: 
            Raises a TimeoutError if the screen size retrieval exceeds the specified timeout.
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "slate", 'command': 'getWindowSize'}
    json = yield request
    if json["status"] == RespStatus.SuccessJson.value:
        return (json["body"]["width"], json["body"]["height"])
    else:
        return (0 , 0)

def call_reflection(ops:typing.List, out:str, timeout_seconds: int = 15) -> typing.Any:
    """ This function is used to invoke a series of reflection methods with the given ordered dictionary of OPFunctions. 
        It waits for all the methods to complete execution for a maximum of 'timeout_seconds' seconds
        
        Args:
            - ops: An ordered dictionary of OPFunctions representing the sequence of reflection methods to be executed.
            - out: Use the return value of this function as the return value of the reflection.
            - timeout_seconds: An integer representing the maximum time to wait for all the methods to complete execution. Default value is 15 seconds.
            
        Returns:
            True if reflection methods exec successed
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "reflection", 'command': 'callFunc', "body": {"ops": ops, "outOp": out}}
    json = yield request
    body = json["body"]
    # if json["status"] == RespStatus.SuccessJson.value:
    #     return body["OutValue"]
    # elif json["status"] == RespStatus.Error.value:
    #     return body["failure"]
    # else:
    return body

