'''
Created on 08-April-2021

@author: Aniket Kumar Tripathi
'''

import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk

class ScrollableFrame(tk.LabelFrame):

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.members = []
        canvas = tk.Canvas(self, bd=-2, highlightthicknes=0)
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.sframe = tk.Frame(canvas, bd=0, highlightthickness=0)
        self.sframe.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.sframe, anchor='n')
        canvas.configure(yscrollcommand=scrollbar.set)
        self.sframe.grid_columnconfigure(0,weight=1)



class Thumbnail:

    def __init__(self,id_, container, image, leftmouse_action=None, rightmouse_action=None):
        self.id_ = id_
        self.frame = tk.Frame(container, bg='black', highlightthickness=1, padx=3, pady=3, takefocus=1)
        self.frame.bind("<Enter>", lambda event, f=self.frame: f.configure(bg='red'))
        self.frame.bind("<Leave>", lambda event, f=self.frame: f.configure(bg='black'))
        self.frame.grid_rowconfigure(0, weight = 1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.thumb = ImageTk.PhotoImage(image.resize([128,128]))
        self.label = tk.Label(self.frame, image = self.thumb)
        if leftmouse_action :
            self.label.bind("<Button-1>", lambda event : leftmouse_action(id_=self.id_))
        if rightmouse_action :
            self.label.bind("<Button-2>", lambda event : rightmouse_action(id_=self.id_))
        self.label.grid(row=0, column=0, sticky = 'nsew')
        self.frame.grid(padx=5, pady=5)


class Album_Thumbnail(Thumbnail):

    def __init__(self, id_, album, container, image, leftmouse_action=None, rightmouse_action=None):
        super().__init__(id_, container, image, leftmouse_action, rightmouse_action)
        self.album = album
        self.text_widget = tk.Text(self.frame, bd=3, height=1, width=10, wrap=tk.WORD)
        self.text_widget.grid(row=1, column=0, pady=3)
        self.text_widget.insert('1.0', album.name)
        def update_text():
            self.text_widget.config(state=tk.DISABLED)
            text = self.text_widget.get('1.0', tk.END)
            album.name = text
        self.text_widget.bind("<Button-1>", lambda event, w=self.text_widget: w.config(state=tk.NORMAL))
        self.text_widget.bind("<Key-Return>", lambda event : update_text())
        self.text_widget.bind("<FocusOut>", lambda event : update_text())