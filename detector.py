from human import Human
import cv2
import mediapipe as mp
from formulas import *


def draw_exercises(img, exercises):
    if not exercises:
        return

    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 0.5
    font_thickness = 1
    text_color = (0, 255, 0)
    text_color_bg = (0, 0, 255)

    max_text_width = 0
    total_text_height = 0

    for ex_name, ex_count in exercises.items():
        text = f'{ex_name}: {ex_count}'
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_w, text_h = text_size
        if (text_w > max_text_width):
            max_text_width = text_w
        total_text_height += text_h + 5

        cv2.putText(img, text, (3, total_text_height),
                    font, font_scale, text_color, font_thickness)

    cv2.rectangle(img, (2, 2), (max_text_width+5,
                  total_text_height+5), text_color_bg)


def draw_finish_text(img):
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 0.5
    font_thickness = 1
    text_color = (0, 255, 0)
    text_color_bg = (0, 0, 255)

    text = 'План выполнен. Можете закрывать окно'
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size

    cv2.rectangle(img, (2, 2), (text_w+2, text_h+7), text_color_bg, -1)
    cv2.putText(img, text, (3, text_h+5), font, font_scale,
                text_color, font_thickness)


def convert_gui_exercises_to_simple(gui_exercises):
    exercises = {}
    for ex_name, ex_count in gui_exercises.items():
        ex_count_int = int(ex_count.text())
        if ex_count_int > 0:
            exercises[ex_name.text()] = ex_count_int
    return exercises


def show(gui_exercises):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    exercises = convert_gui_exercises_to_simple(gui_exercises)
    stage = None

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()

        if not exercises:
            draw_finish_text(frame)
        draw_exercises(frame, exercises)

        RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(RGB)

        try:
            landmarks = results.pose_landmarks.landmark
            human = Human(landmarks)

            shoulder = human.keypoints['LEFT_SHOULDER']
            elbow = human.keypoints['LEFT_ELBOW']
            wrist = human.keypoints['LEFT_WRIST']

            angle = get_angle(shoulder, elbow, wrist)
            print(angle)
            if angle > 140:
                stage = 'down'
            elif angle < 50 and stage == 'down':
                stage = 'up'
                exercises['Сгибания в локтях'] -= 1
                if exercises['Сгибания в локтях'] == 0:
                    exercises.pop('Сгибания в локтях')
        except:
            pass

        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('Окно тренировки', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
