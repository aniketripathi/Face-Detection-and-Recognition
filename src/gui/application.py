'''
Created on 05-April-2021

@author: Aniket Kumar Tripathi
'''

import tkinter as tk
from tkinter.ttk import Progressbar as pb
from PIL import Image as pImage, ImageTk
from os import path as path
from threading import Thread

from .helper_widgets import ScrollableFrame
from .helper_widgets import Thumbnail
from .helper_widgets import Album_Thumbnail
from .helper_windows import Albums_Dialog
from .helper_windows import Loading_Bar
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
    images = []
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
        self.toolbar = tk.Frame(self.base, pady=5, relief=tk.GROOVE, bd=5, height=50)
        self.toolbar.grid(row=0, column=0, sticky='nsew')
        self.add_album_button = tk.Button(self.toolbar, text='Add albums', command=lambda:self.scan_albumimage(self.root))
        self.add_album_button.grid(row=0, column=0, padx=5)

        self.scan_button = tk.Button(self.toolbar, text='Scan', padx=5, command=lambda: self.scan_directory(self.root))
        self.scan_button.grid(row=0, column=1, padx=5)

        # Main Pane - album pane and image pane
        self.main_pane = tk.Frame(self.base, bd=1)
        self.main_pane.grid(row=1, column=0, sticky='nsew')
        self.main_pane.grid_columnconfigure(1, weight=1)
        self.main_pane.grid_rowconfigure(0, weight=1)

        # Album container
        self.album_pane = ScrollableFrame(self.main_pane, labelanchor='n', text='Album', padx=2, pady=2, takefocus=False, relief=tk.SUNKEN, bd=3, width=192)
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



    def album_leftmouse(self, id_):
        if self.albumimages_panes :
          self.albumimages_panes[id_].tkraise()

    def album_rightmouse(self, id_):
        None

    def scan_directory(self, parent):
        folder = tk.filedialog.askdirectory() + "/"
        unscanned_images = image_manager.load(folder)
        if unscanned_images:
            class Scan_Progress:
                def __init__(self):
                    self.album = None
                    self.album_scancount = 0
                    self.face_detection_complete = False
                    self.face_recognition_complete = False

            sp = Scan_Progress()
            self.images += unscanned_images

            def process(scan_progress=sp):
                fd.scan(unscanned_images)
                scan_progress.face_detection_complete = True

                for album in self.albums:
                    scan_progress.album = album
                    album.scan(unscanned_images)
                    scan_progress.album_scancount += 1
                scan_progress.face_recognition_complete = True

            loading_bar = Loading_Bar(self.root, "Loading Albums", len(unscanned_images) + len(self.albums))
            albumthread = Thread(target = lambda : process())

            def update_var(scan_progress=sp):
                if not scan_progress.face_detection_complete :
                    loading_bar.value = fd.__count__
                    if fd.__current_image__ :
                        loading_bar.text = 'Detecting Faces ... ' + self.images[fd.__current_image__.id_].location

                elif not scan_progress.face_recognition_complete :
                    loading_bar.value = fd.__count__ + scan_progress.album_scancount
                    if scan_progress.album:
                        loading_bar.text = 'Recognizing Faces for album ...' + scan_progress.album.id_

                else :
                    loading_bar.value = len(unscanned_images) + len(self.albums)
                    loading_bar.text = 'Complete'


            albumthread.start()
            loading_bar.start(update_var)
            parent.wait_window(loading_bar.root)

            for album in self.albums:
                sf = ScrollableFrame(self.image_pane)
                sf.grid(row=0, column=0, sticky='nsew')
                sf.grid_rowconfigure(0, weight=1)
                sf.grid_columnconfigure(0, weight=1)
                self.albumimages_panes.append(sf)

                i = 0
                for mface in album.matching_faces:
                    mimage = self.images[mface.image]
                    thumb = Thumbnail(id_=mimage.id_,container=self.albumimages_panes[album.id_].sframe,image=mimage.getPILimage())
                    thumb.frame.grid(row = i // 5, column = i % 5)
                    sf.members.append(thumb)
                    i += 1

    def scan_albumimage(self,parent):
        ad = Albums_Dialog(parent)
        parent.wait_window(ad.top)
        if(ad.closed):
            file = ad.file_name
            if(file):
                img = Image(0, file)
                fd.scan([img],unload = True)
                self.album_images.append(img)
                for face in img.faces :
                    l = face.location
                    # (top,right,bottom,left) -> (left,top,right,bottom)
                    im = img.getPILimage().crop((l[3],l[0],l[1],l[2]))
                    album = Album(self.__albumcount__, face)
                    album_thumb = Album_Thumbnail(self.__albumcount__, album, self.album_pane.sframe, im,
                                           leftmouse_action=self.album_leftmouse, rightmouse_action=self.album_rightmouse)
                    album_thumb.frame.grid(row=self.__albumcount__, column=0)
                    self.album_thumbnails.append(album_thumb)
                    self.__albumcount__ += 1
                    self.albums.append(album)
                    self.album_pane.members.append(album_thumb)
                    self.root.update()
