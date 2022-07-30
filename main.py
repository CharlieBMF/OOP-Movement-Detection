import cv2
from datetime import datetime
import pandas as pd


class MovementDetection:
    """A class with necessary functions to detect objects on frame"""

    def __init__(self):
        self.first_frame = self.get_base_frame()
        self.detection_status_list = [None, None]
        self.object_detect_times = []
        self.day = datetime.now().strftime("%d")
        self.df = pd.DataFrame(columns=["Start", "End"])
        self.video = cv2.VideoCapture(0)
        self.movement_detection = False
        self.frame = None
        self.gray = None
        self.delta_frame = None
        self.thresh_frame = None

    def reset_detection(self):
        """Reset movement detection status"""
        self.movement_detection = False

    def generate_frames(self):
        """Generate single frame as gray, delta and thresh"""
        check, self.frame = self.video.read()
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.gray = cv2.GaussianBlur(self.gray, (21, 21), 0)
        self.delta_frame = cv2.absdiff(self.first_frame, self.gray)
        self.thresh_frame = cv2.threshold(self.delta_frame, 75, 255, cv2.THRESH_BINARY)[1]
        self.thresh_frame = cv2.dilate(self.thresh_frame, None, iterations=2)

    def check_object_movement(self):
        """Checking new object apperance by comparing with last movement status"""
        if self.detection_status_list[-1] is True and self.detection_status_list[-2] is False:
            self.object_detect_times.append(datetime.now())
        elif self.detection_status_list[-1] is False and self.detection_status_list[-2] is True:
            self.object_detect_times.append(datetime.now())

    def draw_object_movement(self):
        """Drawing rectangle on color frame which shows area where new object has been detected"""
        (cnts, _) = cv2.findContours(self.thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in cnts:
            if cv2.contourArea(contour) < 10000:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            self.movement_detection = True

    def record_detection_status(self):
        """Appending detection status to history list"""
        self.detection_status_list.append(self.movement_detection)

    def check_day(self):
        """Checks if there is a new day to generate new .csv file"""
        if datetime.now().strftime("%d") > self.day:
            self.save_csv()

    def clear_detection_status_list(self):
        """Clearing detection status history each 100 records"""
        if len(self.detection_status_list) > 100:
            self.detection_status_list = [self.detection_status_list[-2], self.detection_status_list[-1]]

    def show_frames(self):
        """Shows frames (Color, Gray, Delta and Thresh)"""
        cv2.imshow('Color Frame', self.frame)
        cv2.imshow('Gray', self.gray)
        cv2.imshow('Delta Frame', self.delta_frame)
        cv2.imshow('Threshold Frame', self.thresh_frame)

    def save_csv(self):
        """Saving detection times as Y-m-d-H-M-S.csv"""
        if len(self.object_detect_times) > 0:
            if self.movement_detection:
                self.object_detect_times.append(datetime.now())
            for i in range(0, len(self.object_detect_times), 2):
                self.df = self.df.append({'Start': self.object_detect_times[i],
                                          "End": self.object_detect_times[i + 1]},
                                         ignore_index=True)
            name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.csv'
            self.df.to_csv(name)
            self.df = pd.DataFrame(columns=["Start", "End"])
            self.object_detect_times = []
            self.day = datetime.now().strftime("%M")

    @staticmethod
    def check_wait_key():
        """Checking if this is finish for detecting"""
        key = cv2.waitKey(1)
        if key == ord('q'):
            return 'break'

    @staticmethod
    def get_base_frame():
        """Generate first frame which is base for delta frames and detection method"""
        video = cv2.VideoCapture(0)
        check, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        video.release()
        return gray


garden_guard = MovementDetection()
while True:
    garden_guard.reset_detection()
    garden_guard.generate_frames()
    garden_guard.check_object_movement()
    garden_guard.draw_object_movement()
    garden_guard.record_detection_status()
    garden_guard.check_day()
    garden_guard.clear_detection_status_list()
    garden_guard.show_frames()
    finish = garden_guard.check_wait_key()

    if finish == 'break':
        garden_guard.save_csv()
        break
