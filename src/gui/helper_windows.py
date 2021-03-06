'''
Created on 08-April-2021

@author: Aniket Kumar Tripathi
'''

import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import filedialog as fd

from PIL import Image, ImageTk

class AlbumsDialog:

	def __init__(self, parent):
		self.top = tk.Toplevel(parent, takefocus=False)
		self.top.grab_set()
		self.top.geometry('520x620')
		self.top.lift(aboveThis=parent)
		self.top.title('Select Album')
		self.top.grid_rowconfigure(0, weight=1)
		self.top.grid_columnconfigure(0, weight=1)

		self.file_name = None
		self.loaded_image = None
		self.image_width = 480
		self.image_height = 480
		self.closed = False

		# Base frame for dialog
		self.base = tk.Frame(self.top, pady=2, padx=2)
		self.base.grid(row=0, column=0, sticky='nsew')
		self.base.grid_columnconfigure(0, weight=1)
		self.base.grid_rowconfigure(0, weight=1)

		# Image Viewer
		self.image_frame = tk.Frame(self.base, padx=4, pady=4, relief=tk.RIDGE, width=self.image_width, height=self.image_height, bd=3)
		self.image_frame.grid(row=0,column=0, sticky='nsew')
		self.image_label = tk.Label(self.image_frame)
		self.image_label.grid(row=0,column=0, padx=5, pady=5)

		# Buttons container
		self.buttons_frame = tk.Frame(self.base, padx=5, pady=5, relief=tk.GROOVE, bd=3)
		self.buttons_frame.grid(row=1, column=0, sticky='ew')
		self.buttons_frame.grid_columnconfigure(1, weight=1)
		self.buttons_frame.grid_rowconfigure((0,1), weight=1)

		# Select file Button
		self.loadfile_button = tk.Button(self.buttons_frame, text='Select File', command=self.__getfile__)
		self.loadfile_button.grid(row=0, column=0, sticky='w')

		# Selected file label
		self.selectedfile_label = tk.Label(self.buttons_frame, text='No File Selected', wraplength=360, justify='left')
		self.selectedfile_label.grid(row=0, column=1,sticky='ew')

		# Load button
		self.load_button = tk.Button(self.buttons_frame, text='Load', command= self.__update_imagelabel__)
		self.load_button.grid(row=0, column=2, sticky='e')

		# Ok button
		self.ok_button = tk.Button(self.buttons_frame, text='OK', command=self.__ok__)
		self.ok_button.grid(row=1, column=0, sticky='w')

		# Cancel button
		self.cancel_button = tk.Button(self.buttons_frame, text='Cancel', command=self.__cancel__)
		self.cancel_button.grid(row=1, column=2, sticky='e')

		# Add action to buttons
		self.loadfile_button.command = tk

	def __ok__(self):
		self.top.grab_release()
		self.top.destroy()
		self.closed = True


	def __cancel__(self):
		self.top.grab_release()
		self.top.destroy()
		self.closed = True
		self.file_name = None

	def __getfile__(self):
		formats = [("JPG", "*.jpg"), ("JPEG", "*.jpeg"), ("PNG", "*.png"), ("BMP", "*.bmp")]
		self.file_name = fd.askopenfilename(parent=self.top, title='Select Image File', filetypes=formats)
		self.__update_selectfilelabel__()

	def  __update_selectfilelabel__(self):
		if(not self.file_name):
			self.selectedfile_label.config(text='No File Selected')
		else:
			self.selectedfile_label.config(text=self.file_name)

	def __update_imagelabel__(self):
		if(self.file_name):
			self.loaded_image = ImageTk.PhotoImage(Image.open(self.file_name)
								.resize((self.image_height,self.image_width)))
			self.image_label.config(image=self.loaded_image)

class LoadingBar:

	def __init__(self,parent,title, max_value):
		self.parent = parent
		self.root = tk.Toplevel(parent)
		self.root.lift(aboveThis=parent)
		self.root.grab_set()
		self.root.title(title)
		self.root.geometry('512x64')
		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_columnconfigure(0, weight=1)
		self.root.update_idletasks()
		self.value = 0
		self.text = 'Loading ... '

		frame = tk.Frame(self.root, padx=3, pady=3, relief = tk.RIDGE)
		frame.grid(row=0, column=0, sticky='nsew')
		frame.grid_columnconfigure(0, weight=1)

		self.text_label = tk.Label(frame, text=self.text, anchor='n')
		self.text_label.grid(row=0,column=0, sticky='ew')

		self.progressbar = Progressbar(frame, mode='determinate', orient=tk.HORIZONTAL, maximum=max_value)
		self.progressbar.grid(row=1, column=0, sticky ='ew')
		self.max = max_value
		self.progressbar["value"] = self.value
		self.completed = False
		self.update_function = None

	def start(self, update_function):
		self.update_function = update_function
		self.completed = False
		self.value = 0
		self.progressbar["value"] = self.value
		self.update()

	def update(self):
		self.update_function()
		if not self.completed :
			if self.value >= self.max :
				self.completed = True
			self.progressbar["value"] = self.value
			self.root.after(100, self.update)
			self.text_label.config(text=self.text)
		else :
			self.root.grab_release()
			self.root.destroy()

class ImageViewer:

	def __init__(self, parent, images, current_imageid=0):
		self.root = tk.Toplevel(parent, takefocus=False)
		self.root.grab_set()
		self.root.lift(aboveThis=parent)
		self.root.title('Image Viewer')
		self.root.state('zoomed')
		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_columnconfigure(0, weight=1)

		self.frame = tk.Frame(self.root)
		self.frame.grid(row=0, column=0, sticky='nsew')
		self.frame.grid_columnconfigure(0, weight=1)
		self.frame.grid_rowconfigure(0, weight=1)
		self.current = current_imageid
		self.image = None

		# Insert image here
		self.canvas = tk.Canvas(self.frame, bd=3, relief=tk.RIDGE)
		self.canvas.grid(row=0, column=0, sticky='nsew')
		img = images[self.current]
		self.addto_canvas(img)

		self.toolbar = tk.Frame(self.frame, bd=3, relief=tk.GROOVE, height=50)
		self.toolbar.grid(row=1, column=0)
		self.toolbar.grid_rowconfigure(0, weight=1)
		self.next_button = tk.Button(self.toolbar, text='NEXT', anchor='n',
							  command=lambda : self.traverse_images(images,+1))
		self.next_button.grid(row = 0,column = 1, padx=5, pady=2)
		self.previous_buttoon = tk.Button(self.toolbar, text='PREVIOUS',
								   command=lambda : self.traverse_images(images,-1))
		self.previous_buttoon.grid(row=0, column=0, padx=5, pady=2)

	def traverse_images(self, imgs, step):
		if 0 <= self.current + step < len(imgs):
			self.current = self.current + step
			img = imgs[self.current]
			self.canvas.delete('all')
			self.addto_canvas(img)


	def addto_canvas(self, img):
		self.image = ImageTk.PhotoImage(img.get_PIL_image())
		self.root.update()
		cw = self.canvas.winfo_width()
		ch = self.canvas.winfo_height()
		iw = self.image.width()
		ih = self.image.height()
		self.canvas.create_image(cw / 2, ch / 2, image=self.image, anchor=tk.CENTER)
		for face in img.faces:
			if face.recognized:
				self.create_labelled_rect(face,x=(cw - iw) / 2, y=(ch - ih) / 2)


	def create_labelled_rect(self,face, x, y):
		if face.recognized:
			album = face.album
			loc = face.location
			# (top,right,bottom,left) - > (left, top, right+1, bottom+1)
			self.canvas.create_rectangle(x + loc[3], y + loc[0], x + loc[1] + 1, y + loc[2] + 1, outline='lime', width=2)
			self.canvas.create_text(x + (loc[3] + loc[1]) / 2, y + loc[2], text=album.name, anchor='n',
						  font = ('Times', '20', 'bold'), fill='lime', state=tk.DISABLED)
