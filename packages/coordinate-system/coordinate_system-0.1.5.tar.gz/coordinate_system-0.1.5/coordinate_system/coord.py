import ctypes
import sys
import os

sys.path.append(os.getcwd())

import coordinate_system

class coord3:
    def __init__(self, x, y, z):
        self.coord = coordinate_system.coord3(x, y, z)

    def __add__(self, other):
        if isinstance(other, coord3):
            result = self.coord + other.coord
            return coord3(result.pos().x, result.pos().y, result.pos().z)
        raise TypeError("Operand must be of type 'coord3'")

    def __sub__(self, other):
        if isinstance(other, coord3):
            result = self.coord - other.coord
            return coord3(result.pos().x, result.pos().y, result.pos().z)
        raise TypeError("Operand must be of type 'coord3'")

    def __mul__(self, other):
        if isinstance(other, coord3):
            result = self.coord * other.coord
            return coord3(result.pos().x, result.pos().y, result.pos().z)
        raise TypeError("Operand must be of type 'coord3'")

    def __truediv__(self, other):
        if isinstance(other, coord3):
            result = self.coord / other.coord
            return coord3(result.pos().x, result.pos().y, result.pos().z)
        raise TypeError("Operand must be of type 'coord3'")

    def __repr__(self):
        pos = self.coord.pos()
        return f"<coord3 ({pos.x}, {pos.y}, {pos.z})>"

    def to_vec3(self):
        """Convert to vec3 representation."""
        return self.coord.tovec()