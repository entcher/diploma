from point import Point
from formulas import *

import mediapipe as mp


class Human:
    def __init__(self, landmarks):
        self.keypoints = {}
        for mark, data_point in zip(mp.solutions.pose.PoseLandmark, landmarks):
            self.keypoints[mark.name] = Point(
                data_point.x, data_point.y, data_point.visibility)

    def estimate_pose(self):
        return self.person_stands()
        return 'Неопределено'

    def person_stands(self) -> str:
        angle1 = -1
        left_hip = self.keypoints["LEFT_HIP"]
        left_knee = self.keypoints["LEFT_KNEE"]
        left_ankle = self.keypoints["LEFT_ANKLE"]
        if angle_exists(left_hip, left_knee, left_ankle):
            angle1 = get_angle(left_hip, left_knee, left_ankle)
            print(angle1)

        angle2 = -1
        right_hip = self.keypoints["RIGHT_HIP"]
        right_knee = self.keypoints["RIGHT_KNEE"]
        right_ankle = self.keypoints["RIGHT_ANKLE"]
        if angle_exists(right_hip, right_knee, right_ankle):
            angle2 = get_angle(right_hip, right_knee, right_ankle)
            print(angle2)

        if angle1 > 170 and angle2 > 170:
            return 'Стоит'
        else:
            return 'Сидит'
