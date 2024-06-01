from .point import *
from enum import Enum
import mediapipe as mp


class Phase(Enum):
    Start = 1
    Doing = 2
    Done = 3


exercises_names = [
    'Наклоны шеи влево',
    'Наклоны шеи вправо',
    'Подъемы рук над головой',
    'Разведение руками в стороны',
    'Сгибания в локтях (левая рука)',
    'Сгибания в локтях (правая рука)',
    'Разгибания из-за головы (левая рука)',
    'Разгибания из-за головы (правая рука)',
    'Наклоны корпуса вперед',
    'Наклоны корпуса влево',
    'Наклоны корпуса вправо',
    'Выпады левой ногой',
    'Выпады правой ногой',
    'Приседания',
]


class Workout:
    def __init__(self, landmarks):
        self.skeleton = {}
        for mark, data_point in zip(mp.solutions.pose.PoseLandmark, landmarks):
            self.skeleton[mark.name] = Point(data_point.x, data_point.y, data_point.visibility)            

    def do_exercise(self, exercise_name: str, phase: Phase):
        exercises_funcs = [
            self.degree_exercise(phase, 'NOSE', 'LEFT_EAR', 'LEFT_SHOULDER', 110, 80),
            self.degree_exercise(phase, 'NOSE', 'RIGHT_EAR', 'RIGHT_SHOULDER', 110, 80),
            self.raise_hands_forward(phase),
            self.raise_hands_sideways(phase),
            self.degree_exercise(phase, 'LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST', 140, 50),
            self.degree_exercise(phase, 'RIGHT_SHOULDER', 'RIGHT_ELBOW', 'RIGHT_WRIST', 140, 50),
            self.degree_exercise(phase, 'LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST', 50, 140),
            self.degree_exercise(phase, 'RIGHT_SHOULDER', 'RIGHT_ELBOW', 'RIGHT_WRIST', 50, 140),
            self.degree_exercise(phase, 'NOSE', 'LEFT_HIP', 'LEFT_KNEE', 150, 100),
            self.degree_exercise(phase, 'LEFT_SHOULDER', 'LEFT_HIP', 'LEFT_KNEE', 170, 160),
            self.degree_exercise(phase, 'RIGHT_SHOULDER', 'RIGHT_HIP', 'RIGHT_KNEE', 170, 160),
            self.degree_exercise(phase, 'LEFT_HIP', 'LEFT_KNEE', 'LEFT_ANKLE', 170, 90),
            self.degree_exercise(phase, 'RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_ANKLE', 170, 90),
            self.squat(phase),
        ]

        exercises_funcs = dict(zip(exercises_names, exercises_funcs))
        exercise_func = exercises_funcs.get(exercise_name)
        if exercise_func:
            return exercise_func
        else:
            return None

    def degree_exercise(
        self,
        phase: Phase,
        landmark1: str,
        landmark2: str,
        landmark3: str,
        doing_degree: float,
        done_degree: float,
    ):
        point1 = self.skeleton[landmark1]
        point2 = self.skeleton[landmark2]
        point3 = self.skeleton[landmark3]

        if self.not_fits([point1, point2, point3]):
            raise Exception()

        angle = get_angle(point1, point2, point3)
        # print(angle)

        if angle > doing_degree:
            return Phase.Doing
        elif angle < done_degree and phase == Phase.Doing:
            return Phase.Done
        else:
            return phase

    def squat(self, phase: Phase) -> Phase:
        left_hip = self.skeleton['LEFT_HIP']
        left_knee = self.skeleton['LEFT_KNEE']
        left_ankle = self.skeleton['LEFT_ANKLE']

        right_hip = self.skeleton['RIGHT_HIP']
        right_knee = self.skeleton['RIGHT_KNEE']
        right_ankle = self.skeleton['RIGHT_ANKLE']

        left_angle = get_angle(left_hip, left_knee, left_ankle)
        right_angle = get_angle(right_hip, right_knee, right_ankle)

        if left_angle > 170 and right_angle > 170:
            return Phase.Doing
        elif left_angle < 80 and right_angle < 80 and phase == Phase.Doing:
            return Phase.Done
        else:
            return phase

    def raise_hands_forward(self, phase: Phase) -> Phase:
        left_wrist = self.skeleton['LEFT_WRIST']
        right_wrist = self.skeleton['RIGHT_WRIST']
        nose = self.skeleton['NOSE']

        if left_wrist.y > nose.y and right_wrist.y > nose.y:
            return Phase.Doing
        elif left_wrist.y < nose.y and right_wrist.y < nose.y and phase == Phase.Doing:
            return Phase.Done
        else:
            return phase

    def raise_hands_sideways(self, phase: Phase) -> Phase:
        left_wrist = self.skeleton['LEFT_WRIST']
        left_shoulder = self.skeleton['LEFT_SHOULDER']
        right_wrist = self.skeleton['RIGHT_WRIST']
        right_shoulder = self.skeleton['RIGHT_SHOULDER']

        if left_wrist.x > left_shoulder.x and right_wrist.x < right_shoulder.x:
            return Phase.Doing
        elif (
            left_wrist.x < left_shoulder.x
            and right_wrist.x > right_shoulder.x
            and phase == Phase.Doing
        ):
            return Phase.Done
        else:
            return phase

    def not_fits(self, points: list[Point]) -> bool:
        if any(point.visibility < 0.8 for point in points):
            return True
        return False
