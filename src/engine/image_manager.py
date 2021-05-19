'''
Created on 18-Jan-2021

@author: Aniket Kumar Tripathi
'''

import os
import collections
import imghdr

from .base import Image

# A variable used to generate unique image id_
__imid__ = -1


# Function to generate unique image id_
def __gen_imageid__():
    global __imid__
    __imid__ += 1
    return __imid__


# Load images from given directory or set of directories.
# dirs = A single directory (str) or a set of directories(a sequence of
# strings)
# load = If false image data is not loaded (by Default) and will be loaded when
# used.
# Returns - A list of images of type Image
def load(dirs, lazy=False):
    images = []
    if isinstance(dirs, str):
        dirs = [dirs]

    if isinstance(dirs, collections.Sequence):
        for path in dirs:
            for subpath in os.listdir(path):
                file = ''.join([path, subpath])
                if(os.path.isfile(file) and imghdr.what(file)):
                    image = Image(__gen_imageid__(), file, lazy)
                    images.append(image)
    return images

def __reset_id__():
    global __imid__
    __imid__ = -1
