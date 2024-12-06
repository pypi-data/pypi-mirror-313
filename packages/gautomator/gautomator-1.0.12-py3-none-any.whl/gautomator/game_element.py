from typing import Dict, Optional, Union, Tuple
from numbers import Number

from gautomator.click_type import ClickType
from gautomator.element_type import ElementType
from gautomator.common.exceptions import GAutomatorException
from gautomator.context import Context

import logging

logger = logging.getLogger('GameElement')

class GameElement:

    def __init__(self, gauto, element_type, data, widget_info=None, deferred_load=False):
        self._gauto = gauto
        self._element_type = element_type
        self._data = dict(data)
        self._widget_info = widget_info
        self._deferred_load = deferred_load

    def _load_attributes(self):  # non-threadsafe function
        attributes = self._gauto._get_attributes(self._widget_info)
        self._data = dict(attributes)
        self._deferred_load = False
        pass

    def get_attribute(self, name: str, default_value: str = None) -> Optional[Union[str, Dict]]:
        if name in self._data:
            return self._data.get(name)

        if self._deferred_load:
            self._load_attributes()

        return self._data.get(name, default_value)

    @property
    def visible(self) -> bool:
        """Whether the element is visible to a user.

        """
        visibility = self.get_attribute("visibility", "hidden")
        return visibility == "Visible" or  visibility == "HitTestInvisible" or  visibility == "SelfHitTestInvisible"

    @property
    def enabled(self) -> bool:
        """Whether the element is enabled.

        """
        return self.get_attribute("isEnabled", "false") == "true"

    @property
    def checked(self) -> bool:
        """Whether the checkbox is checked.

        """
        return self.get_attribute("isChecked", "false") == "true"

    @property
    def interactable(self) -> bool:
        """Whether the checkbox is checked.

        """
        return self.get_attribute("isInteractable", "false") == "true"

    @property
    def volatile(self) -> bool:
        """Whether the checkbox is checked.

        """
        return self.get_attribute("isVolatile", "false") == "true"

    @property
    def accessible(self) -> bool:
        """Whether the checkbox is checked.

        """
        return self.get_attribute("isAccessible", "false") == "true"

    @property
    def accessible_text(self) -> bool:
        """Whether the checkbox is checked.

        """
        return self.get_attribute("accessibleText", "")

    @property
    def name(self) -> str:
        return self.get_attribute("name", "")

    @property
    def class_name(self) -> str:
        return self.get_attribute("className", "")

    @property
    def map_name(self) -> str:
        return self.get_attribute("map", "")

    @property
    def x(self) -> Number:
        return float(self.get_attribute("x", "0"))

    @property
    def y(self) -> Number:
        return float(self.get_attribute("y", "0"))

    @property
    def unique_id(self) -> str:
        return int(self.get_attribute("uniqueID", "-1"))

    @property
    def serial_number(self) -> str:
        return self.get_attribute("serialNumber", None)

    @property
    def id(self) -> str:
        return self.get_attribute("id", None)

    @property
    def type(self) -> str:
        return self.get_attribute("type", None)

    @property
    def title(self) -> str:
        return self.get_attribute("title", None)

    @property
    def address(self) -> str:
        return self.get_attribute("address", None)

    @property
    def text(self) -> str:
        return self.get_attribute("text", None)

    def set_text(self, text: str = '') -> bool:
        """Sends text to the element.

        """
        return self._gauto._set_text(self.name, text, self.unique_id)

    def click(self, click_type: str = ClickType.SIMULATED_LOCATION_TOUCH) -> bool:
        """Click the element.

        """
        logging.debug("_element_type:%s", self._element_type)
        if self._element_type == ElementType.UWIDGET:
            return self._gauto._click(click_type, self.name, self.unique_id)
        elif self._element_type == ElementType.SWIDGET:
            return self._gauto._click(click_type, self.name, self.address)
        
    def set_checked_state(self, checked_state: bool) -> bool:
        """Set checked state of the element.

        """
        return self._gauto._set_checkbox(self.name, checked_state, self.unique_id)

    def get_parent(self):
        """Get this GameElement's parent GameElement.

        """
        if self._element_type == ElementType.UWIDGET:
            return self._gauto._get_parent("uniqueID", str(self.unique_id))
        elif self._element_type == ElementType.SWIDGET:
            return self._gauto._get_parent("address", self.address)

    def get_location(self) -> Tuple[float, float]:
        screen_size = self._gauto._get_screen_size()
        width = screen_size[0]
        height = screen_size[1]
        if width == 0 or height == 0:
            logger.error("can not get screen size")
            raise GAutomatorException("can not get screen size")
        else:   
            if self._gauto.context == Context.UE_SLATE:
                center_x = float(self.get_attribute("centerX", "0"))
                center_y = float(self.get_attribute("centerY", "0"))
            else:
                el_width = float(self.get_attribute("width", "0"))
                el_height = float(self.get_attribute("height", "0"))
                center_x = self.x + el_width/2
                center_y = self.y + el_height/2
            return (center_x/width, center_y/height)
