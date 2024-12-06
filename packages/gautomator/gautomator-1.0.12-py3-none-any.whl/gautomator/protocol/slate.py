import typing
from .common import CMD_DICT

def slate_click( 
        name: str, 
        address: typing.Optional[str] = None, 
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
    """Function to simulate a click on a slate object
        Args:
           name (str): The name of the slate object
           address (Optional[str]): The address of the slate object, if any
           timeout_seconds (int): The timeout in seconds for the click action
        Returns:
           Generator: Yields the timeout and request, and returns the status and body of the response
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "slate", 'command': 'click', 'body': {'name':name, 'address': address}}
    json = yield request
    print("slate_click recv json:" + str(json))
    data = yield request
    print("slate_click recv data:" + str(data))
    return (json["status"], json["body"])

def slate_on_key_event( 
        key_code: float,
        action: float,
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
    """ Function to handle key events for the slate object
        Args:
            key_code (float): The key code of the key event
            action (float): The action of the key event
            timeout_seconds (int, optional): The timeout for the key event, default is 15 seconds
        Returns:
            Generator: Yields a tuple (status, body) where status is an int and body is a str
    """ 
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "slate", 'command': 'keyEvent', 'body': {'keyCode':key_code, 'action': action}}
    json = yield request
    return (json["status"], json["body"])


def slate_begin_touch( 
        start_position: dict,
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
    """ slate_begin_touch: Initiates a touch event on a slate.
        Args:
           start_position (dict): The starting position of the touch event.
           timeout_seconds (int, optional): The timeout for the touch event in seconds. Defaults to 15.
        Returns:
           Generator: Yields the timeout_seconds and request, then returns a tuple containing the status and body of the response.
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "slate", 'command': 'keyEvent', 'body': {'startPosition': start_position}}
    json = yield request
    return (json["status"], json["body"])

def slate_move_touch( 
        touch_index: float,
        screen_delta: dict,
        duration_seconds: float,
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
    """ Function to simulate a touch event on a slate, moving the touch point according to the given parameters
          Args:
            touch_index (float): The index of the touch event
            screen_delta (dict): The change in screen position
            duration_seconds (float): The duration of the touch event in seconds
            timeout_seconds (int, optional): The timeout for the touch event in seconds, default is 15
         Returns:
            Generator: Yields a tuple (status, body) where status is an int and body is a string
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "slate", 'command': 'keyEvent', 
                     'body': {'touchIndex': touch_index, 'screenDelta': screen_delta, 'durationSeconds': duration_seconds}}
    json = yield request
    return (json["status"], json["body"])

def slate_end_touch( 
        touch_index: float,
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
    """ Function to handle the end of a touch event with slate object
        Args:
            touch_index: float - The index of the touch event
            timeout_seconds: int - The timeout duration in seconds (default: 15)
        Returns:
            Generator - Yields a tuple (status: int, body: str) containing the status and body of the response
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "slate", 'command': 'keyEvent', 'body': {'touchIndex': touch_index}}
    json = yield request
    return (json["status"], json["body"])
