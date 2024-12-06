from gautomator.tcp.ga_sdk_client import GASdkClient
from gautomator.protocol.actor import *

import logging

logger = logging.getLogger('Actor')

class Actor:

    def __init__(self, conn: GASdkClient):
        self._conn = conn
    
    @property
    def location(self) -> str:
        """
            Gets the current location of the cursor.

            Returns:
            A string representing the current location of the cursor.
        """
        return self._conn.exec(get_location())[1]

    def set_location(self, pos: Tuple[float, float, float]) -> bool: 
        """
            Sets the location of the cursor.

            Args:
            pos: A tuple of three floats representing the new position of the cursor.
            
            Returns:
            A boolean indicating whether the operation was successful.
        """
        return self._conn.exec(set_location(pos))

    def yaw(self, value: float) -> bool: 
        """
            Rotates the cursor around the y-axis.

            Args:
            value: A float representing the angle of rotation in degrees.

            Returns:
            A boolean indicating whether the operation was successful.
        """
        return self._conn.exec(yaw(value))
    
    def roll(self, value: float) -> bool: 
        """
            Rotates the cursor around the x-axis.

            Args:
            value: A float representing the angle of rotation in degrees.

            Returns:
            A boolean indicating whether the operation was successful.
        """
        return self._conn.exec(roll(value))
    
    def pitch(self, value: float) -> bool: 
        """
            Rotates the cursor around the z-axis.

            Args:
            value: A float representing the angle of rotation in degrees.

            Returns:
            A boolean indicating whether the operation was successful.
        """
        return self._conn.exec(pitch(value))
    
    def move_forward(self, value: float) -> bool: 
        """
            Moves the cursor forward.

            Args:
            value: A float representing the distance to move.

            Returns:
            A boolean indicating whether the operation was successful.
        """
        return self._conn.exec(move_forward(value))
    
    def move_right(self, value: float) -> bool: 
        """
             Moves the cursor to the right.

            Args:
            value: A float representing the distance to move.

            Returns:
            A boolean indicating whether the operation was successful.
        """
        return self._conn.exec(move_right(value))