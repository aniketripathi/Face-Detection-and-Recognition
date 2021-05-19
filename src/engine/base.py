'''
Created on 08-April-2021

@author: Aniket Kumar Tripathi
'''

from face_recognition import face_distance
from face_recognition import load_image_file
from PIL import Image as pImage

class Album:
    def __init__(self, id_, face, name=None):
        self.id_ = id_
        self.name = 'Album' + str(id_) if not name else name
        self.face = face
        self.matching_faces = []

    # Scan a list of images.  For any image if a face matches with the face of
    # this album then that face is saved in matching faces.  1 album is alowed
    # to match only 1 face in each image.
    def scan(self, images, threshold=0.6):
        for img in images:
            for face in img.faces:
                match = face_distance([face.signature], self.face.signature) <= threshold
                if match[0]:
                    self.matching_faces.append(face)
                    face.album = self
                    face.recognized = True
                    break

class Face:

    def __init__(self, face_id, image_id, location, signature, recognized=False):
        self.id_ = face_id
        self.image = image_id
        self.location = location
        self.signature = signature
        self.recognized = recognized
        self.album = None



class Image:
    # Image class encapsulates an image supported by lazy loading.  The image
    # is loaded using opencv.imread()
    # img_id : Unique image id_.
    # location : location of the image.  This class is not responsible to
    # verify valid locations.
    # load : If True the image is instantly loaded otherwise it is loaded when
    # the image is accessed.
    # scanned : True or False.  Whether the image is scanned for face
    # detection.  False by default.
    # faces : List of faces detected in this image.  Only to be used if
    # scanned
    # = True.  None by default.


    def __init__(self, img_id, location, lazy=False, faces=None):
        self.id_ = img_id
        self.location = location
        self.__imgdata__ = load_image_file(location) if lazy else None
        self.loaded = lazy
        self.faces = faces

    # Use this method to access the image
    def imgdata(self):

        if not self.loaded:
            # Load image from location if not loaded
            self.__imgdata__ = load_image_file(self.location)
            self.loaded = True

        return self.__imgdata__

    # Use this to save memory
    def __unload__(self):
        self.__imgdata__ = None
        self.loaded = False

    # Returns PIL image of __imgdata__
    def get_PIL_image(self, unload=True):
        img = pImage.fromarray(self.imgdata().astype('uint8'), 'RGB')
        if unload :
            self.__unload__()
        return img
