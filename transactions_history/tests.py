from django.test import TestCase
import cv2
import numpy as np

# Create your tests here.


cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break