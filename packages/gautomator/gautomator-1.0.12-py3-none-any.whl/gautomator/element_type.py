"""The By implementation."""

from enum import Enum, unique


class ElementType(object):
    """
    Set of supported locator strategies.
    """

    UWIDGET = "UWidget"
    SWIDGET = "SWidget"
    GAMEOBJECT = "GameObject"
