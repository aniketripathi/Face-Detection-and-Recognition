'''

Created on 2-Feb-2021

@author: Aniket Kumar Tripathi

'''
import face_recognition

class Album:
    def __init__(self, id, name, face):
        self.id = id
        self.name = name
        self.face = face
        self.matching_faces = None

    def scan(faces, threshold=0.6):
        self.matching_faces = []
        
        for face in faces:
            match = face_recognition.compare_faces(face.signature, self.face.signature,tolerance=threshold)
            if(match):
                self.matching_faces.append(face.id)
