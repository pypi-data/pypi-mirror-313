"""The By implementation."""

from enum import Enum, unique


class ClickType(object):
    """
    Set of supported locator strategies.
    """

    AUTO = "auto"
    TRIGGERING_EVENT = "triggeringEvent"
    SIMULATED_LOCATION_TOUCH = "simulatedLocationTouch"
