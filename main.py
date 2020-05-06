import cv2
import numpy as np
import dlib
import time

#Face recognition and prediction variables
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#Timer variables
time_passed = 0
cam_initialized = False
cam_uptime = 2 #in seconds

#Frame variables
n_frames = 5
frame_counter = 0

while True:
    time_start = time.time()
    print(time_passed)
    if time_passed > cam_uptime:
        break
    
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    

    faces = detector(gray)

    for face in faces:
        '''
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 255, 0), 3)
        '''
        
        landmarks = predictor(gray, face)
        for i in range(0, 68):       
            cv2.circle(frame, (landmarks.part(i).x,landmarks.part(i).y), 4, (255, 0, 0), -1)

    cv2.imshow("Frame", frame)
    if cam_initialized == False:
        cam_initialized = True
        time_start = time.time()
    

    key = cv2.waitKey(1)
    if key == 27:
        break
    time_end = time.time()
    time_passed += time_end - time_start
    frame_counter+=1

print("Number of frames: " + str(frame_counter))