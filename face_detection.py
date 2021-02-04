# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 23:23:54 2021

@author: Shashi
"""

import cv2
import face_recognition
import os
from datetime import datetime

import Face
import Image

class FaceDetection:
    
    def scan(self, images):
        
		# count stores number of images scanned
		self.count = 0
		
		# id stores Face_id
		self.id = 0
		
        for img in self.images:
            
            # Image load in imgTest
            self.imgTest = face_recognition.load_image_file(img)
            
            # Image faceLocation stored in faceLoc
			# face_location returns A list of tuples of found face locations in css (top, right, bottom, left) order
            self.faceLoc = face_recognition.face_locations(self.imgTest)
			
			# count increment after successfully image scan
			self.count += 1
            
            # if face not found faceLoc will be empty
            # len(faceLoc) == 0 that means face not found
            if len(self.faceLoc) == 0:
                continue
            
            # else
			# face found in given image
            
            # face_encodings returns A list of 128-dimensional face encodings (one for each face in the image)
            self.encodeImg = face_recognition.face_encodings(self.faceLoc)
            
            for i in len(self.faceLoc):
				# face_id = id
				Face.face_id = self.id
				self.id += 1
				
				# signature = 128-dimension face encoding for each face in the image
				Face.signature = self.encodeImg[i]
            
            # image_id = name of image file + current date and time
            Face.image_id = f'{os.path.splitext(img)[0]}'        
            
            
        
