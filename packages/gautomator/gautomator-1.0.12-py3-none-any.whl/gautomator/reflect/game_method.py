from gautomator.tcp.ga_sdk_client import GASdkClient
from gautomator.protocol.common import OPFunction
from gautomator.reflect.game_method import *
from collections import OrderedDict
from gautomator.protocol.common import call_reflection
import logging
import typing

logger = logging.getLogger('Actor')

class GameMethods:

    def __init__(self, conn: GASdkClient, methods: typing.OrderedDict[str, OPFunction], out: str):
        self._conn = conn
        assert isinstance(methods, OrderedDict), "functions must be ordered dict"
        assert out in methods.keys() , "return function name not in " +  str(methods.keys())
        self._ops_dict = []
        for k, v in methods.items() :
            v.op_name = k
            self._ops_dict.append(v.to_json())
        self._out = out
    
    def invoke(self, timeout_seconds = 15) -> typing.Any:
        return self._conn.exec(call_reflection(self._ops_dict, self._out, timeout_seconds))