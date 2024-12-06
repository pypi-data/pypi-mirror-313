"""The By implementation."""

from enum import Enum, unique


class By(object):
    """
    Set of supported locator strategies.
    """

    XPATH = "xpath"
    NAME = "name"
    CLASS_NAME = "className"
    TEXT = "text"
    WIDGET_PATH = "widgetPath"
    TYPE = "type"
