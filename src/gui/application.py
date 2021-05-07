'''
Created on 05-April-2021

@author: Aniket Kumar Tripathi
'''

import tkinter as tk
from tkinter.ttk import Progressbar as pb
from PIL import Image as pImage, ImageTk

from .helper_widgets import ScrollableFrame
from .helper_widgets import Thumbnail
from .helper_windows import Albums_Dialog
from src.engine.base import Image
import src.engine.face_detection as fd


class Application:
    albums = set()
    album_images = set()

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Face Recognition")
        self.root.geometry('1024x768')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.state('zoomed')

        # self.base container - containes 2 children - self.toolbar and main
        # pane
        self.base = tk.Frame(self.root, pady=5, takefocus=1)
        self.base.grid(row=0, column=0, sticky='nsew')
        self.base.grid_columnconfigure(0, weight=1)
        self.base.grid_rowconfigure(1, weight=1)

        # self.toolbar container
        self.toolbar_height = 50
        xpad_t = 10
        ypad_t = 5
        self.toolbar = tk.Frame(self.base, padx=xpad_t, pady=ypad_t, relief=tk.GROOVE, bd=5, height=self.toolbar_height)
        self.toolbar.grid(row=0, column=0, sticky='nsew')
        self.add_album_button = tk.Button(self.toolbar, text='Add albums', command=lambda:self.scan_albumimage(self.root))
        self.add_album_button.grid(row = 0, column = 0)

        # Main Pane - album pane and image pane
        self.main_pane = tk.Frame(self.base, bd=1, takefocus=1)
        self.main_pane.grid(row = 1, column = 0, sticky = 'nsew')
        self.main_pane.grid_columnconfigure(1, weight = 1)
        self.main_pane.grid_rowconfigure(0, weight=1)

        # Album container
        xpad_a = 2
        ypad_a = 2
        self.album_pane = ScrollableFrame(self.main_pane, labelanchor = 'n', text = 'Album', padx = xpad_a, pady = ypad_a, relief = tk.SUNKEN, bd = 3, takefocus=1, width=192)
        self.album_pane.grid_propagate(0)
        self.album_pane.grid_columnconfigure(0, weight=1)
        self.album_pane.grid_rowconfigure(0, weight=1)
        self.album_pane.grid(row = 0, column = 0, sticky = 'nsew')

        # Image container
        xpad_i = 2
        ypad_i = 5
        self.image_pane = tk.LabelFrame(self.main_pane, labelanchor='n', text='Images', padx=xpad_i, pady=ypad_i, relief=tk.SUNKEN,bd=3)
        self.image_pane.grid(row = 0, column = 1, sticky = 'nsew')
        self.image_pane.grid_columnconfigure(0, weight=1)


        self.root.mainloop()


    def scan_albumimage(self,parent):

        ad = Albums_Dialog(parent)
        parent.wait_window(ad.top)
        if(ad.closed):
            file = ad.file_name
            if(file):
                img = Image(0, file)
                fd.scan([img],unload=True)
                self.albums.update(img.faces)
                i = 0
                for face in self.albums :
                    l = face.location
                    print(l)
                    # (top,right,bottom,left) -> (left,top,right,bottom)
                    im = pImage.open(img.location).crop((l[3],l[0],l[1],l[2]))
                    canvas = tk.Canvas(self.root)
                    album_img = Thumbnail(self.album_pane.sframe,image=im)
                    album_img.frame.grid(row=i, column=0)
                    i += 1
                    self.album_images.add(album_img)
                    self.root.update()
