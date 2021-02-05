import engine.image_manager as imgmanager
import engine.face_detection as fd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os


# This module is designed to test phase 1

# Print current working directory
print(os.getcwd())

# Modify this
loc = 'data/images/'

dirs = ['0--Parade/', '10--People_Marching/', '13--Interview/', '23--Shoppers/']
dir = loc+'22--Picnic/'
dirs = [''.join((loc ,dirs[i])) for i in range(len(dirs))]

# Test Loading a single directory Non lazy
single_dir_images = imgmanager.load(dir,load=False)

# Test loading multiple directories Lazy loading
multiple_dir_images = imgmanager.load(dirs,load)


# Single directory
n = 6
fig1, axes1 = plt.subplots(2,3)
for (ax,i) in zip(axes1.flat, range(n)):
    ax.imshow(single_dir_images[i].imgdata())
    ax.axis('off')
fig1.show()

# Multiple directory
n = 6
fig2, axes2 = plt.subplots(2,3)
for (ax,i) in zip(axes2.flat, range(n)):
    ax.imshow(multiple_dir_images[i].imgdata())
    ax.axis('off')
fig2.show()

plt.show()

n = 6
# Testing face detection
print(len(single_dir_images))
count = fd.scan(multiple_dir_images[0:n])
print(count)

fig3, axes3 = plt.subplots(2,3)
for (ax,i) in zip(axes3.flat, range(n)):
        faces = multiple_dir_images[i].faces
        ax.imshow(multiple_dir_images[i].imgdata())
        ax.axis('on')
        for j in range(len(faces)):
            loc = faces[j].location
            print(i,loc)
            rect = patches.Rectangle((loc[3],loc[0]), loc[1]-loc[3], loc[2]-loc[0], fill=False, linewidth=2, color='green')
            print(rect)
            ax.add_patch(rect)

fig3.show()
plt.show()