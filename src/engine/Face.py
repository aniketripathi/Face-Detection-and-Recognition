'''
Created on 18-Jan-2021

@author: Aniket Kumar Tripathi
'''


class Face: 

    def __init__(self, face_id, image_id, location, signature, recognized=False):
        self.id = face_id
        self.image = image_id
        self.location = location
        self.signature = signature
        self.recognized = recognized
        
