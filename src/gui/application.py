'''
Created on 05-April-2021

@author: Aniket Kumar Tripathi
'''

import tkinter as tk
from threading import Thread

from src.engine.base import Image
import src.engine.face_detection as fd
from src.engine.base import Album
import src.engine.image_manager as image_manager

from .helper_widgets import ScrollableFrame
from .helper_widgets import Thumbnail
from .helper_widgets import Album_Thumbnail
from .helper_windows import AlbumsDialog
from .helper_windows import LoadingBar
from .helper_windows import ImageViewer

class Application:

    def __init__(self):
        self.albums = []
        # Images from which albums were created
        self.album_images = []
        # Frame that holds the images corresponding to albums
        self.albumimages_panes = []
        # Holds Thumbnails for albums
        self.album_thumbnails = []
        # Holds all images to be scanned (except th e image from which album
        # was
        # created
        self.images = []
        self.__albumcount__ = 0

        self.root = tk.Tk()
        self.root.title("Face Recognition")
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
        self.add_album_button = tk.Button(self.toolbar, text='Add albums',
                                         command=lambda:self.scan_albumimage(self.root))
        self.add_album_button.grid(row=0, column=0, padx=5)

        self.scan_button = tk.Button(self.toolbar, text='Scan', padx=5,
                                    command=lambda: self.scan_directory(self.root))
        self.scan_button.grid(row=0, column=1, padx=5)

        # Main Pane - album pane and image pane
        self.main_pane = tk.Frame(self.base, bd=1)
        self.main_pane.grid(row=1, column=0, sticky='nsew')
        self.main_pane.grid_columnconfigure(1, weight=1)
        self.main_pane.grid_rowconfigure(0, weight=1)

        # Album container
        self.album_pane = ScrollableFrame(self.main_pane, labelanchor='n', text='Album',
                                         padx=2, pady=2, takefocus=False, relief=tk.SUNKEN, bd=3, width=192)
        self.album_pane.grid_propagate(0)
        self.album_pane.grid_columnconfigure(0, weight=1)
        self.album_pane.grid_rowconfigure(0, weight=1)
        self.album_pane.grid(row=0 , column=0, sticky='nsew')

        # Image container
        self.image_pane = tk.LabelFrame(self.main_pane, labelanchor='n', text='Images',
                                       padx=2, pady=5, relief=tk.SUNKEN,bd=3)
        self.image_pane.grid(row=0, column=1, sticky='nsew')
        self.image_pane.grid_columnconfigure(0, weight=1)
        self.image_pane.grid_rowconfigure(0, weight=1)


        self.root.mainloop()


    def album_leftmouse(self, id_):
        if self.albumimages_panes:
            self.albumimages_panes[id_].tkraise()

    def album_rightmouse(self, id_):
        pass

    def scan_directory(self, parent):
        folder = tk.filedialog.askdirectory() + "/"
        unscanned_images = image_manager.load(folder)
        if unscanned_images:
            class ScanProgress:
                def __init__(self):
                    self.album = None
                    self.album_scancount = 0
                    self.face_detection_complete = False
                    self.face_recognition_complete = False

            sp = ScanProgress()
            self.images += unscanned_images

            def process(scan_progress=sp):
                fd.scan(unscanned_images)
                scan_progress.face_detection_complete = True

                for album in self.albums:
                    scan_progress.album = album
                    album.scan(unscanned_images)
                    scan_progress.album_scancount += 1
                scan_progress.face_recognition_complete = True

            loading_bar = LoadingBar(self.root, "Loading Albums", len(unscanned_images) + len(self.albums))
            albumthread = Thread(target = process)

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
            fd.__reset_count__
            for album in self.albums:
                i = 0
                for mface in album.matching_faces:
                    mimage = self.images[mface.image]
                    thumb = Thumbnail(id_=mimage.id_,container=self.albumimages_panes[album.id_].sframe,image=mimage.get_PIL_image(),
                                     leftmouse_action=lambda id_: ImageViewer(self.root,self.images,current_imageid=id_))
                    thumb.frame.grid(row = i // 5, column = i % 5)
                    self.albumimages_panes[album.id_].members.append(thumb)
                    i += 1

    def scan_albumimage(self,parent):
        adialog = AlbumsDialog(parent)
        parent.wait_window(adialog.top)
        if(adialog.closed):
            file = adialog.file_name
            if(file):
                img = Image(0, file)
                fd.scan([img],unload = True)
                fd.__reset_count__()
                self.album_images.append(img)
                for face in img.faces :
                    loc = face.location
                    # (top,right,bottom,left) -> (left,top,right,bottom)
                    fimg = img.get_PIL_image().crop((loc[3],loc[0],loc[1],loc[2]))
                    album = Album(self.__albumcount__, face)
                    album_thumb = Album_Thumbnail(self.__albumcount__, album, self.album_pane.sframe, fimg,
                                           leftmouse_action=self.album_leftmouse, rightmouse_action=self.album_rightmouse)
                    album_thumb.frame.grid(row=self.__albumcount__, column=0)
                    sframe = ScrollableFrame(self.image_pane)
                    sframe.grid(row=0, column=0, sticky='nsew')
                    sframe.grid_rowconfigure(0, weight=1)
                    sframe.grid_columnconfigure(0, weight=1)
                    self.albumimages_panes.append(sframe)
                    self.album_thumbnails.append(album_thumb)
                    self.__albumcount__ += 1
                    self.albums.append(album)
                    self.album_pane.members.append(album_thumb)
                    self.root.update()
