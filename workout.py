from point import Point
from formulas import *

from enum import Enum
import mediapipe as mp


class Phase(Enum):
    Start = 1
    Doing = 2
    Done = 3


class Workout:
    def __init__(self, landmarks):
        self.skeleton = {}
        for mark, data_point in zip(mp.solutions.pose.PoseLandmark, landmarks):
            self.skeleton[mark.name] = Point(
                data_point.x, data_point.y, data_point.visibility)

    def do_exercise(self, exercise_name, phase):
        exercises = {
            'Сгибания в локтях': self.curl,
            'Наклоны вперед': self.bend_over,
            'Наклоны в стороны': self.bend_right,
            'Приседания': self.squat
        }

        exercise_func = exercises.get(exercise_name)
        if exercise_func:
            return exercise_func(phase)
        else:
            return None

    def curl(self, phase: Phase) -> Phase:
        shoulder = self.skeleton['LEFT_SHOULDER']
        elbow = self.skeleton['LEFT_ELBOW']
        wrist = self.skeleton['LEFT_WRIST']
        angle = get_angle(shoulder, elbow, wrist)

        if angle > 140:
            return Phase.Doing
        if angle < 50 and phase == Phase.Doing:
            return Phase.Done
        else:
            return phase

    def bend_over(self, phase: Phase) -> Phase:
        nose = self.skeleton['NOSE']
        hip = self.skeleton['LEFT_HIP']
        knee = self.skeleton['LEFT_KNEE']
        angle = get_angle(nose, hip, knee)

        if angle > 150:
            return Phase.Doing
        elif angle < 100 and phase == Phase.Doing:
            return Phase.Done
        else:
            return phase

    def bend_right(self, phase: Phase) -> Phase:
        shoulder = self.skeleton['RIGHT_SHOULDER']
        hip = self.skeleton['RIGHT_HIP']
        knee = self.skeleton['RIGHT_KNEE']
        angle = get_angle(shoulder, hip, knee)

        if angle > 170:
            return Phase.Doing
        elif angle < 160 and phase == Phase.Doing:
            return Phase.Done
        else:
            return phase

    def squat(self, phase: Phase) -> Phase:
        pass
