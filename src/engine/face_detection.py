# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 23:23:54 2021

@author: Shashi
"""

import face_recognition
import os
from .Face import Face



def scan(images):

    # Number of images
    count = 0

    for img in images:

        # Image faceLocation stored in faceLoc
        # face_location returns A list of tuples of found face locations in css
        # (top, right, bottom, left) order
        # count increment after successfully image scan
        faceLoc = face.recognition.face_locations(img.imgdata())
        count += 1
        
        # if face not found faceLoc will be empty
        # len(faceLoc) == 0 that means face not found
        # else face found in given image
        if len(faceLoc) == 0:
            continue

        # face_encodings returns A list of 128-dimensional face encodings
        # (one for each face in the image)
        encodeImg = face_recognition.face_encodings(faceLoc)

        faces = [Face(i, img.id, faceLoc[i], encodeImg[i]) for i in range(len(faceLoc))]

        img.faces = faces

    return count
