'''
Created on 05-April-2021

@author: Aniket Kumar Tripathi
'''

import tkinter as tk
from src.gui.albums_dialog import Albums_Dialog

def main():
    root = tk.Tk()
    root.title("Face Recognition")
    root.geometry('1024x768')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.state('zoomed')

    # Base container - containes 2 children - toolbar and main pane
    base = tk.Frame(root, pady=5)
    base.grid(row=0, column=0, sticky='nsew')
    base.grid_columnconfigure(0, weight=1)
    base.grid_rowconfigure(1, weight=1)

    # Toolbar container
    toolbar_height = 50
    xpad_t = 10
    ypad_t = 5
    toolbar = tk.Frame(base, padx=xpad_t, pady=ypad_t, relief=tk.GROOVE, bd=5, height=toolbar_height)
    toolbar.grid(row=0, column=0, sticky='nsew')
    add_album_button = tk.Button(toolbar, text='Add albums', command=lambda:Albums_Dialog(root))
    add_album_button.grid(row=0, column=0)

    # Main Pane - album pane and image pane
    main_pane = tk.Frame(base, bd=1)
    main_pane.grid(row=1, column=0, sticky='nsew')
    main_pane.grid_columnconfigure(0, weight=1)
    main_pane.grid_columnconfigure(1, weight=5)
    main_pane.grid_rowconfigure(0, weight=1)

    # Album container
    xpad_a = 2
    ypad_a = 5
    album_pane = tk.LabelFrame(main_pane, labelanchor='n', text='Album', padx=xpad_a, pady=ypad_a, relief=tk.RIDGE, bd=3)
    album_pane.grid_columnconfigure(0, weight=1)
    album_pane.grid(row=0, column=0, sticky='nsew')

    # Image container
    xpad_i = 2
    ypad_i = 5
    image_pane = tk.LabelFrame(main_pane, labelanchor='n', text='Images', padx=xpad_i, pady=ypad_i, relief=tk.RIDGE,bd=3)
    image_pane.grid(row=0, column=1, sticky='nsew')
    image_pane.grid_columnconfigure(0, weight=1)


    root.mainloop()

