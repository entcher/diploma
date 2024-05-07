from dataclasses import dataclass
import math


@dataclass
class Point:
    x: float
    y: float
    visibility: float


def get_angle(a: Point, b: Point, c: Point) -> float:
    BA = [a.x - b.x, a.y - b.y]
    BC = [c.x - b.x, c.y - b.y]

    dot_product = BA[0]*BC[0] + BA[1]*BC[1]

    length_AB = math.sqrt(BA[0]**2 + BA[1]**2)
    length_AC = math.sqrt(BC[0]**2 + BC[1]**2)

    cos_angle = dot_product / (length_AB * length_AC)

    angle_rad = math.acos(cos_angle)
    angle_deg = math.degrees(angle_rad)

    return angle_deg
