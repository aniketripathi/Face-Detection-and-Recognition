
import engine.image_manager as imgmanager
import engine.face_detection as fd
import os
from timeit import default_timer as timer

# This module is designed to test the performance

# Print current working directory
print(os.getcwd())

# Modify this
loc = 'data/images/'

dirs = ['0--Parade/']   #, '10--People_Marching/', '13--Interview/', '23--Shoppers/']
dirs = [''.join((loc ,dirs[i])) for i in range(len(dirs))]

start = timer()
lazy_images = imgmanager.load(dirs)
end = timer()
count = len(lazy_images)
print(f"Time to lazy load {count} images is ", (end-start))

start = timer()
images = imgmanager.load(dirs, load=True)
end = timer()
count = len(images)
print(f"Time to load {count} images is ", (end-start))

start = timer()
count = fd.scan(lazy_images)
end = timer()
print(f"Time to scan lazy {count} images is ", (end-start))

start = timer()
count = fd.scan(images)
end = timer()
print(f"Time to scan {count} images is ", (end-start))
