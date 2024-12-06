import datetime
import logging
import threading
import time
import os

from typing import List, Tuple, Callable
from .context import Context
from .game_actor import Actor
from .by import *
from .common.const import AKEY_EVENT_ACTION_DOWN, AKEY_EVENT_ACTION_UP, AKEY_EVENT_ACTION_MOVE
from .context import Context
from .game_event_manager import GameEventManager
from .game_element import GameElement
from .game_element_finder import GameElementFinder
from .tcp.ga_sdk_client import GASdkClient
from .protocol.common import *
from .protocol.slate import *
from .protocol.umg import *
from .protocol.touch import *
from gautomator.reflect.game_method import GameMethods
from .common.exceptions import GAutomatorException, NoSuchElementException, NotImplementedException

logger = logging.getLogger('gautomator')


class GAutomator(Context):

    def __init__(
        self,
        device_type: str,
        udid: str = "",
        port: int = 27029,
        enable_logging: bool = True,
        timeout_seconds: int = 15,
    ):
        """
        Args:
            device_type (str): The connected device type, android, iOS or local.
            udid (str): android serial number or iOS udid, default to the only connected one.
                        If device_type is local, udid is "127.0.0.1".
            port (int): The port number to use for the connection, defaults to 27029.
                        If device_type is local, please use forwarded port number.
            enable_logging (bool): Whether to enable logging. Defaults to True.
            timeout_seconds (int): The number of seconds to wait for a response from the server before timing out. Defaults to 15.

        Description:
            This method initializes a new instance of the CursorTutor class with the specified parameters.
            The host and port parameters are used to connect to the server, while the enable_logging parameter determines whether logging is enabled or not.
            The timeout_seconds parameter specifies the number of seconds to wait for a response from the server before timing out.
            If "GA_SDK_PORT" env set, use it, else use port instead
        """
        logger.debug("timeout_seconds=%d", timeout_seconds)
        self._device_type = device_type
        self._udid = udid
        self._port = port
        self.enable_logging = enable_logging
        self._context = Context.UE_UMG
        self._timeout_seconds = timeout_seconds
        self._sdk_client = GASdkClient(
            self._device_type, self._udid, self._port, timeout_seconds
        )
        self._event_manager = GameEventManager(self._sdk_client)
        self._health_check_thread = None 
        self._wait_engine_ready()

    def _wait_engine_ready(self) -> None:
        for i in range(self._timeout_seconds):
            try:
                res = self._sdk_client.exec(get_engine_info())
                if res[0] == RespStatus.SuccessJson.value:
                    return
            except GAutomatorException:
                logger.warn("GAutomatorException engine not ready, retry it")
            except ConnectionError:
                logger.warn("ConnectionError engine not ready, retry it")
            time.sleep(1)
        raise GAutomatorException("wait engine ready timeout")

    def _health_check(self, tick_time, exception_callback: Callable = None) -> None:
        """Detect engine link status every tick_time seconds.
        
        Heart beats check is necessary, because if you use goios forward,
        tidevice relay or iproxy to connect the game sdk engine，
        you can not detect connection closed by tcp.

        Args: tick_time, min tick_time 5 second

        """
        logger.debug("start heart_beats tick_time=%d", tick_time)
        while True:
            if tick_time < 5:
                tick_time = 5
            time.sleep(tick_time)
            try:
                res = self._sdk_client.exec(is_alive(tick_time))
                logger.debug("heart_beats:%s", res)
            except Exception as e:
                logger.error("cancel heart_beats, exception detected:%s", e, exc_info=True)
                """
                    Exit process when trio exception detected
                """
                if exception_callback:
                    exception_callback()
                break

    def _context_get_attributes(self, context, widget_info):
        if context == Context.UE_UMG:
            return self._sdk_client.exec(umg_get_attributes(widget_info=widget_info))
        elif context == Context.UE_SLATE:
            raise NotImplementedException
        elif context == Context.UE_ACTOR:
            raise NotImplementedException

    def _get_attributes(self, widget_info) -> bool:
        res = self._context_get_attributes(self._context, widget_info)
        return res

    def _context_get_parent(self, context, this_find_by, this_find_by_value):
        source = self.page_source
        finder = GameElementFinder(gauto=self, xml=source)
        game_elements = finder.find_by_and_get_parent(this_find_by, this_find_by_value)
        if len(game_elements) > 0:
            return game_elements[0]
        else:
            raise NoSuchElementException()

    def _set_checkbox(self, name: str, checked_state: bool, unique_id: int = -1) -> bool:
        if self._context == Context.UE_UMG:
            return self._sdk_client.exec(umg_set_checkbox(name, checked_state, unique_id))
        else:
            raise NotImplementedException()

    def _set_text(self, name: str, text: str, unique_id: int = -1) -> bool:
        if self._context == Context.UE_UMG:
            return self._sdk_client.exec(umg_set_text(name, text, unique_id))
        else:
            raise NotImplementedException()

    def _get_parent(self, this_find_by: str, this_find_by_value: str = None) -> GameElement:
        res = self._context_get_parent(self._context, this_find_by, this_find_by_value)
        return res

    def _click(self, click_type: str, name: str, unique_identifier: typing.Union[str, int]) -> bool:
        if self._context == Context.UE_UMG:
            res = self._sdk_client.exec(umg_click(click_type, name, unique_identifier))
        elif self._context == Context.UE_SLATE:
            res = self._sdk_client.exec(slate_click(name=name, address=unique_identifier))
            return res[0] == RespStatus.SuccessJson

    def _context_find_game_elements(self, by: By = By.NAME, value: str = None,
                                        find_in_context=Context.CURRENT_CONTEXT) -> List[GameElement]:
        if find_in_context == Context.ALL_CONTEXTS:
            return []  # TODO: find in all context

        if find_in_context == Context.CURRENT_CONTEXT:
            context = self._context

        if context == Context.UE_UMG:
            if by == By.NAME:
                uwidget_info = self._sdk_client.exec(umg_find_widget(by, value))
                finder = GameElementFinder(gauto=self, xml="")
                return finder.construct_game_elements_from_uwidget_info(uwidget_info)
            else:
                source = self.page_source
                finder = GameElementFinder(gauto=self, xml=source)
                return finder.find_by(by, value)
        elif context == Context.UE_SLATE:
            source = self.page_source
            finder = GameElementFinder(gauto=self, xml=source)
            return finder.find_by(by, value)

    def _get_screen_size(self, timeout_seconds: int = 15) -> Tuple[int, int]:
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
        return self._sdk_client.exec(get_screen_size(timeout_seconds=timeout_seconds))

    @property
    def page_source(self) -> str:
        # Returns the ue element xml tree of the current page.
        result:dict = self._sdk_client.exec(get_source(self._context))
        return result[1]["source"]

    @property
    def engine_info(self) -> str:
        """
        Returns information about the game engine being used.
        @return: A string containing information about the game engine.
        """
        result:dict = self._sdk_client.exec(get_engine_info())
        return result[1]

    def find_game_elements(self, by: By = By.NAME, value: str = None,
                        find_in_context=Context.CURRENT_CONTEXT, timeout_seconds = 15) -> List[GameElement]:
        """
        Finds game elements based on the specified locator strategy and value.
        
        Args:
            by (By): The locator strategy to use. Defaults to By.NAME.
            value (str): The value to search for. Defaults to None.
            find_in_context (Context): The context to search in. Defaults to Context.CURRENT_CONTEXT.
        
        Returns:
            List[GameElement]: The game element that was found.
        """
        start_time = datetime.datetime.now()
        while True:
            res = self._context_find_game_elements(by, value, find_in_context)
            if len(res) > 0:
                return res
            current_time = datetime.datetime.now()
            if (current_time - start_time).total_seconds() >= timeout_seconds:
                raise NoSuchElementException()
            time.sleep(1)

    def find_game_element(self, by: By = By.NAME, value: str = None,
                        find_in_context=Context.CURRENT_CONTEXT, timeout_seconds = 15) -> GameElement:
        """
        Finds a game element based on the specified locator strategy and value.
        
        Args:
            by (By): The locator strategy to use. Defaults to By.NAME.
            value (str): The value to search for. Defaults to None.
            find_in_context (Context): The context to search in. Defaults to Context.CURRENT_CONTEXT.
        
        Returns:
            GameElement: The game element that was found.
        """
        start_time = datetime.datetime.now()
        while True:
            res = self._context_find_game_elements(by, value, find_in_context)
            if len(res) > 0:
                return res[0]
            current_time = datetime.datetime.now()
            if (current_time - start_time).total_seconds() >= timeout_seconds:
                raise NoSuchElementException()
            time.sleep(1)

    def screenshot(self, save_path:str, timeout_seconds: int =15) -> bool:
        """
        Takes a screenshot of the current screen and saves it to the specified path.
        Args:
            save_path (str): The path where the screenshot will be saved.
        Returns:
            True if success .
        """
        res = self._sdk_client.exec(screenshot(self._context, save_path, timeout_seconds))
        return res == RespStatus.SuccessJson

    def register_event_handler(self, event_name:  str, event_callback) -> str:
        """
        Registers an event handler for the specified event name. 
        The event handler is a function that will be called when the event is triggered. 
        The function should take one argument, which is the event data. 
        Returns a unique identifier for the registered event handler, which can be used to unregister the handler later. 

        Args:
            event_name (str): The name of the event to register the handler for.
            event_callback (function): The function to call when the event is triggered.

        Returns:
            str: A unique identifier for the registered event handler.
        """
        res = self._event_manager.register_event_handler(event_name, event_callback)
        return res

    def unregister_event_handler(self, game_event: str, callback_id):
        """
        Unregisters an event handler for a specific game event.

        Args:
            game_event (str): The name of the game event to unregister the handler for.
            callback_id: The ID of the callback function to unregister.

        Description:
            This method removes the specified callback function from the list of event handlers for the specified game event.
            If the callback function is not registered for the specified game event, this method does nothing.
        """
        self._event_manager.unregister_event_handler(game_event, callback_id)

    def unregister_all_events(self):
        # Unregisters all events for the current instance of the class.
        self._event_manager.stop()

    def on_key_up(self, key_code: int, key_action: int = 0) -> bool:
        """
            Handles key up events.
            Args:
                key_code (int): The code of the released key.
            Returns:
                bool: True if the event was handled, False otherwise.
        """
        res = self._sdk_client.exec(slate_on_key_event(key_code, AKEY_EVENT_ACTION_UP | key_action))
        return res

    def on_key_down(self, key_code: int, key_action: int = 0) -> bool:
        """
        Handles key down events.

        Args:
            key_code (int): The code of the key that was pressed.

        Returns:
            bool: True if the event was handled, False otherwise.

        Description:
            This method is called when a key is pressed down. 
            It handles the event by updating the state of the tutor accordingly. 
            If the event was handled, it returns True, otherwise it returns False.
        """
        res = self._sdk_client.exec(slate_on_key_event(key_code, AKEY_EVENT_ACTION_DOWN | key_action))
        return res

    def keyevent(self, key_code: int, duration: float = 0.05, key_action: int = 0) -> bool:
        """
        Method to simulate a key press event with given key code and duration
        This method is only avaliable for editor or pc client

        Args:
            key_code (int): The code of the key that was pressed.

        Returns:
            bool: True if the event was handled, False otherwise.

        """
        success = self.on_key_down(key_code, key_action)
        if not success:
            return False
        time.sleep(duration)
        success = self.on_key_up(key_code)
        return success

    def touch_down(self, pos: Tuple[float, float], pointer_id:int = 0, by_scrycpy: bool = True) -> typing.Union[int, bool]:
        """
        Called when the user touches down on the screen.
        Args:
            pos: A tuple of floats representing the (x, y) position of the touch.
        Returns:
            An integer representing the unique identifier for the touch event.
        """
        if by_scrycpy:
            size = ScreenSize(width=1920, height=1080)
            down_pos = Position(screen_size=size, point=Point(size.width * pos[0], size.height * pos[1]))
            return self._sdk_client.exec((scrcpy_touch_event(AKEY_EVENT_ACTION_DOWN, pointer_id, down_pos)))
        else :
            res = self._sdk_client.exec(slate_begin_touch({"x": pos[0], "y": pos[1]}))
            return res[1]

    def touch_move(self, pos: Tuple[float, float], pointer_id:int = 0, index: int = 0, by_scrycpy: bool = True) -> bool:
        """
        Move the cursor to a new position on the screen.

        Args:
            index (int): The index of the cursor to move.
            pos (Tuple[float, float]): The new position of the cursor as a tuple of (x, y) coordinates.

        Returns:
            bool: True if the cursor was successfully moved, False otherwise.

        Description:
            This method updates the position of the cursor with the given index to the new position specified by the pos argument.
        """
        if by_scrycpy:
            size = ScreenSize(width=1920, height=1080)
            move_pos = Position(screen_size=size, point=Point(size.width * pos[0], size.height * pos[1]))
            return self._sdk_client.exec((scrcpy_touch_event(AKEY_EVENT_ACTION_MOVE, pointer_id, move_pos)))
        else:
            res = self._sdk_client.exec(slate_move_touch( index, {"x": pos[0], "y": pos[1]}, 1))
            return res

    def touch_up(self,  pos: Tuple[float, float], pointer_id:int = 0, index: int = 0, by_scrycpy: bool = True) -> bool:
        """
        Touch up event handler for a specific cursor.

        Args:
            index (int): The index of the cursor to handle touch up event.

        Returns:
            bool: True if the touch up event is handled successfully, False otherwise.

        Description:
            This method is called when the user lifts their finger off the screen while touching a specific cursor. 
            It handles the touch up event by updating the cursor's state and returning True if the touch up event 
            is handled successfully. Otherwise, it returns False.
        """
        if by_scrycpy:
            size = ScreenSize(width=1920, height=1080)
            up_pos = Position(screen_size=size, point=Point(size.width * pos[0], size.height * pos[1]))
            return self._sdk_client.exec((scrcpy_touch_event(AKEY_EVENT_ACTION_UP, pointer_id, up_pos)))
        else:
            res = self._sdk_client.exec(slate_end_touch(index))
            return res[1]

    def touch(self, pos: Tuple[float, float], duration: float = 0.01) -> bool:
        """
        Function to simulate a touch event at a given position with an optional duration
        
        Args:
            pos: The position to touch
            duration: The duration of the touch event (default 0.01 seconds)

        Returns: 
            True if the touch event was successful, False otherwise
        """
        if duration < 0 :
            logger.error("duration must be non-negative")
            return False

        size = ScreenSize(width=1920, height=1080)
        touch_pos = Position(screen_size=size, point=Point(size.width * pos[0], size.height * pos[1]))
        res_down = self._sdk_client.exec((scrcpy_touch_event(AKEY_EVENT_ACTION_DOWN, 0, touch_pos)))
        time.sleep(duration)
        res_up = self._sdk_client.exec((scrcpy_touch_event(AKEY_EVENT_ACTION_UP, 0, touch_pos)))
        return res_down and res_up

    def swipe(self, source: Tuple[float, float], dest: Tuple[float, float], steps:int = 15, 
              step_duration:float = 0.05, down_duration:float = 0.05, up_duration:float = 0.05) -> bool:
        """
        Function to simulate a swipe event at a given position with an optional duration
        """
        if steps < 1:
            logger.error("steps must be greate than 1")
            return False

        if step_duration < 0 :
            logger.error("step_duration must be non-negative")
            return False

        if down_duration < 0 :
            logger.error("down_duration must be non-negative")
            return False

        if up_duration < 0 :
            logger.error("up_duration must be non-negative")
            return False

        size = ScreenSize(width=1920, height=1080)
        source_pos = Position(screen_size=size, point=Point(size.width * source[0], size.height * source[1]))
        dest_pos = Position(screen_size=size, point=Point(size.width * dest[0], size.height * dest[1]))

        res_down = self._sdk_client.exec((scrcpy_touch_event(AKEY_EVENT_ACTION_DOWN, 0, source_pos)))
        if not res_down:
            return False
        time.sleep(down_duration)
        step_x = abs(dest_pos.point.x - source_pos.point.x) / steps
        step_y = abs(dest_pos.point.y - source_pos.point.y) / steps
        if dest_pos.point.x < source_pos.point.x:
            step_x = -step_x

        if dest_pos.point.y < source_pos.point.y:
            step_y = -step_y
        logger.debug("step_x=%d, step_y=%d", step_x, step_y)

        current_pos = source_pos
        for i in range(steps):
            x = current_pos.point.x + step_x
            y = current_pos.point.y + step_y
            point = Point(x, y)
            pos = Position(point, source_pos.screen_size)
            res_move = self._sdk_client.exec((scrcpy_touch_event(AKEY_EVENT_ACTION_MOVE, 0, pos)))
            if not res_move:
                return False
            current_pos = pos
            time.sleep(step_duration)
        time.sleep(up_duration)
        res_up = self._sdk_client.exec((scrcpy_touch_event(AKEY_EVENT_ACTION_UP, 0, dest_pos)))
        return res_up

    def get_actor(self) -> Actor:
        """
        Get first play actor in ue engine.
        """
        return Actor(self._sdk_client)

    def send_msg(self, msg: str, event_name: str = "", timeout_seconds: int =15) -> typing.Tuple[bool, str]:
        """
        Sends a message to the sdk server.
        Args:
            msg: The message to send.
        Returns:
            A string indicating the status of the message sending process.
        """
        res = self._sdk_client.exec(call_user_command(msg, event_name, timeout_seconds))
        logger.debug("_call_user_command %s res :%s", event_name, res)
        return res

    def enable_health_check(self, tick_time:int =10, exception_callback: Callable = None) -> bool:
        """
        Enable health check function with optional tick time and exception callback parameters

        Args:
          tick_time: int - time interval in seconds between health checks (default 10 seconds)
          exception_callback: Callable - function to be called if an exception occurs during health check (default None)
        
        Returns: 
          bool - True if health check is enabled successfully, False otherwise
        """
        if self._health_check_thread:
            logger.info("health thread already created")
        else:
            self._health_check_thread = threading.Thread(target=self._health_check, args=(tick_time, exception_callback), daemon=True)
            self._health_check_thread.start()
        return True

    def set_filter(self, show_hidden_el:bool ) -> bool:
        """
        Set filter criteria for dump elements

        Args:
          show_invisible: bool - The args to set if dump hidden elements
         
        Returns: 
          bool - True if filter is setted
        """
        return self._sdk_client.exec(set_filter(self._context, show_hidden_el))

    def exec_console_cmd(self, cmd:str , timeout_seconds: int = 15) -> bool:
        """
        Exec console cmd in game process

        Args:
          cmd: str - The exec cmd of console
          timeout_seconds: - The timeout for exec cmd of console
        Returns: 
          str - The cmd result of console
        """
        return self._sdk_client.exec(exec_console_cmd(cmd, timeout_seconds))

    def get_game_methods(self, methods:typing.OrderedDict[str, OPFunction], out:str) -> GameMethods:
        return GameMethods(self._sdk_client, methods, out)
