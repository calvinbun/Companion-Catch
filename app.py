import sys
import cv2
import mediapipe as mp
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QFont
from PyQt5.QtWidgets import QMessageBox




class PoseDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initMediapipe()
        self.landmarks_sequence = []
        self.alert_message = ""
        self.alert_triggered = False
        self.drawing = False
        self.rect_start = None
        self.rect_end = None
        self.rectangles = []

        ret, frame = self.cap.read()
        frame = cv2.resize(frame, (640, 360))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = frame.shape
        qImg = QImage(frame.data, w, h, w * c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.label.setPixmap(pixmap)

    def initUI(self):
        self.setWindowTitle("Pose Detection App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_capture)
        self.layout.addWidget(self.start_button)

        self.draw_area_button = QPushButton("Draw Area", self)
        self.draw_area_button.clicked.connect(self.start_drawing_area)  # Connect the button to drawing mode
        self.layout.addWidget(self.draw_area_button)

        self.delete_area_button = QPushButton("Delete Area", self)
        self.delete_area_button.clicked.connect(self.delete_areas)
        self.layout.addWidget(self.delete_area_button)

        self.browse_video_button = QPushButton("Browse Video", self)
        self.browse_video_button.clicked.connect(self.browse_video)
        self.layout.addWidget(self.browse_video_button)

        self.central_widget.setLayout(self.layout)

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.is_capturing = False
        self.frame_counter = 0

    def initMediapipe(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.pose = self.mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6)


    def browse_video(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv);;All Files (*)", options=options)
        if file_path:
            self.video_path = file_path
            self.cap = cv2.VideoCapture(self.video_path)

    def start_capture(self):
        if not self.is_capturing:
            self.is_capturing = True
            self.start_button.setText("Stop")
            self.timer.start(20)
        else:
            self.is_capturing = False
            self.start_button.setText("Start")
            self.timer.stop()
    def delete_areas(self):
        self.rectangles = []  # Clear the stored rectangles

    def start_drawing_area(self):
        self.draw_area_button.setText("Drawing Area")
        self.setCursor(Qt.CrossCursor)
        self.drawing = True

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Companion Catch")
        msg.setText("ALERT! FALL DETECTED!")

        x = msg.exec_()

    def mousePressEvent(self, event):
        if self.drawing:
            if not self.rect_start:
                self.rect_start = event.pos()
            else:
                self.rect_end = event.pos()
                self.drawing = False
                self.setCursor(Qt.ArrowCursor)
                self.rectangles.append((self.rect_start, self.rect_end))
                self.update_frame()
                self.rect_start = None
                self.rect_end = None

    # def mouseReleaseEvent(self, event):
    #     if self.drawing:
    #         self.rect_end = event.pos()
    #         self.drawing = False
    #         self.setCursor(Qt.ArrowCursor)
    #         self.rectangles.append((self.rect_start, self.rect_end))
    #         self.update_frame()


    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = cv2.resize(frame, (640, 360))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame)
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            self.frame_counter += 1

            # Collect pose_landmarks for every 20 frames
            if self.frame_counter == 20:
                self.landmarks_sequence.append(results.pose_landmarks)

         



                # Chelandmarks_insidekeypoint (index 0) is in the bottom half of the image
                last_landmarks = self.landmarks_sequence[-1]
                nose_landmark = last_landmarks.landmark[0]  # Index 0 is the Nose landmark
                left_knee = last_landmarks.landmark[25]
                right_knee = last_landmarks.landmark[26]
                left_shoulder = last_landmarks.landmark[11]
                right_shoulder = last_landmarks.landmark[12]
                left_hip = last_landmarks.landmark[23]
                right_hip = last_landmarks.landmark[24]
                left_ankle = last_landmarks.landmark[27]
                right_ankle = last_landmarks.landmark[28]
                left_shoulder = last_landmarks.landmark[11]
                right_shoulder = last_landmarks.landmark[12]
                if (self.rectangles != None):
                  print(f"IGNORE AREA: {self.rect_start} {self.rect_end}")
                # Check if the "FALLING" condition is met
                if (nose_landmark.y > right_knee.y) or (nose_landmark.y > left_knee.y):
                    self.alert_triggered = True
                if (nose_landmark.x < left_shoulder.x) and (nose_landmark.x < right_shoulder.x) and (nose_landmark.x < right_knee.x) and (nose_landmark.x > left_knee.x):
                    self.alert_triggered = True
                # Clear the alert if the condition is not met

                # Assuming left_hip, left_knee, left_ankle, right_hip, right_knee, and right_ankle are represented as landmarks





                if not self.alert_triggered:
                    self.alert_message = ""
                else:
                    self.alert_message = "FALLING"

                if self.rectangles:
                    for rect_start, rect_end in self.rectangles:
                        landmarks_inside = 0

                        for landmark in results.pose_landmarks.landmark:
                            landmark_x = int(landmark.x * frame.shape[1])
                            landmark_y = int(landmark.y * frame.shape[0])

                            if rect_start.x() < landmark_x < rect_end.x() and rect_start.y() < landmark_y < rect_end.y():
                                landmarks_inside += 1

                        print(f"Landmarks inside the rectangle: {landmarks_inside}")
                    if landmarks_inside > 15:
                        self.alert_message = "IGNORE"

                # Create QPoint objects from the landmarks
                left_hip_point = QPoint(int(left_hip.x * frame.shape[1]), int(left_hip.y * frame.shape[0]))
                left_knee_point = QPoint(int(left_knee.x * frame.shape[1]), int(left_knee.y * frame.shape[0]))
                left_ankle_point = QPoint(int(left_ankle.x * frame.shape[1]), int(left_ankle.y * frame.shape[0]))
                right_hip_point = QPoint(int(right_hip.x * frame.shape[1]), int(right_hip.y * frame.shape[0]))
                right_knee_point = QPoint(int(right_knee.x * frame.shape[1]), int(right_knee.y * frame.shape[0]))
                right_ankle_point = QPoint(int(right_ankle.x * frame.shape[1]), int(right_ankle.y * frame.shape[0]))

                # Calculate vectors for the left side
                left_vector1 = left_hip_point - left_knee_point
                left_vector2 = left_ankle_point - left_knee_point

                # Calculate vectors for the right side
                right_vector1 = right_hip_point - right_knee_point
                right_vector2 = right_ankle_point - right_knee_point

                # Calculate the angles in radians for both sides
                left_cosine_theta = (left_vector1.x() * left_vector2.x() + left_vector1.y() * left_vector2.y()) / \
                                    (math.sqrt(left_vector1.x() ** 2 + left_vector1.y() ** 2) * 
                                    math.sqrt(left_vector2.x() ** 2 + left_vector2.y() ** 2))

                right_cosine_theta = (right_vector1.x() * right_vector2.x() + right_vector1.y() * right_vector2.y()) / \
                                    (math.sqrt(right_vector1.x() ** 2 + right_vector1.y() ** 2) * 
                                    math.sqrt(right_vector2.x() ** 2 + right_vector2.y() ** 2))

                left_angle_rad = math.acos(left_cosine_theta)
                right_angle_rad = math.acos(right_cosine_theta)

                # Convert the angles to degrees
                left_angle_deg = math.degrees(left_angle_rad)
                right_angle_deg = math.degrees(right_angle_rad)
                if (left_angle_deg + right_angle_deg) < 170:
                    print("SITTING")
                    self.alert_message = "SITTING"


                self.frame_counter = 0
        
        h, w, c = frame.shape
        qImg = QImage(frame.data, w, h, w * c, QImage.Format_RGB888)

        # Create a QPixmap for drawing rectangles
        pixmap = QPixmap.fromImage(qImg)
        painter = QPainter(pixmap)

        # Draw stored rectangles
        for start, end in self.rectangles:
            pen = QPen(QColor(255, 0, 0))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawRect(start.x(), start.y(), end.x() - start.x(), end.y() - start.y())

        # Release the QPainter
        painter.end()

        # Set the QPixmap to the label
        self.label.setPixmap(pixmap)

        if self.alert_triggered:
            self.draw_alert_message(pixmap)
            if len(self.landmarks_sequence) > 0:
                        # Get the bounding box coordinates
                        landmarks = self.landmarks_sequence[-1]
                        min_x, max_x = float('inf'), 0
                        min_y, max_y = float('inf'), 0

                        for landmark in landmarks.landmark:
                            x, y = landmark.x, landmark.y
                            min_x = min(min_x, x)
                            max_x = max(max_x, x)
                            min_y = min(min_y, y)
                            max_y = max(max_y, y)

                        min_x = int(min_x * frame.shape[1])
                        max_x = int(max_x * frame.shape[1])
                        min_y = int(min_y * frame.shape[0])
                        max_y = int(max_y * frame.shape[0])
                        cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)

            # Draw a red bounding box around the detected skeleton
        self.label.setPixmap(pixmap)

    popup_time = 3
    def draw_alert_message(self, pixmap):
        painter = QPainter(pixmap)
        pen = QPen()
        pen.setColor(QColor(255, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)

        font = QFont()
        font.setPointSize(50)
        painter.setFont(font)
        rect = self.label.rect()
        rect.setTop(100)  # Adjust the position of the alert message
        painter.drawText(rect, Qt.AlignCenter, self.alert_message)
        if self.alert_message == "FALLING":
          while popup_time > 0:
              self.show_popup()
              popup_time -= 1

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
