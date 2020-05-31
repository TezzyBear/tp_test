import cv2
import numpy as np
import dlib
import time
import pandas as pd #pandas 1.0.3
import os
import xlsxwriter #pip install XlsxWriter 1.2.8
import datetime #pip install dateTime 4.3

#Face recognition and prediction variables
#cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#Timer variables
time_passed = 0
cam_initialized = False
cam_uptime = 2 #in seconds

#Frame variables
n_frames_segundos = 5
n_frames_totales = cam_uptime * n_frames_segundos  #Era 3
#frames_per_second = 20 
frame_counter = 0

def returnArea(x1,x2,y1,y2):
    return (x2-x1) * (y2-y1)


def main_function(video_path, save_path):
    cap = cv2.VideoCapture(video_path)
    frame_number = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print("FPS:" + str(fps))
    print("Frame Number: " + str(frame_number))
    seconds = int(frame_number / fps)
    print("Seconds: " + str(seconds))

    n_frames_segundos = 5
    n_frames_totales = seconds * n_frames_segundos  #Era 3

    green = (0,255,0)
    prediction_points = []
    face_points = []

    frame_counter = 0
    print(frame_counter)
    while(cap.isOpened() and frame_counter < frame_number):
        frame_counter += 1
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('frame',frame)
        
        faces = detector(gray)

        x1_max = 0
        x2_max = 0
        y1_max = 0
        y2_max = 0

        max_area = returnArea(x1_max,x2_max,y1_max,y2_max)

        if len(faces) != 0: 
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

            cv2.rectangle(frame,(x1_max,y1_max),(x2_max,y2_max),green,3)
            #cv2.imshow("Frame", frame)

            #Conseguir los 68 puntos del rostro predominante de este frame
            landmarks = predictor(gray, actual_face)
            face_points = []
            for i in range(0, 68):       
                cv2.circle(frame, (landmarks.part(i).x,landmarks.part(i).y), 4, (255, 0, 0), -1)
                face_points.append((landmarks.part(i).x,landmarks.part(i).y))
            prediction_points.append(face_points)
            
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

    print("Total time Passed: " + str(seconds))
    print("Number of frames: " + str(frame_counter))

    frame_mod = frame_counter//n_frames_totales
    frame_mod_res = frame_counter % n_frames_totales
    print("Frame module: " +str(frame_mod))

    temp = []
    #Iniciación del excel
    workbook = xlsxwriter.Workbook(save_path+'.xlsx')
    worksheet = workbook.add_worksheet()
    row = 2
    time_frames = []
    dummy_time = 0

    # Create a format to use in the merged range.
    title_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'blue'})

    subtitle_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'
        })

    normal_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
        })


    #Organizar los títulos
    worksheet.merge_range(0,0,1,0,"Time",title_format)
    col = 1
    for i in range (68):
        worksheet.write(0,col,"Punto "+str(i+1),title_format)
        worksheet.merge_range(0,col,0,col+1,"Punto "+str(i+1),title_format)
        worksheet.write(1,col,"X",subtitle_format)
        worksheet.write(1,col + 1,"Y",subtitle_format)
        col = col + 2

    #Guardar los valores de los puntos
    for i in range (frame_counter - frame_mod_res):
        if i >= len(prediction_points):
            break
        if i % frame_mod == 0:
            col = 0
            worksheet.write_string(row, col, "{:.2f}".format(dummy_time),normal_format)
            col = 1
            for point in prediction_points[i]:
                worksheet.write_number(row,col,point[0],normal_format)
                worksheet.write_number(row,col+1,point[1],normal_format)
                col = col +2
            row += 1

            time_frames.append(dummy_time)
            temp.append(prediction_points[i])
            dummy_time += (seconds / n_frames_totales)

    workbook.close()
    prediction_points = temp

#path = 'my_directory/'
path = "C:/Users/Ansset Rojas G/Desktop/UPC/Ciclo VIII/TDP/IA de la verdad/MU3D-Package/Videos/"
path_result = 'Results/'
entries = os.listdir(path)



for entry in entries:
    print(entry)
    new_path = path + entry
    save_path = path_result + entry
    main_function(new_path, save_path)
    print("=================================================")
print("Succes")
