from human import Human
import cv2
import mediapipe as mp


def put_text(image, text):
    font = cv2.FONT_HERSHEY_COMPLEX
    org = (0, 15)
    fontScale = 0.5
    color = (0, 0, 255)
    thickness = 1

    image = cv2.putText(image, text, org, font,
                        fontScale, color, thickness, cv2.LINE_AA)


def show(file_path):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    # add filepath instead of hardcode
    img = cv2.imread('images/bending.jpg')
    RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(RGB)

    human = Human(results.pose_landmarks.landmark)
    pose_name = human.estimate_pose()
    print(f'Положение: {pose_name}')

    mp_drawing.draw_landmarks(
        img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    put_text(img, pose_name)
    cv2.imshow('Результат', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
