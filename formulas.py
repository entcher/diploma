from point import Point
import math


def get_angle(a: Point, b: Point, c: Point) -> float:
    deg = math.degrees(
        math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x))
    return deg + 360 if deg < 0 else deg


def angle_exists(a: Point, b: Point, c: Point) -> bool:
    if a.visibility < 0.9 or b.visibility < 0.9 or c.visibility < 0.9:
        return False
    return True
