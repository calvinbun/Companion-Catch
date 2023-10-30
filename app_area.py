import sys
import cv2
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QFont

class PoseDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.draw_area_button = QPushButton("Draw Area", self)
        self.initUI()
        self.initMediapipe()
        self.landmarks_sequence = []
        self.alert_message = ""
        self.alert_triggered = False
        self.drawing = False
        self.roi = None
        self.start_point = None
        self.end_point = None
        self.draw_mode = False

    def initUI(self):
        self.setWindowTitle("Pose Detection App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label = QLabel(self)
        self.label.mousePressEvent = self.on_mouse_press
        self.label.mouseMoveEvent = self.on_mouse_move
        self.label.mouseReleaseEvent = self.on_mouse_release
        self.layout.addWidget(self.label)

        self.layout.addWidget(self.draw_area_button)
        self.draw_area_button.clicked.connect(self.toggle_draw_mode)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_capture)
        self.layout.addWidget(self.start_button)

        self.central_widget.setLayout(self.layout)

        self.cap = cv2.VideoCapture("old_fall.mp4")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.paintEvent)
        self.is_capturing = False
        self.frame_counter = 0

    def initMediapipe(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

        # Set a higher confidence threshold (e.g., 0.7)
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

    def start_capture(self):
        if not self.is_capturing:
            self.is_capturing = True
            self.start_button.setText("Stop")
            self.timer.start(20)
        else:
            self.is_capturing = False
            self.start_button.setText("Start")
            self.timer.stop()

    def toggle_draw_mode(self):
        if not self.is_capturing:
            if self.draw_mode:
                self.draw_area_button.setText("Draw Area")
                self.draw_mode = False
            else:
                self.draw_area_button.setText("Finish Drawing")
                self.draw_mode = True
                self.roi = None
                self.label.clear()

    def on_mouse_press(self, event):
        if not self.alert_triggered and self.draw_mode:
            self.drawing = True
            self.start_point = event.pos()
            self.end_point = self.start_point

    def on_mouse_move(self, event):
        if self.drawing and self.draw_mode:
            self.end_point = event.pos()
            self.label.update()

    def on_mouse_release(self, event):
        if self.drawing and self.draw_mode:
            self.end_point = event.pos()
            self.drawing = False
            self.roi = [self.start_point, self.end_point]
            self.label.update()

    def paintEvent(self, event):
        if self.is_capturing:
            ret, frame = self.cap.read()
            if not ret:
                return
            frame = cv2.resize(frame, (640, 360))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame)
            if results.pose_landmarks:
                self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
                self.frame_counter += 1

                # Collect pose_landmarks for every 10 frames
                if self.frame_counter == 10:
                    self.landmarks_sequence.append(results.pose_landmarks)

                    # Check if the Nose keypoint (index 0) is in the bottom half of the image
                    last_landmarks = self.landmarks_sequence[-1]
                    nose_landmark = last_landmarks.landmark[0]  # Index 0 is the Nose landmark
                    left_knee = last_landmarks.landmark[25]
                    right_knee = last_landmarks.landmark[26]
                    left_shoulder = last_landmarks.landmark[11]
                    right_shoulder = last_landmarks.landmark[12]

                    # Check if the "FALLING" condition is met
                    if (nose_landmark.y > left_shoulder.y) or (nose_landmark.y > right_shoulder.y) or (nose_landmark.y > right_knee.y) or (nose_landmark.y > left_knee.y):
                        self.alert_triggered = True
                    if (nose_landmark.x < left_shoulder.x) and (nose_landmark.x < right_shoulder.x) and (nose_landmark.x < right_knee.x) and (nose_landmark.x > left_knee.x):
                        self.alert_triggered = True

                    # Clear the alert if the condition is not met
                    if not self.alert_triggered:
                        self.alert_message = ""

                    self.frame_counter = 0

            h, w, c = frame.shape
            qImg = QImage(frame.data, w, h, w * c, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)

            # Draw the area if it is defined
            if self.roi:
                painter = QPainter(pixmap)
                pen = QPen(QColor(0, 0, 255))
                pen.setWidth(2)
                painter.setPen(pen)
                painter.drawRect(self.start_point.x(), self.start_point.y(), self.end_point.x() - self.start_point.x(), self.end_point.y() - self.start_point.y())

            self.label.setPixmap(pixmap)


    def closeEvent(self, event):
        self.cap.release()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = PoseDetectionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
