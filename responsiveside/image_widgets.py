import customtkinter as ctk
from tkinter import filedialog,Canvas
from pssettings import *
import glob, os
from PIL import Image,ImageOps, ImageTk

class ImageImport(ctk.CTkFrame):
    def __init__(self,parent, import_func):
        super().__init__(master = parent)
        self.grid(column = 0, columnspan = 2, row = 0, sticky = 'nsew')
        self.import_func = import_func
        self.button_images = [] # list to store the button images

        # Add a title label
        self.title_label = ctk.CTkLabel(self, text="Image Selection", font=("Arial", 36))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)  # Span across all columns, add some padding

        self.createImageList()
        self.configureGrid()
        self.createButtons()

    def configureGrid(self):
        # Configure grid to have 3 columns with even weight
        self.columnconfigure(0, weight= 1)
        self.columnconfigure(1, weight= 1)
        self.columnconfigure(2, weight= 1)

    def createImageList(self):
        # populate list for image values
        for infile in glob.glob("01_base_images\\*.jpg"):
            with Image.open(infile) as im:
                im = ImageOps.fit(im, (80, 80)).convert("RGBA")
                ima = ImageTk.PhotoImage(im)
                name = os.path.basename(infile)
                self.button_images.append({'image':ima,'filename':name,'filepath':infile, 'status': self.generateStatus(os.path.basename(infile))}) # add image to the list, with 3 values; image,name,filepath

    def generateStatus(self, name):
        name = os.path.splitext(name)[0] + '.txt' # name of image
        try:
            for infile in glob.glob("03_complete_images\\*.txt"): # check done images
                if name in os.path.basename(infile):
                    return BUTTON_COMPLETE
            for infile in glob.glob("02_edited_images\\*.txt"): # check edited images
                if name in os.path.basename(infile):
                    return BUTTON_EDIT
        except:
            print('No edited files!')
        return BUTTON_BASE # all other case return blue

    def createButtons(self):
        # Initialize counters for each column
        col_counters = {BUTTON_BASE: 0, BUTTON_EDIT: 0, BUTTON_COMPLETE: 0}

        # Determine the column index for each button type
        col_indices = {BUTTON_BASE: 0, BUTTON_EDIT: 1, BUTTON_COMPLETE: 2}

        for ima in self.button_images:
            # Determine the column and row for the current button
            col = col_indices[ima['status']]
            row = 1 + col_counters[ima['status']] * 2

            # Create and place the button
            ctk.CTkButton(self, text=None, image=ima['image'],
                          command=lambda p=ima['filepath']: self.import_func(p),
                          fg_color=ima['status'],hover_color='grey30').grid(row=row, column=col)
            ctk.CTkLabel(self,text = ima['filename']).grid(row=row + 1, column=col)

            # Increment the row counter for this column
            col_counters[ima['status']] += 1

class ImageOutput(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(master = parent, background = BACKGROUND_COLOR , bd = 0, highlightthickness = 0, relief = 'ridge')
        self.grid(row = 0, column = 1, sticky = 'nsew', padx = 10, pady = 10)
        self.bind('<Configure>', resize_image)

class CloseOutput(ctk.CTkButton):
    def __init__(self, parent,close_func):
        super().__init__(
            master = parent,
            command = close_func,
            text = 'x',
            text_color=WHITE,
            fg_color='transparent',
            width = 40, height = 40,
            corner_radius = 0,
            hover_color = CLOSE_RED)
        self.place(relx = 0.99, rely = 0.01, anchor = 'ne')