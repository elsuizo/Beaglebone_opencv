#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 01:36:36 2013

@author: elsuizo
"""

#
import cv

import os

import time

import serial

import numpy as np
#************************************************************************
#para encender los leds de la beaglebone
##==============================================================================
led0_on = 'echo 1 > /sys/class/leds/beaglebone::usr0/brightness'
led0_off = 'echo 0 > /sys/class/leds/beaglebone::usr0/brightness'
#
led1_on = 'echo 1 > /sys/class/leds/beaglebone::usr1/brightness'
led1_off = 'echo 0 > /sys/class/leds/beaglebone::usr1/brightness'
#
led2_on = 'echo 1 > /sys/class/leds/beaglebone::usr2/brightness'
led2_off = 'echo 0 > /sys/class/leds/beaglebone::usr2/brightness'
#
led3_on = 'echo 1 > /sys/class/leds/beaglebone::usr3/brightness'
led3_off = 'echo 0 > /sys/class/leds/beaglebone::usr3/brightness'
##=============================================================================
#************************************************************************

#************************************************************************
#Funciones
#************************************************************************

#puerto=serial.Serial('/dev/ttyACM0',9600,timeout=1)

def dondeEstoy(x_imagen,y_imagen,x,y):
    tol=60
    #derecha
    if (0 < x < x_imagen/2) :

        print 'derecha'
        
        #puerto.write('d')

    #Adealnte
    if ( (x_imagen/2)-tol< x < (x_imagen/2)+tol) :

        print 'Adelante'
        #puerto.write('a')

    #izquierda
    if (x_imagen/2 < x < x_imagen) :

        print 'izquierda'
        #puerto.write('i')


#************************************************************************
capture = cv.CaptureFromCAM(0)
#k=0
cv.NamedWindow("ventana1", 0 )
cv.NamedWindow( "ventana2", 0 )
tol=20
k=0
while (True and k<100):


    img = cv.QueryFrame( capture )

    (x2,y2)=cv.GetSize(img)
    #cv.SetImageROI(img, (110,37,420,410))
    cv.Smooth(img, img, cv.CV_BLUR, 3);


    hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3)
    cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV)


    thresholded_img =  cv.CreateImage(cv.GetSize(hsv_img), 8, 1)
    #cv.InRangeS(hsv_img, (120, 80, 80), (140, 255, 255), thresholded_img) #purple
    #cv.InRangeS(hsv_img, (104, 178, 70), (130, 240, 124), thresholded_img) #azul
    cv.InRangeS(hsv_img, (69, 100, 60), (80, 170, 70), thresholded_img) #verde
    moments = cv.Moments(cv.GetMat(thresholded_img),0)
    area = cv.GetCentralMoment(moments, 0, 0)

    cv.Line(img, (x2,y2/2),(0,y2/2), (255, 0, 0), 1, 8)
    cv.Line(img, (x2/2,0),(x2/2,y2), (0, 255, 0), 1, 8)

    print area

    if(area > 90):


        #print 'hola'

        x = cv.GetSpatialMoment(moments, 1, 0)/area
        y = cv.GetSpatialMoment(moments, 0, 1)/area
        x1=cv.Round(x)
        y1=cv.Round(y)
        centro=(x1,y1)

        dondeEstoy(x2,y2,x1,y1)

        #print 'x: ' + str(x) + ' y: ' + str(y) + ' area: ' + str(area)


        #overlay = cv.CreateImage(cv.GetSize(img), 8, 3)

        cv.Circle(img, centro, 5, (255, 255, 255), 20)

        #cv.Dilate(thresholded_img,thresholded_img,None,3)


        #cv.Merge(thresholded_img, None, None, None, img)


    cv.ShowImage("ventana1", img)
    cv.ShowImage("ventana2", thresholded_img)
    k+=1
    if cv.WaitKey(3) == 27:
        puerto.close()
        break
