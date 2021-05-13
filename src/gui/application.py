'''
Created on 05-April-2021

@author: Aniket Kumar Tripathi
'''

import tkinter as tk
from tkinter.ttk import Progressbar as pb
from PIL import Image as pImage, ImageTk
from os import path as path

from .helper_widgets import ScrollableFrame
from .helper_widgets import Thumbnail
from .helper_windows import Albums_Dialog
from src.engine.base import Image
import src.engine.face_detection as fd
from src.engine.base import Album
import src.engine.image_manager as image_manager


class Application:
    albums = []

    # Images from which albums were created
    album_images = []

    # Frame that holds the images corresponding to albums
    albumimages_panes = []

    # Holds Thumbnails for albums
    album_thumbnails = []

    # Holds all images to be scanned (except th e image from which album was
    # created
    images = None

    __albumcount__ = 0

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Face Recognition")
        self.root.geometry('1024x768')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.state('zoomed')

        # self.base container - containes 2 children - self.toolbar and main
        # pane
        self.base = tk.Frame(self.root, pady=5)
        self.base.grid(row=0, column=0, sticky='nsew')
        self.base.grid_columnconfigure(0, weight=1)
        self.base.grid_rowconfigure(1, weight=1)

        # self.toolbar container
        self.toolbar = tk.Frame(self.base, padx=10, pady=5, relief=tk.GROOVE, bd=5, height=50)
        self.toolbar.grid(row=0, column=0, sticky='nsew')
        self.add_album_button = tk.Button(self.toolbar, text='Add albums', command=lambda:self.scan_albumimage(self.root))
        self.add_album_button.grid(row=0, column=0)

        self.scan_button = tk.Button(self.toolbar, text='Scan', command=lambda: self.scan_directory(self.root))
        self.scan_button.grid(row=0, column=1)

        # Main Pane - album pane and image pane
        self.main_pane = tk.Frame(self.base, bd=1)
        self.main_pane.grid(row=1, column=0, sticky='nsew')
        self.main_pane.grid_columnconfigure(1, weight=1)
        self.main_pane.grid_rowconfigure(0, weight=1)

        # Album container
        self.album_pane = ScrollableFrame(self.main_pane, labelanchor='n', text='Album', padx=2, pady=2, relief=tk.SUNKEN, bd=3, width=192)
        self.album_pane.grid_propagate(0)
        self.album_pane.grid_columnconfigure(0, weight=1)
        self.album_pane.grid_rowconfigure(0, weight=1)
        self.album_pane.grid(row=0 , column=0, sticky='nsew')

        # Image container
        self.image_pane = tk.LabelFrame(self.main_pane, labelanchor='n', text='Images', padx=2, pady=5, relief=tk.SUNKEN,bd=3)
        self.image_pane.grid(row=0, column=1, sticky='nsew')
        self.image_pane.grid_columnconfigure(0, weight=1)
        self.image_pane.grid_rowconfigure(0, weight=1)


        self.root.mainloop()



    def album_leftmouse(self, id):
        print(id)
        print("left mouse clicked")
        self.album_pane.members[id].frame.focus_set()
        self.albumimages_panes[id].tkraise()

    def album_rightmouse(self, id):
        None

    def scan_directory(self, parent):
        print('scanning ... \n')
        folder = tk.filedialog.askdirectory() + "/"
        self.images = image_manager.load(folder)
        print(folder, ' ', len(self.images))
        fd.scan(self.images)

        for album in self.albums:
            album.scan(self.images)
            sf = ScrollableFrame(self.image_pane)
            sf.grid(row=0, column=0, sticky='nsew')
            sf.grid_rowconfigure(0, weight=1)
            sf.grid_columnconfigure(0, weight=1)
            self.albumimages_panes.append(sf)

            i = 0
            print(' faces in album ', album.id, ' = ', len(album.matching_faces))
            for mface in album.matching_faces:
                mimage = self.images[mface.image]
                thumb = Thumbnail(id=mimage.id,container=self.albumimages_panes[album.id].sframe,image=mimage.getPILimage())
                thumb.frame.grid(row = i // 3, column = i % 3)
                sf.members.append(thumb)
                i += 1
        print('scanning finished ... \n')

    def scan_albumimage(self,parent):
        ad = Albums_Dialog(parent)
        parent.wait_window(ad.top)
        if(ad.closed):
            file = ad.file_name
            if(file):
                img = Image(0, file)
                fd.scan([img],unload=True)
                self.album_images.append(img)
                i = 0
                for face in img.faces :
                    l = face.location
                    # (top,right,bottom,left) -> (left,top,right,bottom)
                    im = img.getPILimage().crop((l[3],l[0],l[1],l[2]))
                    album_thumb = Thumbnail(id=self.__albumcount__,container=self.album_pane.sframe,image=im,
                                           leftmouse_action=self.album_leftmouse, rightmouse_action=self.album_rightmouse)
                    album_thumb.frame.grid(row=i, column=0)
                    self.album_thumbnails.append(album_thumb)
                    album = Album(self.__albumcount__, None, face)
                    self.__albumcount__ += 1
                    self.albums.append(album)
                    self.album_pane.members.append(album_thumb)
                    self.root.update()
                    i += 1