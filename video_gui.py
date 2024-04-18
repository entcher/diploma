from workout import Workout, Phase
from ui_writer import *
from stats import write_csv
from utility import find_dicts_difference

import cv2
import mediapipe as mp
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class VideoWindow(QWidget):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    def __init__(self, exercises):
        super().__init__()

        self.setWindowTitle('Видео')
        self.setGeometry(100, 100, 640, 480)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.video_label = QLabel()
        self.layout.addWidget(self.video_label)

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.display_frame(exercises))
        self.timer.start(30)

        self.phase = Phase.Start
        self.start_exercises = exercises.copy()
        self.current_exercise = next(iter(exercises))

    def display_frame(self, exercises):
        ret, frame = self.cap.read()
        if not ret:
            return

        # add method to check if person fits the screen
        if not exercises:
            write_finish_text(frame)
            self.cap.release()
            done_exercises = find_dicts_difference(
                self.start_exercises, exercises)
            write_csv(done_exercises)

        write_exercises(frame, exercises)
        RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = VideoWindow.pose.process(RGB)

        try:
            landmarks = results.pose_landmarks.landmark
            workout = Workout(landmarks)

            self.phase = workout.do_exercise(self.current_exercise, self.phase)

            if self.phase == None:
                return
            if self.phase == Phase.Done:
                self.phase = Phase.Start
                exercises[self.current_exercise] -= 1
                if exercises[self.current_exercise] == 0:
                    exercises.pop(self.current_exercise)
                    self.current_exercise = next(iter(exercises))
        except:
            pass

        RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = VideoWindow.pose.process(RGB)

        VideoWindow.mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, VideoWindow.mp_pose.POSE_CONNECTIONS)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(
            frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.video_label.setPixmap(pixmap)
