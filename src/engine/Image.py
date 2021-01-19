'''
Created on 18-Jan-2021

@author: Aniket Kumar Tripathi
'''
from cv2 import imread


# Image class encapsulates an image supported by lazy loading. The image is loaded using opencv.imread()
# img_id : Unique image id.
# location : location of the image. This class is not responsible to verify valid locations.
# load : If True the image is instantly loaded otherwise it is loaded when the image is accessed.
# scanned : True or False. Whether the image is scanned for face detection. False by default.
# faces : List of faces detected in this image. Only to be used if scanned = True. None by default.
class Image:
    
    def __init__(self, img_id, location, load=False, scanned=False, faces=None):
        self.id = img_id
        self.location = location
        self.__imgdata__ = imread(location) if load else None
        self.loaded = load
        self.scanned = scanned
        self.faces = faces if scanned else None
    
    # Use this method to access the image
    def imgdata(self):
        
        if(not self.loaded):
            # Load image from location if not loaded
            self.__imgdata__ = imread(self.location)
            self.loaded = True
            
        return self.__imgdata__
    
    # Use this to save memory
    def __unload__(self):
        self.__imgdata__ = None
        self.loaded = False
