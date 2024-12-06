from gautomator.tcp.ga_sdk_client import GASdkClient
from gautomator.protocol.common import enable_user_event, T_JSON_DICT, subscribe, unsubscribe
from dataclasses import dataclass
from typing import Callable

import threading
import uuid
import queue
import logging

logger = logging.getLogger('GameEventManager')


@dataclass
class UserEventTriggerred:
    '''
    Customized User Event
    '''
    #: event unique id
    sequence_id: str
    #: attached JSON data
    name: str
    #: attached JSON data
    msg: str
    #: Timestamp.
    timestamp: str

    @classmethod
    def from_json(cls, json: T_JSON_DICT):
        body = json['body']
        return cls(
            sequence_id=str(json['requestId']),
            name=body['name'],
            msg=str(body['msg']),
            timestamp=str(body['timestamp'])
     )
    
class GameEventManager():
    def __init__(self, client: GASdkClient):
        self._events = dict()
        self._is_run = False
        self._client = client

    def register_event_handler(self, event_name: str,
                               event_callback: Callable = None, timeout_seconds: int = 15) -> str:
        """Register the event callback of the given event name

        This method will put the event_name and event_callback to the events map.
        If the sdk client received the message of the given event_name , then the 
        event_callback will be called immediately.

        Args:
           event_name: The event name you want to listened.
           event_callback: The event callback when sdk client 
           received the message of the given event_name.

        Returns:
           The callback identifier of the event name.
        """
        res = self._client.exec(subscribe(event_name, timeout_seconds))
        logger.debug("subscribe res :%s", res)
        
        callback_id = event_callback.__name__
        if event_name not in self._events:
            self._events[event_name] = {}
        self._events[event_name][callback_id] = event_callback
        logger.debug("register event_name(%s) success callback_id=%s ", event_name, callback_id)
        if not self._is_run:
            self.run()
        return callback_id

    def unregister_event_handler(self, event_name: str, callback_id: str, timeout_seconds: int = 15):
        logger.debug("handle unregister %s-%s", event_name, callback_id)
        
        res = self._client.exec(unsubscribe(event_name, timeout_seconds))
        logger.debug("unsubscribe res :%s", res)

        for k in list(self._events.keys()):
            if callback_id in self._events[k]:
                del self._events[k][callback_id]
                if len(self._events[k]) == 0:
                    del self._events[k]
        if len(self._events) == 0:
            logger.debug("no events , stop listening")
            self.stop()

    def _clear_event_handlers(self):
            for k in list(self._events.keys()):
                for callback_id in list(self._events[k].keys()):
                        del self._events[k][callback_id]
                del self._events[k]

    def _on_game_event(self, event_name, msg):
        if event_name in self._events.keys():
            for callback_id in self._events[event_name]:
                callback = self._events[event_name][callback_id];
                callback(UserEventTriggerred.from_json(msg))
               
    def run(self):
        self._is_run = True
        '''
            set daemon true to stop listen when main thread exit
        '''
        threading.Thread(target=self._start_listen, daemon=True).start()

    def stop(self):
        self._is_run = False
        self._clear_event_handlers()

    def is_stopped(self) -> bool:
        return not self._is_run
 
    def _start_listen(self):
        q = self._client.listen_event("GameLogic.userEventTriggerred")
        self._client.exec(enable_user_event())
        while True:
            try:
                message = q.get(block=True)
            except queue.Empty:
                logger.warn("listen event queue is empty")
            if "body" in message.keys():
                body = message["body"]
                if "name" in body.keys():
                    self._on_game_event(body["name"], message)

