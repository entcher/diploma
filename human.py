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
        if self.person_bends():
            return 'Наклоняется'
        elif self.person_lies():
            return 'Лежит'
        elif self.person_sits():
            return 'Сидит'
        elif self.person_runs():
            return 'Бежит'
        elif self.person_walks():
            return 'Идет'
        elif self.person_stands():
            return 'Стоит'
        return 'Неизвестно'

    def person_stands(self) -> bool:
        left_leg_angle = -1
        left_hip = self.keypoints["LEFT_HIP"]
        left_knee = self.keypoints["LEFT_KNEE"]
        left_ankle = self.keypoints["LEFT_ANKLE"]
        if angle_exists(left_hip, left_knee, left_ankle):
            left_leg_angle = get_angle(left_hip, left_knee, left_ankle)
            print(left_leg_angle)

        right_leg_angle = -1
        right_hip = self.keypoints["RIGHT_HIP"]
        right_knee = self.keypoints["RIGHT_KNEE"]
        right_ankle = self.keypoints["RIGHT_ANKLE"]
        if angle_exists(right_hip, right_knee, right_ankle):
            right_leg_angle = get_angle(right_hip, right_knee, right_ankle)
            print(right_leg_angle)

        return True if left_leg_angle > 170 and right_leg_angle > 170 else False

    def person_sits(self) -> bool:
        left_leg_angle = -1
        left_hip = self.keypoints["LEFT_HIP"]
        left_knee = self.keypoints["LEFT_KNEE"]
        left_ankle = self.keypoints["LEFT_ANKLE"]
        if angle_exists(left_hip, left_knee, left_ankle):
            left_leg_angle = get_angle(left_hip, left_knee, left_ankle)
            print(left_leg_angle)

        right_leg_angle = -1
        right_hip = self.keypoints["RIGHT_HIP"]
        right_knee = self.keypoints["RIGHT_KNEE"]
        right_ankle = self.keypoints["RIGHT_ANKLE"]
        if angle_exists(right_hip, right_knee, right_ankle):
            right_leg_angle = get_angle(right_hip, right_knee, right_ankle)
            print(right_leg_angle)

        return True if left_leg_angle < 170 and right_leg_angle < 170 else False

    def person_lies(self) -> bool:
        left_shoulder = self.keypoints["LEFT_SHOULDER"]
        left_hip = self.keypoints["LEFT_HIP"]
        left_ankle = self.keypoints["LEFT_ANKLE"]
        if left_shoulder.x < left_hip.x < left_ankle.x or left_ankle.x < left_hip.x < left_shoulder.x:
            return True
        return False

    def person_walks(self) -> bool:
        left_heel = self.keypoints["LEFT_HEEL"]
        right_heel = self.keypoints["RIGHT_HEEL"]
        left_hip = self.keypoints["RIGHT_HIP"]
        if angle_exists(left_heel, right_heel, left_hip):
            angle = get_angle(left_heel, left_hip, right_heel)
            print(angle)
            if angle < 70:
                return True
        return False

    def person_runs(self) -> bool:
        left_heel = self.keypoints["LEFT_HEEL"]
        right_heel = self.keypoints["RIGHT_HEEL"]
        left_hip = self.keypoints["RIGHT_HIP"]
        if angle_exists(left_heel, right_heel, left_hip):
            angle = get_angle(left_heel, left_hip, right_heel)
            print(angle)
            if angle >= 70:
                return True
        return False

    def person_bends(self) -> bool:
        right_elbow = self.keypoints["RIGHT_ELBOW"]
        right_hip = self.keypoints["RIGHT_HIP"]
        right_heel = self.keypoints["RIGHT_HEEL"]
        if right_heel.y > right_elbow.y > right_hip.y:
            return True
        return False
