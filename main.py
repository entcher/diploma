from human import Human

import cv2
import mediapipe as mp


def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    img = cv2.imread('images/img2.jpg')
    RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(RGB)

    human = Human(results.pose_landmarks.landmark)
    pose_name = human.estimate_pose()
    print(f'Положение: {pose_name}')

    mp_drawing.draw_landmarks(
        img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow('Output', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
