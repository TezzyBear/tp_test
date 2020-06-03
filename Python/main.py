import cv2
import numpy as np
import dlib
import time
import pandas as pd #pandas 1.0.3
import os
import xlsxwriter #pip install XlsxWriter 1.2.8
import datetime #pip install dateTime 4.3

#Face recognition and prediction variables
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#Timer variables
time_passed = 0
cam_initialized = False
cam_uptime = 5 #in seconds

#Frame variables
n_frames_segundos = 5
n_frames_totales = cam_uptime * n_frames_segundos  #Era 3
#frames_per_second = 20 
frame_counter = 0



prediction_points = []

green = (0,255,0)
blue = (0,0,255)
red = (255,0,0)

colour_lists =[]
colour_lists.append(green)
colour_lists.append(blue)
colour_lists.append(red)

def returnArea(x1,x2,y1,y2):
    return (x2-x1) * (y2-y1)

while True:
    time_start = time.time()
    #print(time_passed)
    if time_passed > cam_uptime:
       break
    
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    

    faces = detector(gray)

    x1_max = 0
    x2_max = 0
    y1_max = 0
    y2_max = 0

    max_area = returnArea(x1_max,x2_max,y1_max,y2_max)

    i = 0
    #actual_face
    #if len(faces) != 0: 
    actual_face = [(None,None),(None,None)]
    for face in faces:
        
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        temp_area = returnArea(x1,x2,y1,y2)

        if max_area < temp_area:
            x1_max = x1
            x2_max = x2
            y1_max = y1
            y2_max = y2
            actual_face = face
        
        '''

        if i == colour_lists.count: i = 0

        cv2.rectangle(frame, (x1,y1), (x2,y2), colour_lists[i], 3)

        i = i +1
        
        
        landmarks = predictor(gray, face)
        face_points = []
        for i in range(0, 68):       
            cv2.circle(frame, (landmarks.part(i).x,landmarks.part(i).y), 4, (255, 0, 0), -1)
            face_points.append((landmarks.part(i).x,landmarks.part(i).y))
        prediction_points.append(face_points)
        '''
    
    cv2.rectangle(frame,(x1_max,y1_max),(x2_max,y2_max),green,3)

    cv2.imshow("Frame", frame)

    #Conseguir los 68 puntos del rostro predominante de este frame
    landmarks = predictor(gray, actual_face)
    face_points = []
    for i in range(0, 68):       
        cv2.circle(frame, (landmarks.part(i).x,landmarks.part(i).y), 4, (255, 0, 0), -1)
        face_points.append((landmarks.part(i).x,landmarks.part(i).y))
    prediction_points.append(face_points)

    if cam_initialized == False:
        cam_initialized = True
        time_start = time.time()
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    time_end = time.time()
    time_passed += time_end - time_start
    frame_counter+=1
print("Total time Passed: " + str(time_passed))
print("Number of frames: " + str(frame_counter))

frame_mod = frame_counter//n_frames_totales
frame_mod_res = frame_counter % n_frames_totales
print("Frame modifier: " +str(frame_mod))

temp = []
#Iniciación del excel
day = (datetime.datetime.now()).strftime("%Y-%m-%d")
hour = (datetime.datetime.now()).strftime("%H-%M-%S")
workbook = xlsxwriter.Workbook(day+"_"+hour+'.xlsx')
worksheet = workbook.add_worksheet()
row = 1
time_frames = []
dummy_time = 0

bold = workbook.add_format({'bold': 1})
worksheet.write(0,0,"Time",bold)
col = 1
for i in range (68):
    worksheet.write(0,col,"Punto "+str(i+1),bold)
    col = col + 2

for i in range (frame_counter - frame_mod_res):
    if i % frame_mod == 0:
        col = 0
        #print(str(i) + " - " + "{:.2f}".format(dummy_time))
        worksheet.write_string(row, col, "{:.2f}".format(dummy_time))
        col = 1
        for point in prediction_points[i]:
            worksheet.write_number(row,col,point[0])
            worksheet.write_number(row,col+1,point[1])
            col = col +2
        row += 1

        time_frames.append(dummy_time)
        temp.append(prediction_points[i])
        dummy_time += (cam_uptime / n_frames_totales)

workbook.close()
prediction_points = temp