import numpy as np
import cv2
import socket
import sys
import os
import pdb
import serial
import time
import math

# Serial entworking 
ser = serial.Serial('/dev/ttyUSB0',9600)
if ser is None:
   ser = serial.Serial('/dev/ttyUSB1',9600)

# Stream video load
video_capture = cv2.VideoCapture(-1)
video_capture.set(3, 320)
video_capture.set(4, 240)

# Variable for add previous direction 
previous = []

while(True):
   
   # Crop video
   for i in xrange(5):
       video_capture.grab()
   ret, frame = video_capture.read()
   crop_img = frame[80:240, 0:320]

   # Change RGB to gray
   # Add Gaussian filter to reomove noise
   gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
   blur = cv2.GaussianBlur(gray,(9,9),0)

   # Set threshold to extract black color
   ret,thresh1 = cv2.threshold(blur,80,255,cv2.THRESH_BINARY_INV)

   # Make contour to smooth
   mask = cv2.erode(thresh1, None, iterations=2)
   mask = cv2.dilate(mask, None, iterations=2)

   # Save contour
   contours, _ = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)[-2:]


   # If 'previous' is full, pop the first element
   if len(previous) == 5:
       previous.pop(0)
  
   # If the car fail to find way, go straight 
   if len(previous) == 4 and previous[0] == previous[2] and previous[1] == previous[3]:
       ser.write((b'F\n').encode('ascii'))
       previous.append('X')
  
   # If contour extracted, calculate the center
   elif len(contours) > 0:
       c = max(contours, key=cv2.contourArea)
       M = cv2.moments(c)

       cx = int(M['m10']/M['m00'])
       cy = int(M['m01']/M['m00'])

       cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
       cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

       cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

       print cx
       print cy

      # If the line located in right, go right
       if cx >= 120:
           ser.write((b'R\n').encode('ascii'))
           previous.append('R')

      # If the line located in the middel, go forward      
       if cx < 120 and cx > 50:
           ser.write((b'F\n').encode('ascii'))
           previous.append('F')
         
      # If the line located in left, go left
       if cx <= 50:
           ser.write((b'L\n').encode('ascii'))
           previous.append('L')

   # If can't find line, go backward
   else:
       ser.write((b'B\n').encode('ascii'))
       previous.append('B')
  
   # Show the camera
   cv2.imshow('frame',crop_img)
   if cv2.waitKey(150) & 0xFF == ord('q'):
       break
  
   read_serial = ser.readline()
   print(read_serial)
