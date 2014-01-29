#! /usr/bin/env python 

# -*- coding: utf-8 -*-

#Imports
#*************************************************************************

import cv2 
import serial
import numpy as np


#puerto = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

#*************************************************************************

#Funciones 
#*************************************************************************
def dondeEstoy(x_imagen,y_imagen,x,y):
    tol=60
    #derecha
    if (0 < x < x_imagen/2) :

        print 'derecha'
        
        #puerto.write('d')

    #Adelante
    if ( (x_imagen/2)-tol< x < (x_imagen/2)+tol) :

        print 'Adelante'
        #puerto.write('a')

    #izquierda
    if (x_imagen/2 < x < x_imagen) :

        print 'izquierda'
        #puerto.write('i')


#*************************************************************************

cam_num = 0
video = cv2.VideoCapture(cam_num)
#cv2.namedWindow("Captura de Camara")

if video.isOpened():

    flag, frame = video.read()
else:

    flag = False
    print 'No hay camara disponible'


#Comienzo del loop 
contador = 0
while flag:

    flag, frame = video.read()
    
    #Comienzo del procesamiento

    ROI = frame[20:-1,80:560] 
    (y, x, chanels) = ROI.shape

    #smoot the image 
    #-------------------------------------------------------------------------
    ROI = cv2.GaussianBlur(ROI,(5,5),0) #parametros: size kernel, media max
    #frame = cv2.medianBlur(frame,5)
    #frame = cv2.bilateralFilter(frame,9,0,0)

    #-------------------------------------------------------------------------

    hsv_img = cv2.cvtColor(ROI, cv2.COLOR_BGR2HLS)
    hsv_img_eq = hsv_img.copy()
    chanel_V = hsv_img_eq[:,:,1]
    chanel_V = cv2.equalizeHist(chanel_V)
    hsv_img_eq[:,:,1] = chanel_V

    #frame_back = cv2.cvtColor(hsv_img_eq,cv2.COLOR_HLS2BGR_FULL)

    cv2.line(ROI,(x,y/2),(0,y/2),(0,0,237),1,8)
    cv2.line(ROI,(x/2,0),(x/2,y),(0,0,237),1,8)

    lower_green = np.array([69,100,60])
    upper_green = np.array([80,170,70])

    # Threshold the HSV image to get only green colors
    #-------------------------------------------------------------------------
    mask = cv2.inRange(hsv_img, lower_green, upper_green)
    #-------------------------------------------------------------------------
    
    #dilate
    #-------------------------------------------------------------------------
    #kernel = np.ones((3,3),'uint8') 
    #mask = cv2.dilate(mask,kernel)
    #-------------------------------------------------------------------------

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(ROI,ROI, mask= mask)
    
    moments = cv2.moments(mask)


    area = moments['m00']

    print area 

    if (area > 500 ):
        contador +=1
        x_track = int( np.round(moments['m10'] / area))
        y_track = int(np.round(moments['m01'] / area))
        centro = (x_track,y_track)
        
        dondeEstoy(x,y,x_track,y_track)

        cv2.circle(ROI,centro,5,(0,255,0),15)

    
    cv2.imshow('frame',frame)
    #cv2.imshow('frame restaurada',frame_back)

    cv2.imshow('resultado',ROI)
    #cv2.imshow('hsv eq',hsv_img_eq)

    #cv2.imshow("Captura de Camara",frame) #mostramos la imagen

    key = cv2.waitKey(3) #Capturamos la tecla ESC

    if key == 27 :
        flag = False
#puerto.close()        
cv2.destroyAllWindows()
print 'la cantidad de veces detectada es',contador
