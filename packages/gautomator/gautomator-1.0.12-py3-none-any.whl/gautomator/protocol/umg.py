from .common import CMD_DICT, T_JSON_DICT, RespStatus
from dataclasses import dataclass
from enum import Enum
from gautomator.by import By

import typing
import json

@dataclass
class UWidgetBasicInfo:
    #: Widget UObject UniqueID
    unique_id: int

    #: Widget UObject Serial Number
    serial_number: str

    #: Widget Name
    name: str

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['uniqueId'] = int(self.unique_id)
        json['serialNumber'] = int(self.serial_number)
        json['name'] = self.name
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) :
        return cls(
            unique_id=int(json['uniqueID']),
            serial_number=str(json['serialNumber']),
            name=str(json['name']),
        )

class ClickType(Enum):
    AUTO = "auto"
    TRIGGERING_EVENT = "triggeringEvent"
    SIMULATED_LOCATION_TOUCH = "simulatedLocationTouch"


def umg_click( 
        click_type: ClickType,
        name: str,
        unique_id: int = -1,
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, dict]]:
    """ Click a UMG widget
        Args:
            click_type: ClickType - The type of click to perform
            name: str - The name of the widget to click
            unique_id: Optional[str] - The unique ID of the widget (default: None)
            timeout_seconds: int - The timeout in seconds (default: 15)
        Returns:
            Generator[Any, CMD_DICT, Tuple[int, str]] - A generator that yields the status and response body
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "umg", 'command': 'click', 
                     'body': {'name':name, 'clickType': click_type, 'uniqueID': unique_id}}
    json = yield request
    return (json["status"], json["body"])

def umg_find_widget( 
        by: By,
        value: str,
        timeout_seconds: int = 15
    ) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, UWidgetBasicInfo]]:
    """ Find a UMG widget
        Args:
            by: By - The method to find the widget
            value: str - The value to search for
            timeout_seconds: int - The timeout in seconds (default: 15)
        Returns:
            Generator[Any, CMD_DICT, Tuple[int, UWidgetBasicInfo]] - A generator that yields the status and UWidgetBasicInfo object
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "umg", 'command': 'findWidget', 
                     'body': {'by':by, 'value': value}}
    res_json = yield request
    if res_json["status"] == RespStatus.SuccessJson.value:
        return (True, UWidgetBasicInfo.from_json(res_json["body"]["widgetInfo"]))
    else:
        return (False, res_json["body"]["error"])

def umg_set_text(name: str, text: str, unique_id: int = -1, 
                 timeout_seconds: int = 15) -> typing.Generator[typing.Any, CMD_DICT, typing.Tuple[int, bool]]:
    """ Set text of a UMG widget
        Args:
            name: str - The name of the widget to set text
            text: str - The text to set
            unique_id: Optional[str] - The unique ID of the widget (default: None)
            timeout_seconds: int - The timeout in seconds (default: 15)
        Returns:
            Generator[Any, CMD_DICT, Tuple[int, bool]] - A generator that yields the status and a boolean indicating success
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    body = {'name':name, 'text': text}
    if unique_id is not None:
        body['uniqueID'] = unique_id
    request: dict = {'object': "umg", 'command': 'setText', 
                     'body': body}
    res_json = yield request
    return (res_json["status"] == RespStatus.SuccessJson.value)

def umg_get_attributes(widget_info: UWidgetBasicInfo, 
                       timeout_seconds: int = 15) -> typing.Generator[typing.Any, CMD_DICT, dict]:
    """ Get attributes of a UMG widget
        Args:
            widget_info: UWidgetBasicInfo - The basic information of the widget
            timeout_seconds: int - The timeout in seconds (default: 15)
        Returns:
            Generator[Any, CMD_DICT, dict] - A generator that yields the attributes of the widget as a dictionary
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    request: dict = {'object': "umg", 'command': 'GetAttrs', 'body': widget_info.to_json()}
    res_json = yield request

    attributes = res_json["body"]["attributes"]
    res_list =[]
    for attribute in attributes:
        res_list.append((attribute["name"], attribute["value"]))
    return res_list

def umg_set_checkbox(name: str, check_state: bool, unique_id: int = -1, 
                 timeout_seconds: int = 15) -> typing.Generator[typing.Any, CMD_DICT, bool]:
    """ Set text of a UMG widget
        Args:
            name: str - The name of the widget to set text
            text: str - The text to set
            unique_id: Optional[str] - The unique ID of the widget (default: None)
            timeout_seconds: int - The timeout in seconds (default: 15)
        Returns:
            Generator[Any, CMD_DICT, Tuple[int, bool]] - A generator that yields the status and a boolean indicating success
    """
    timeout_seconds = timeout_seconds
    yield timeout_seconds
    body = {'name':name, 'state': check_state}
    if unique_id >= 0:
        body['uniqueID'] = unique_id
    request: dict = {'object': "umg", 'command': 'setCheckBox', 
                     'body': body}
    res_json = yield request
    return (res_json["status"] == RespStatus.SuccessJson.value)