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

'''
class Face: 

    def __init__(self, face_id, image_id, signature, recognized=False):
        self.id = face_id
        self.image = image_id
        self.signature = signature
        self.recognized = recognized
        
        # Input - images - A list of images of type Image
        # Scans all the Images present in images list for faces and adds faces to image.face
        # Returns - Number of images scanned successfully
'''

class FaceDetection:
    
    def scan(self, images):
        
        for img in self.images:
            
            # Image load in imgTest
            self.imgTest = face_recognition.load_image_file(img)
            
            # Image faceLocation stored in faceLoc
            self.faceLoc = face_recognition.face_locations(self.imgTest)
            
            # if face not found faceLoc will be empty
            # len(faceLoc) == 0 that means face not found
            if len(self.faceLoc) == 0:
                continue
            
            # face found in given image
            
            # 128 face metrics stored in encodeImg
            self.encodeImg = face_recognition.face_encodings(self.faceLoc)
            
            # Date and Time loaded for giving unique id
            self.now = datetime.now()
            dt_string = self.now.strftime("%d/%m/%Y_%H:%M:%S")
            
            # face_id = index of image in image list + current date and time
            Face.face_id = f'{images.index(img)}_{dt_string}'
            
            # image_id = name of image file + current date and time
            Face.image_id = f'{os.path.splitext(img)[0]}_{dt_string}'
            
            # signature = 128 metrics of face found in image file
            Face.signature = self.encodeImg
            
            
            
        