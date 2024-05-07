from models.workout import Workout, Phase
from .ui_writer import *
from stats import write_csv
from utility import find_dicts_difference

import cv2
import mediapipe as mp
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class VideoWindow(QWidget):
    close_signal = pyqtSignal()

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def __init__(self, exercises, current_user):
        super().__init__()

        self.current_user = current_user

        self.setWindowTitle('Видео')
        self.setGeometry(100, 100, 640, 480)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.video_label = QLabel()
        self.layout.addWidget(self.video_label)

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_frame)
        self.timer.start(30)

        self.phase = Phase.Start
        self.start_exercises = exercises.copy()
        self.remained_exercises = exercises
        self.current_exercise = next(iter(exercises))

    def display_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        if not self.remained_exercises:
            write_line(
                frame,
                'План выполнен. Можете закрывать окно',
                text_color=(0, 255, 0),
                background_color=(0, 0, 255),
            )
            self.cap.release()

        RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = VideoWindow.pose.process(RGB)

        try:
            landmarks = results.pose_landmarks.landmark
            workout = Workout(landmarks)

            self.phase = workout.do_exercise(self.current_exercise, self.phase)
            write_exercises(frame, self.remained_exercises)

            if self.phase == None:
                return
            if self.phase == Phase.Done:
                self.phase = Phase.Start
                self.remained_exercises[self.current_exercise] -= 1
                if self.remained_exercises[self.current_exercise] == 0:
                    self.remained_exercises.pop(self.current_exercise)
                    self.current_exercise = next(iter(self.remained_exercises))
        except:
            write_line(
                frame,
                'Отойдите от камеры подальше',
                text_color=(0, 0, 0),
                background_color=(255, 255, 0),
            )

        VideoWindow.mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, VideoWindow.mp_pose.POSE_CONNECTIONS
        )
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.video_label.setPixmap(pixmap)

    def closeEvent(self, _):
        self.cap.release()
        done_exercises = find_dicts_difference(self.start_exercises, self.remained_exercises)
        if done_exercises:
            write_csv(done_exercises, self.current_user)
        self.close_signal.emit()
