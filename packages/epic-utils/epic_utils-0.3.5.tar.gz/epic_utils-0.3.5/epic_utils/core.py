from .decorator import ClassProperty, ForceArgType, MeasureTime
from .error import ErrorHandler
from typing import Union
import math


class Converter:
    def dec2hex(value : int):
        h = hex(value)
        result = str.upper(h[2:])
        if len(result) < 2:
            result = "0" + result
        return result
class Vector2():
    def __init__(self, x : float, y : float):
        self.x : float = x
        self.y : float = y
    @property
    def this(self):
        return [self.x, self.y]    
    def set(self, x : float, y : float):
        self.x = x
        self.y = y
    def setX(self, x : float):
        self.x = x
    def setY(self, y : float):
        self.y = y
    @property
    def sqrMagnitude(self):
        return self.x**2 + self.y**2
    @property
    def magnitude(self):
        return math.sqrt(self.sqrMagnitude)
    @property
    def normalized(self): 
        mag = self.magnitude
        return Vector2(self.x/mag, self.y/mag)
    def toTuple(self):
        return (self.x, self.y)
    def toList(self):
        return [self.x, self.y]
    
    @staticmethod
    @ForceArgType("Vector2", "Vector2")
    def sqrDistance(vector1, vector2):
        return abs(vector2.x - vector1.x)**2 + abs(vector2.y - vector1.y)**2
    @staticmethod
    @ForceArgType("Vector2", "Vector2")
    def distance(vector1, vector2) -> float:
        return math.sqrt(Vector2.sqrDistance(vector1, vector2))
    
    @staticmethod
    @ForceArgType(tuple)
    def fromArray(array : tuple):
        if len(array) < 2:
            ErrorHandler.raiseError(IndexError, f"length <2> expected, got length <{len(array)}>")
        return Vector2(array[0], array[1])
    @staticmethod
    @ForceArgType(dict)
    def fromDict(dictionary : dict):
        keys = list(dictionary.keys())
        if not ("x" in keys and "y" in keys):
            ErrorHandler.raiseError(KeyError, f"keys <x,y> expected, got keys <{','.join(keys)}>")
        return Vector2(dictionary["x"], dictionary["y"])
    @staticmethod
    def max(*args):
        result = Vector2.negativeInfinity
        for vector in args:
            if not ErrorHandler.isType(vector, Vector2):
                continue
            result.x = max(result.x, vector.x)
            result.y = max(result.y, vector.y)
        return result
    @staticmethod
    def min(*args):
        result = Vector2.positiveInfinity
        for vector in args:
            if not ErrorHandler.isType(vector, Vector2):
                continue
            result.x = min(result.x, vector.x)
            result.y = min(result.y, vector.y)
        return result
    
    @staticmethod
    def LinearInterpolation(start, end, time):
        return start + (end - start) * time
    
    @staticmethod
    def QuadraticBezierInterpolation(p0, p1, p2, time):
        tempA = Vector2.LinearInterpolation(p0, p1, time)
        tempB = Vector2.LinearInterpolation(p1, p2, time)
        return Vector2.LinearInterpolation(tempA, tempB, time)
    @staticmethod
    def CubicBezierInterpolation(p0, p1, p2, p3, time : float):
        tempA = Vector2.LinearInterpolation(p0, p1, time)
        tempB = Vector2.LinearInterpolation(p1, p2, time)
        tempC = Vector2.LinearInterpolation(p2, p3, time)
        
        return Vector2.QuadraticBezierInterpolation(tempA, tempB, tempC, time)
    @ClassProperty
    def one(cls):
        return Vector2(1, 1)
    @ClassProperty
    def zero(cls):
        return Vector2(0, 0)
    @ClassProperty
    def up(cls):
        return Vector2(0, 1)
    @ClassProperty
    def down(cls):
        return Vector2(0, -1)
    @ClassProperty
    def left(cls):
        return Vector2(-1, 0)
    @ClassProperty
    def right(cls):
        return Vector2(1, 0)
    @ClassProperty
    def positiveInfinity(cls):
        return Vector2(math.inf, math.inf)
    @ClassProperty
    def negativeInfinity(cls):
        return Vector2(-math.inf, -math.inf)
    
    def __eq__(self, other):
        if ErrorHandler.isType(other, Vector2) or ErrorHandler.isType(other, Vector2Int):
            return self.x == other.x and self.y == other.y
        return self.x == other and self.y == other
    
    def __add__(self, value):
        if ErrorHandler.isType(value, Vector2) or ErrorHandler.isType(value, Vector2Int):
            return Vector2(self.x + value.x, self.y + value.y)
        return Vector2(self.x + value, self.y + value)
    def __sub__(self, value):
        if ErrorHandler.isType(value, Vector2) or ErrorHandler.isType(value, Vector2Int):
            return Vector2(self.x - value.x, self.y - value.y)
        return Vector2(self.x - value, self.y - value)    
    def __mul__(self, value):
        if ErrorHandler.isType(value, Vector2) or ErrorHandler.isType(value, Vector2Int):
            return Vector2(self.x * value.x, self.y * value.y)
        return Vector2(self.x * value, self.y * value)
    def __div__(self, value):
        if ErrorHandler.isType(value, Vector2) or ErrorHandler.isType(value, Vector2Int):
            if value.x == 0.0 or value.y == 0.0:
                ErrorHandler.raiseError(ZeroDivisionError, "")    
            return Vector2(self.x / value.x, self.y / value.y)
        if value == 0.0:
            ErrorHandler.raiseError(ZeroDivisionError, "")
        return Vector2(self.x / value, self.y / value)
    def __truediv__(self, value):
        if ErrorHandler.isType(value, Vector2) or ErrorHandler.isType(value, Vector2Int):
            if value.x == 0.0 or value.y == 0.0:
                ErrorHandler.raiseError(ZeroDivisionError, "")    
            return Vector2(self.x / value.x, self.y / value.y)
        if value == 0.0:
            ErrorHandler.raiseError(ZeroDivisionError, "")
        return Vector2(self.x / value, self.y / value) 
    def __pow__(self, value):
        if ErrorHandler.isType(value, Vector2) or ErrorHandler.isType(value, Vector2Int):
            return Vector2(self.x **value.x, self.y**value.y)
        return Vector2(self.x**value, self.y**value)
    
    def __str__(self):
        return f"Vector2({self.x}, {self.y})"
    
class Vector2Int():
    def __init__(self, x : int, y : int):
        self.x : int = int(x)
        self.y : int = int(y)
    @property
    def this(self):
        return [self.x, self.y]    
    
    def set(self, x : int, y : int):
        self.x = int(x)
        self.y = int(y)
    def setX(self, x : int):
        self.x = int(x)
    def setY(self, y : int):
        self.y = int(y)
    
    @property
    def sqrMagnitude(self):
        return self.x**2 + self.y**2
    @property
    def magnitude(self):
        return math.sqrt(self.sqrMagnitude)
    @property
    def normalized(self): 
        mag = self.magnitude
        return Vector2Int(self.x/mag, self.y/mag)
    def toTuple(self):
        return (self.x, self.y)
    def toList(self):
        return [self.x, self.y]
    
    @staticmethod
    @ForceArgType("Vector2Int", "Vector2Int")
    def sqrDistance(vector1, vector2):
        return abs(vector2.x - vector1.x)**2 + abs(vector2.y - vector1.y)**2
    @staticmethod
    @ForceArgType("Vector2Int", "Vector2Int")
    def distance(vector1, vector2) -> float:
        return math.sqrt(Vector2Int.sqrDistance(vector1, vector2))
    
    @staticmethod
    @ForceArgType(tuple)
    @MeasureTime
    def fromArray(array : tuple):
        if len(array) < 2:
            ErrorHandler.raiseError(IndexError, f"length <2> expected, got length <{len(array)}>")
        return Vector2Int(array[0], array[1])
    @staticmethod
    @ForceArgType(dict)
    @MeasureTime
    def fromDict(dictionary : dict):
        keys = list(dictionary.keys())
        if not ("x" in keys and "y" in keys):
            ErrorHandler.raiseError(KeyError, f"keys <x,y> expected, got keys <{','.join(keys)}>")
        return Vector2Int(dictionary["x"], dictionary["y"])
    @staticmethod
    def max(*args):
        result = Vector2Int.negativeInfinity
        for vector in args:
            if not ErrorHandler.isType(vector, Vector2Int):
                continue
            result.x = max(result.x, vector.x)
            result.y = max(result.y, vector.y)
        return result
    @staticmethod
    def min(*args):
        result = Vector2Int.positiveInfinity
        for vector in args:
            if not ErrorHandler.isType(vector, Vector2Int):
                continue
            result.x = min(result.x, vector.x)
            result.y = min(result.y, vector.y)
        return result
    
    @staticmethod
    def LinearInterpolation(start, end, time):
        return start + (end - start) * time
    
    @staticmethod
    def QuadraticBezierInterpolation(p0, p1, p2, time):
        tempA = Vector2Int.LinearInterpolation(p0, p1, time)
        tempB = Vector2Int.LinearInterpolation(p1, p2, time)
        return Vector2Int.LinearInterpolation(tempA, tempB, time)
    @staticmethod
    def CubicBezierInterpolation(p0, p1, p2, p3, time : float):
        tempA = Vector2Int.LinearInterpolation(p0, p1, time)
        tempB = Vector2Int.LinearInterpolation(p1, p2, time)
        tempC = Vector2Int.LinearInterpolation(p2, p3, time)
        
        return Vector2Int.QuadraticBezierInterpolation(tempA, tempB, tempC, time)
    @ClassProperty
    def one(cls):
        return Vector2Int(1, 1)
    @ClassProperty
    def zero(cls):
        return Vector2Int(0, 0)
    @ClassProperty
    def up(cls):
        return Vector2Int(0, 1)
    @ClassProperty
    def down(cls):
        return Vector2Int(0, -1)
    @ClassProperty
    def left(cls):
        return Vector2Int(-1, 0)
    @ClassProperty
    def right(cls):
        return Vector2Int(1, 0)
    @ClassProperty
    def positiveInfinity(cls):
        return Vector2Int(math.inf, math.inf)
    @ClassProperty
    def negativeInfinity(cls):
        return Vector2Int(-math.inf, -math.inf)
    
    def __eq__(self, other):
        if ErrorHandler.isType(other, Vector2Int) or ErrorHandler.isType(other, Vector2):
            return self.x == other.x and self.y == other.y
        return self.x == other and self.y == other
    def __add__(self, value):
        if ErrorHandler.isType(value, Vector2Int) or ErrorHandler.isType(value, Vector2):
            return Vector2Int(self.x + value.x, self.y + value.y)
        return Vector2Int(self.x + value, self.y + value)
    def __sub__(self, value):
        if ErrorHandler.isType(value, Vector2Int) or ErrorHandler.isType(value, Vector2):
            return Vector2Int(self.x - value.x, self.y - value.y)
        return Vector2Int(self.x - value, self.y - value)    
    def __mul__(self, value):
        if ErrorHandler.isType(value, Vector2Int) or ErrorHandler.isType(value, Vector2):
            return Vector2Int(self.x * value.x, self.y * value.y)
        return Vector2Int(self.x * value, self.y * value)
    def __div__(self, value):
        if ErrorHandler.isType(value, Vector2Int) or ErrorHandler.isType(value, Vector2):
            if value.x == 0.0 or value.y == 0.0:
                ErrorHandler.raiseError(ZeroDivisionError, "")    
            return Vector2Int(self.x / value.x, self.y / value.y)
        if value == 0.0:
            ErrorHandler.raiseError(ZeroDivisionError, "")
        return Vector2Int(self.x / value, self.y / value)
    def __truediv__(self, value):
        if ErrorHandler.isType(value, Vector2Int) or ErrorHandler.isType(value, Vector2):
            if value.x == 0.0 or value.y == 0.0:
                ErrorHandler.raiseError(ZeroDivisionError, "")    
            return Vector2Int(self.x / value.x, self.y / value.y)
        if value == 0.0:
            ErrorHandler.raiseError(ZeroDivisionError, "")
        return Vector2Int(self.x / value, self.y / value) 
    def __pow__(self, value):
        if ErrorHandler.isType(value, Vector2Int) or ErrorHandler.isType(value, Vector2):
            return Vector2Int(self.x **value.x, self.y**value.y)
        return Vector2Int(self.x**value, self.y**value)
    
    def __str__(self):
        return f"Vector2Int({self.x}, {self.y})"    

class Vector3():
    def __init__(self, x : float, y : float, z : float):
        self.x : float = x
        self.y : float = y
        self.z : float = z
    @property
    def this(self):
        return [self.x, self.y, self.z]    
    def set(self, x : float, y : float, z : float):
        self.x = x
        self.y = y
        self.z = z
    def setX(self, x : float):
        self.x = x
    def setY(self, y : float):
        self.y = y
    def setZ(self, z : float):
        self.z = z
    @property
    def sqrMagnitude(self):
        return self.x**2 + self.y**2 + self.z**2
    @property
    def magnitude(self):
        return math.sqrt(self.sqrMagnitude)
    @property
    def normalized(self): 
        mag = self.magnitude
        return Vector3(self.x/mag, self.y/mag, self.z/mag)
    
    def toTuple(self):
        return (self.x, self.y, self.z)
    def toList(self):
        return [self.x, self.y, self.z]
    
    def to_degrees(self):
        return Vector3(math.degrees(self.x), math.degrees(self.y), math.degrees(self.z))
    def to_radians(self):
        return Vector3(math.radians(self.x), math.radians(self.y), math.radians(self.z))

    @staticmethod
    def dot(v1, v2):
        if not (isinstance(v1, Vector3) and isinstance(v2, Vector3)):
            ErrorHandler.raiseError(TypeError, f"<Vector3, Vector3> expected, got <{type(v1).__name__},{type(v2).__name__}>")
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z
    @staticmethod
    def cross(v1, v2):
        if not (isinstance(v1, Vector3) and isinstance(v2, Vector3)):
            ErrorHandler.raiseError(TypeError, f"<Vector3, Vector3> expected, got <{type(v1).__name__},{type(v2).__name__}>")
        x = v1.y * v2.z - v1.z * v2.y
        y = v1.z * v2.x - v1.x * v2.z
        z = v1.x * v2.y - v1.y * v2.x
        return Vector3(x, y, z)
    @staticmethod
    def ProjectOnPlane(vector, plane_normal):
        if not (isinstance(vector, Vector3) and isinstance(plane_normal, Vector3)):
            ErrorHandler.raiseError(TypeError, f"<Vector3, Vector3> expected, got <{type(vector).__name__},{type(plane_normal).__name__}>")
        normal = plane_normal
        projection_length = Vector3.dot(vector, normal)
        projection_vector = normal * projection_length

        return vector - projection_vector
    @staticmethod
    def sqrDistance(vector1, vector2):
        if not (isinstance(vector1, Vector3) and isinstance(vector2, Vector3)):
            ErrorHandler.raiseError(TypeError, f"<Vector3, Vector3> expected, got <{type(vector1).__name__},{type(vector2).__name__}>")
        return abs(vector2.x - vector1.x)**2 + abs(vector2.y - vector1.y)**2 + abs(vector2.z - vector1.z)**2
    @staticmethod
    def distance(vector1, vector2) -> float:
        if not (isinstance(vector1, Vector3) and isinstance(vector2, Vector3)):
            ErrorHandler.raiseError(TypeError, f"<Vector3, Vector3> expected, got <{type(vector1).__name__},{type(vector2).__name__}>")
        return math.sqrt(Vector3.sqrDistance(vector1, vector2))
    @staticmethod
    def dot(v1, v2):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z
    @staticmethod
    def ProjectOnPlane(vector, plane_normal):
        normal = plane_normal
        projection_length = Vector3.dot(vector, normal)
        projection_vector = normal * projection_length

        return vector - projection_vector
    @staticmethod
    def cross(v1, v2):
        cross_x = v1.y * v2.z - v1.z * v2.y
        cross_y = v1.z * v2.x - v1.x * v2.z
        cross_z = v1.x * v2.y - v1.y * v2.x
        return Vector3(cross_x, cross_y, cross_z)
    @staticmethod
    def fromArray(array : Union[list, tuple]):
        if not ErrorHandler.isTypes(array, [list, tuple]):
            ErrorHandler.raiseError(TypeError, f"<list|tuple> expected, got <{type(array).__name__}>")
        if len(array) < 3:
            ErrorHandler.raiseError(IndexError, f"length <2> expected, got length <{len(array)}>")
        return Vector3(array[0], array[1], array[2])
    @staticmethod
    def fromDict(dictionary : dict):
        if not ErrorHandler.isType(dictionary, dict):
            ErrorHandler.raiseError(TypeError, f"<dict> expected, got <{type(dictionary).__name__}>")
        keys = list(dictionary.keys())
        if not ("x" in keys and "y" in keys and "z" in keys):
            ErrorHandler.raiseError(KeyError, f"keys <x,y,z> expected, got keys <{','.join(keys)}>")
        return Vector3(dictionary["x"], dictionary["y"], dictionary["z"])
    @staticmethod
    def max(*args):
        result = Vector2.negativeInfinity
        for vector in args:
            if not ErrorHandler.isType(vector, Vector2):
                continue
            result.x = max(result.x, vector.x)
            result.y = max(result.y, vector.y)
            result.z = max(result.z, vector.z)
        return result
    @staticmethod
    def min(*args):
        result = Vector3.positiveInfinity
        for vector in args:
            if not ErrorHandler.isType(vector, Vector3):
                continue
            result.x = min(result.x, vector.x)
            result.y = min(result.y, vector.y)
            result.z = min(result.z, vector.z)
        return result
    
    @staticmethod
    def LinearInterpolation(start, end, time : float):
        return start + (end - start) * time
    
    @staticmethod
    def QuadraticBezierInterpolation(p0, p1, p2, time : float):
        tempA = Vector3.linearInterpolation(p0, p1, time)
        tempB = Vector3.linearInterpolation(p1, p2, time)
        return Vector3.linearInterpolation(tempA, tempB, time)
    @staticmethod
    def CubicBezierInterpolation(p0, p1, p2, p3, time : float):
        tempA = Vector3.LinearInterpolation(p0, p1, time)
        tempB = Vector3.LinearInterpolation(p1, p2, time)
        tempC = Vector3.LinearInterpolation(p2, p3, time)
        
        return Vector3.QuadraticBezierInterpolation(tempA, tempB, tempC, time)
    @staticmethod
    def Scale(a, b):
        return Vector3(a.x * b.x, a.y * b.y, a.z * b.z)
    @staticmethod
    def Scale6(
        value, 
        posX : float, negX : float,
        posY : float, negY : float,
        posZ : float, negZ : float):
        result : Vector3 = value
        
        if(result.x > 0):
            result.x += posX
        elif(result.x < 0):
            result.x += negX
        if(result.y > 0):
            result.y += posY
        elif(result.y < 0):
            result.y += negY
        if(result.z > 0):
            result.z += posZ
        elif(result.z < 0):
            result.z += negZ
        return result
    @ClassProperty
    def one(cls):
        return Vector3(1, 1, 1)
    @ClassProperty
    def zero(cls):
        return Vector3(0, 0, 0)
    @ClassProperty
    def up(cls):
        return Vector3(0, 1, 0)
    @ClassProperty
    def down(cls):
        return Vector3(0, -1, 0)
    @ClassProperty
    def left(cls):
        return Vector3(-1, 0, 0)
    @ClassProperty
    def right(cls):
        return Vector3(1, 0, 0)
    @ClassProperty
    def forward(cls):
        return Vector3(0, 0, 1)
    @ClassProperty
    def backward(cls):
        return Vector3(0, 0, -1)
    @ClassProperty
    def positiveInfinity(cls):
        return Vector3(math.inf, math.inf, math.inf)
    @ClassProperty
    def negativeInfinity(cls):
        return Vector3(-math.inf, -math.inf, -math.inf)
    
    def __eq__(self, other):
        if ErrorHandler.isType(other, Vector3) or ErrorHandler.isType(other, Vector3Int):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return self.x == other and self.y == other and self.z == other
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __add__(self, value):
        if ErrorHandler.isType(value, Vector3) or ErrorHandler.isType(value, Vector3Int):
            return Vector3(self.x + value.x, self.y + value.y, self.z + value.z)
        return Vector3(self.x + value, self.y + value, self.z + value)
    def __sub__(self, value):
        if ErrorHandler.isType(value, Vector3) or ErrorHandler.isType(value, Vector3Int):
            return Vector3(self.x - value.x, self.y - value.y, self.z - value.z)
        return Vector3(self.x - value, self.y - value, self.z - value)    
    def __mul__(self, value):
        if ErrorHandler.isType(value, Vector3) or ErrorHandler.isType(value, Vector3Int):
            return Vector3(self.x * value.x, self.y * value.y, self.z * value.z)
        return Vector3(self.x * value, self.y * value, self.z * value)
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    def __div__(self, value):
        if ErrorHandler.isType(value, Vector3) or ErrorHandler.isType(value, Vector3Int):
            if value.x == 0.0 or value.y == 0.0 or value.z == 0.0:
                ErrorHandler.raiseError(ZeroDivisionError, "")    
            return Vector3(self.x / value.x, self.y / value.y, self.z / value.z)
        if value == 0.0:
            ErrorHandler.raiseError(ZeroDivisionError, "")
        return Vector3(self.x / value, self.y / value, self.z / value)
    def __truediv__(self, value):
        if ErrorHandler.isType(value, Vector3) or ErrorHandler.isType(value, Vector3Int):
            if value.x == 0.0 or value.y == 0.0 or value.z == 0.0:
                ErrorHandler.raiseError(ZeroDivisionError, "")    
            return Vector3(self.x / value.x, self.y / value.y, self.z / value.z)
        if value == 0.0:
            ErrorHandler.raiseError(ZeroDivisionError, "")
        return Vector3(self.x / value, self.y / value, self.z / value) 
    def __pow__(self, value):
        if ErrorHandler.isType(value, Vector3) or ErrorHandler.isType(value, Vector3Int):
            return Vector3(self.x **value.x, self.y**value.y, self.z**value.z)
        return Vector3(self.x**value, self.y**value, self.z**value)
    
    def __str__(self):
        return f"Vector3({self.x},{self.y},{self.z})"

class Vector3Int():
    def __init__(self, x : int, y : int, z : int):
        self.x : int = int(x)
        self.y : int = int(y)
        self.z : int = int(z)
    @property
    def this(self):
        return [self.x, self.y, self.z]    
    def set(self, x : int, y : int, z : int):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
    def setX(self, x : int):
        self.x = int(x)
    def setY(self, y : int):
        self.y = int(y)
    def setZ(self, z : int):
        self.z = int(z)
    @property
    def sqrMagnitude(self):
        return self.x**2 + self.y**2 + self.z**2
    @property
    def magnitude(self):
        return math.sqrt(self.sqrMagnitude)
    @property
    def normalized(self): 
        mag = self.magnitude
        return Vector3Int(self.x/mag, self.y/mag, self.z/mag)
    
    def toTuple(self):
        return (self.x, self.y, self.z)
    def toList(self):
        return [self.x, self.y, self.z]
    
    def to_degrees(self):
        return Vector3Int(math.degrees(self.x), math.degrees(self.y), math.degrees(self.z))
    def to_radians(self):
        return Vector3Int(math.radians(self.x), math.radians(self.y), math.radians(self.z))

    @staticmethod
    def dot(v1, v2):
        if not (isinstance(v1, Vector3Int) and isinstance(v2, Vector3Int)):
            ErrorHandler.raiseError(TypeError, f"<Vector3Int, Vector3Int> expected, got <{type(v1).__name__},{type(v2).__name__}>")
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z
    @staticmethod
    def cross(v1, v2):
        if not (isinstance(v1, Vector3Int) and isinstance(v2, Vector3Int)):
            ErrorHandler.raiseError(TypeError, f"<Vector3Int, Vector3Int> expected, got <{type(v1).__name__},{type(v2).__name__}>")
        x = v1.y * v2.z - v1.z * v2.y
        y = v1.z * v2.x - v1.x * v2.z
        z = v1.x * v2.y - v1.y * v2.x
        return Vector3Int(x, y, z)
    @staticmethod
    def ProjectOnPlane(vector, plane_normal):
        if not (isinstance(vector, Vector3Int) and isinstance(plane_normal, Vector3Int)):
            ErrorHandler.raiseError(TypeError, f"<Vector3Int, Vector3Int> expected, got <{type(vector).__name__},{type(plane_normal).__name__}>")
        normal = plane_normal
        projection_length = Vector3Int.dot(vector, normal)
        projection_vector = normal * projection_length

        return vector - projection_vector
    @staticmethod
    def sqrDistance(vector1, vector2):
        if not (isinstance(vector1, Vector3Int) and isinstance(vector2, Vector3Int)):
            ErrorHandler.raiseError(TypeError, f"<Vector3Int, Vector3Int> expected, got <{type(vector1).__name__},{type(vector2).__name__}>")
        return abs(vector2.x - vector1.x)**2 + abs(vector2.y - vector1.y)**2 + abs(vector2.z - vector1.z)**2
    @staticmethod
    def distance(vector1, vector2) -> float:
        if not (isinstance(vector1, Vector3Int) and isinstance(vector2, Vector3Int)):
            ErrorHandler.raiseError(TypeError, f"<Vector3Int, Vector3Int> expected, got <{type(vector1).__name__},{type(vector2).__name__}>")
        return math.sqrt(Vector3Int.sqrDistance(vector1, vector2))
    @staticmethod
    def dot(v1, v2):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z
    @staticmethod
    def ProjectOnPlane(vector, plane_normal):
        normal = plane_normal
        projection_length = Vector3Int.dot(vector, normal)
        projection_vector = normal * projection_length

        return vector - projection_vector
    @staticmethod
    def cross(v1, v2):
        cross_x = v1.y * v2.z - v1.z * v2.y
        cross_y = v1.z * v2.x - v1.x * v2.z
        cross_z = v1.x * v2.y - v1.y * v2.x
        return Vector3Int(cross_x, cross_y, cross_z)
    @staticmethod
    def fromArray(array : Union[list, tuple]):
        if not ErrorHandler.isTypes(array, [list, tuple]):
            ErrorHandler.raiseError(TypeError, f"<list|tuple> expected, got <{type(array).__name__}>")
        if len(array) < 3:
            ErrorHandler.raiseError(IndexError, f"length <2> expected, got length <{len(array)}>")
        return Vector3Int(array[0], array[1], array[2])
    @staticmethod
    def fromDict(dictionary : dict):
        if not ErrorHandler.isType(dictionary, dict):
            ErrorHandler.raiseError(TypeError, f"<dict> expected, got <{type(dictionary).__name__}>")
        keys = list(dictionary.keys())
        if not ("x" in keys and "y" in keys and "z" in keys):
            ErrorHandler.raiseError(KeyError, f"keys <x,y,z> expected, got keys <{','.join(keys)}>")
        return Vector3Int(dictionary["x"], dictionary["y"], dictionary["z"])
    @staticmethod
    def max(*args):
        result = Vector2Int.negativeInfinity
        for vector in args:
            if not ErrorHandler.isType(vector, Vector2):
                continue
            result.x = max(result.x, vector.x)
            result.y = max(result.y, vector.y)
            result.z = max(result.z, vector.z)
        return result
    @staticmethod
    def min(*args):
        result = Vector3Int.positiveInfinity
        for vector in args:
            if not ErrorHandler.isType(vector, Vector3):
                continue
            result.x = min(result.x, vector.x)
            result.y = min(result.y, vector.y)
            result.z = min(result.z, vector.z)
        return result
    
    @staticmethod
    def LinearInterpolation(start, end, time : float):
        return start + (end - start) * time
    
    @staticmethod
    def QuadraticBezierInterpolation(p0, p1, p2, time : float):
        tempA = Vector3Int.linearInterpolation(p0, p1, time)
        tempB = Vector3Int.linearInterpolation(p1, p2, time)
        return Vector3Int.linearInterpolation(tempA, tempB, time)
    @staticmethod
    def CubicBezierInterpolation(p0, p1, p2, p3, time : float):
        tempA = Vector3Int.LinearInterpolation(p0, p1, time)
        tempB = Vector3Int.LinearInterpolation(p1, p2, time)
        tempC = Vector3Int.LinearInterpolation(p2, p3, time)
        
        return Vector3Int.QuadraticBezierInterpolation(tempA, tempB, tempC, time)
    @staticmethod
    def Scale(a, b):
        return Vector3Int(a.x * b.x, a.y * b.y, a.z * b.z)
    @staticmethod
    def Scale6(
        value, 
        posX : float, negX : float,
        posY : float, negY : float,
        posZ : float, negZ : float):
        result : Vector3 = value
        
        if(result.x > 0):
            result.x += posX
        elif(result.x < 0):
            result.x += negX
        if(result.y > 0):
            result.y += posY
        elif(result.y < 0):
            result.y += negY
        if(result.z > 0):
            result.z += posZ
        elif(result.z < 0):
            result.z += negZ
        return result
    @ClassProperty
    def one(cls):
        return Vector3Int(1, 1, 1)
    @ClassProperty
    def zero(cls):
        return Vector3Int(0, 0, 0)
    @ClassProperty
    def up(cls):
        return Vector3Int(0, 1, 0)
    @ClassProperty
    def down(cls):
        return Vector3Int(0, -1, 0)
    @ClassProperty
    def left(cls):
        return Vector3Int(-1, 0, 0)
    @ClassProperty
    def right(cls):
        return Vector3Int(1, 0, 0)
    @ClassProperty
    def forward(cls):
        return Vector3Int(0, 0, 1)
    @ClassProperty
    def backward(cls):
        return Vector3Int(0, 0, -1)
    @ClassProperty
    def positiveInfinity(cls):
        return Vector3Int(math.inf, math.inf, math.inf)
    @ClassProperty
    def negativeInfinity(cls):
        return Vector3Int(-math.inf, -math.inf, -math.inf)
    
    def __eq__(self, other):
        if ErrorHandler.isType(other, Vector3Int or ErrorHandler.isType(other, Vector3)):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return self.x == other and self.y == other and self.z == other
    def __neg__(self):
        return Vector3Int(-self.x, -self.y, -self.z)

    def __add__(self, value):
        if ErrorHandler.isType(value, Vector3Int or ErrorHandler.isType(value, Vector3)):
            return Vector3Int(self.x + value.x, self.y + value.y, self.z + value.z)
        return Vector3Int(self.x + value, self.y + value, self.z + value)
    def __sub__(self, value):
        if ErrorHandler.isType(value, Vector3Int or ErrorHandler.isType(value, Vector3)):
            return Vector3Int(self.x - value.x, self.y - value.y, self.z - value.z)
        return Vector3Int(self.x - value, self.y - value, self.z - value)    
    def __mul__(self, value):
        if ErrorHandler.isType(value, Vector3Int or ErrorHandler.isType(value, Vector3)):
            return Vector3Int(self.x * value.x, self.y * value.y, self.z * value.z)
        return Vector3Int(self.x * value, self.y * value, self.z * value)
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    def __div__(self, value):
        if ErrorHandler.isType(value, Vector3Int or ErrorHandler.isType(value, Vector3)):
            if value.x == 0.0 or value.y == 0.0 or value.z == 0.0:
                ErrorHandler.raiseError(ZeroDivisionError, "")    
            return Vector3Int(self.x / value.x, self.y / value.y, self.z / value.z)
        if value == 0.0:
            ErrorHandler.raiseError(ZeroDivisionError, "")
        return Vector3Int(self.x / value, self.y / value, self.z / value)
    def __truediv__(self, value):
        if ErrorHandler.isType(value, Vector3Int or ErrorHandler.isType(value, Vector3)):
            if value.x == 0.0 or value.y == 0.0 or value.z == 0.0:
                ErrorHandler.raiseError(ZeroDivisionError, "")    
            return Vector3Int(self.x / value.x, self.y / value.y, self.z / value.z)
        if value == 0.0:
            ErrorHandler.raiseError(ZeroDivisionError, "")
        return Vector3Int(self.x / value, self.y / value, self.z / value) 
    def __pow__(self, value):
        if ErrorHandler.isType(value, Vector3Int or ErrorHandler.isType(value, Vector3)):
            return Vector3Int(self.x **value.x, self.y**value.y, self.z**value.z)
        return Vector3Int(self.x**value, self.y**value, self.z**value)
    
    def __str__(self):
        return f"Vector3Int({self.x},{self.y},{self.z})"
   
    
    
    
class Quaternion():
    def __init__(self, w : float, x : float, y : float, z : float):
        self.w : float = w
        self.x : float = x
        self.y : float = y
        self.z : float = z
    
    def to_euler(self):
        sinr_cosp = 2 * (self.w * self.x + self.y * self.z)
        cosr_cosp = 1 - 2 * (self.x * self.x + self.y * self.y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (self.w * self.y - self.z * self.x)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp)
        else:
            pitch = math.asin(sinp)
        siny_cosp = 2 * (self.w * self.z + self.x * self.y)
        cosy_cosp = 1 - 2 * (self.y * self.y + self.z * self.z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return Vector3(roll, pitch, yaw).to_degrees()

    
    @staticmethod
    def from_euler(euler : Vector3):
        euler = euler.to_radians()

        cy = math.cos(euler.z * 0.5)
        sy = math.sin(euler.z * 0.5)
        cp = math.cos(euler.y * 0.5)
        sp = math.sin(euler.y * 0.5)
        cr = math.cos(euler.x * 0.5)
        sr = math.sin(euler.x * 0.5)

        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy

        return Quaternion(w, x, y, z)
    @property
    def sqrMagnitude(self):
        return self.w**2 + self.x**2 + self.y**2 + self.z**2
    @property
    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)
    @property
    def inverse(self):
        mag_squared = self.sqrMagnitude
        if mag_squared == 0:
            ErrorHandler.raiseError(ZeroDivisionError, "")
        conjugate_q = self.conjugate()
        return Quaternion(conjugate_q.w / mag_squared, conjugate_q.x / mag_squared, conjugate_q.y / mag_squared, conjugate_q.z / mag_squared)
    def __mul__(self, other):
        if ErrorHandler.isType(other, Quaternion):
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            return Quaternion(w, x, y, z)
        else:
            q_vec = Quaternion.new(0, other.x, other.y, other.z)
            q_res = self * q_vec * self.conjugate
            return Vector3(q_res.x, q_res.y, q_res.z)
    def __str__(self):
        return f"Quaternion({self.w},{self.x},{self.y},{self.z})"


class Region2:
    def __init__(self, vector1 : Vector2, vector2 : Vector2):
        self.v1 : Vector2 = Vector2(min(vector1.x, vector2.x), min(vector1.y, vector2.y))
        self.v2 : Vector2 = Vector2(max(vector1.x, vector2.x), max(vector1.y, vector2.y))
    def isInside(self, vector : Vector2) -> bool:
        return self.v1.x <= vector.x and self.v1.y <= vector.y and self.v2.x >= vector.x and self.v2.y >= vector.y
    
    def __str__(self):
        return f"Region2({self.v1}, {self.v2})"

class Color():
    def __init__(self, r : int, g : int, b : int):
        self.r : int = int(r)
        self.b : int = int(b)
        self.g : int = int(g)
    
    
    @property
    def hex(self):
        r = Converter.dec2hex(self.r)
        g = Converter.dec2hex(self.g)
        b = Converter.dec2hex(self.b)
        return r + g + b
    
    def toTuple(self) -> tuple:
        return (self.r, self.g, self.b)
    
    
    @staticmethod
    def fromTuple(tup : tuple):
        if len(tup) < 3:
            return False
        return Color(tup[0], tup[1], tup[2])
    @ClassProperty
    def White(cls):
        return Color(255, 255, 255)
    @ClassProperty
    def Black(cls):
        return Color(0, 0, 0)
    @ClassProperty
    def Red(cls):
        return Color(255, 0, 0)
    @ClassProperty
    def Green(cls):
        return Color(0, 255, 0)
    @ClassProperty
    def Blue(cls):
        return Color(0, 0, 255)
    
    def __str__(self):
        return f"Color({self.r}, {self.g}, {self.b})"
    
    
