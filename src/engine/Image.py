'''
Created on 18-Jan-2021

@author: Aniket Kumar Tripathi
'''


class Image:
    
    def __init__(self, img_id, location, img_data=None, loaded=False, scanned=False, faces=None):
        self.id = img_id
        self.location = location
        self.__imgdata__ = img_data
        self.loaded = loaded
        self.scanned = scanned
        self.faces = faces
    
    # Use this method to access the image array
    def imgdata(self):
        
        if(not self.loaded):
            # Load image from location if not loaded
            self.loaded = True
            
        return self.__imgdata__
