# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 23:23:54 2021

@author: Shashi
"""

import face_recognition
from .base import Face


__count__ = 0
__current_image__ = None

def scan(images, unload=False):

    # Number of images
    global __count__

    global __current_image__

    for img in images:

        __current_image__ = img
        # Image faceLocation stored in faceLoc
        # face_location returns A list of tuples of found face locations in
        # css
        # (top, right, bottom, left) order
        # count increment after successfully image scan
        face_location = face_recognition.face_locations(img.imgdata())

        # if face not found faceLoc will be empty
        # len(faceLoc) == 0 that means face not found
        # else face found in given image
        if len(face_location) == 0:
            img.faces = []
            img.scanned = True
            continue

        # face_encodings returns A list of 128-dimensional face encodings
        # (one for each face in the image)
        encode_image = face_recognition.face_encodings(img.imgdata(),known_face_locations=face_location)

        faces = [Face(i, img.id_, face_location[i], encode_image[i]) for i in range(len(face_location))]

        img.faces = faces
        img.scanned = True

        # Use this if there are too many images to scan
        if unload:
            img.__unload__()

        __count__ += 1

    return __count__

def __reset_count__():
    global count
    count = 0