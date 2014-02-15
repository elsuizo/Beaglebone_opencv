#! /usr/bin/env python

import cv2 
from time import time

t_start = time()

cam_num = 0
video = cv2.VideoCapture(cam_num)

if not video.isOpened():
    print 'No se pudo conectar la camara '

frames = 10

for i in xrange(frames):
    flag, frame = video.read()
    edges = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(edges, 0, 30, 3)

t_end = time()
#cv2.imwrite('edges_py.png', edges)
cv2.imwrite('capture_py.png', frame)

print 'tardo :%f(seg) en procesar %d frames'  % ((t_end - t_start) , frames)
print 'Adquiriendo y procesando %f frames por seg ' % (frames/(t_end-t_start))
