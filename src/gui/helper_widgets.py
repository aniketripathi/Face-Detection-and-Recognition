'''
Created on 08-April-2021

@author: Aniket Kumar Tripathi
'''

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

class ScrollableFrame(tk.LabelFrame):
    members = []
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, bd=-2)
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.sframe = tk.Frame(canvas,)
        self.sframe.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.sframe, anchor='n')
        canvas.configure(yscrollcommand=scrollbar.set)
        self.sframe.grid_columnconfigure(0,weight=1)



class Thumbnail:

   def __init__(self,id, container, image, leftmouse_action=None, rightmouse_action=None):
       self.id = id
       self.frame = tk.Frame(container, bg='black', highlightthickness=1, padx=3, pady=3, takefocus=1)
       self.frame.bind("<Enter>", lambda event, f=self.frame: f.configure(bg='red'))
       self.frame.bind("<Leave>", lambda event, f=self.frame: f.configure(bg='black'))
       self.frame.grid_rowconfigure(0, weight = 1)
       self.frame.grid_columnconfigure(0, weight=1)
       self.thumb = ImageTk.PhotoImage(image.resize([128,128]))
       self.label = tk.Label(self.frame, image = self.thumb)
       if leftmouse_action :
           self.label.bind("<Button-1>", lambda event : leftmouse_action(id=self.id))
       if rightmouse_action :
           self.label.bind("<Button-2>", lambda event : rightmouse_action(id=self.id))
       self.label.grid(row = 0, column = 0, sticky = 'nsew')
       self.frame.grid(padx=5, pady=5)
