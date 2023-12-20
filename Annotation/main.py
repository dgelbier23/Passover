import customtkinter as ctk 
from image_widgets import *
from PIL import Image, ImageTk,ImageOps, ImageEnhance, ImageFilter
from menu import Menu
import cv2
from drawer import ShapeDrawer
from manipulator import ShapeMan
from scissor import ScissorMan
from pssettings import *
import universal 


class App(ctk.CTk):
    
    def __init__(self):
        #setup
        super().__init__() 
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600')
        self.title('Photo Editor')
        self.minsize(800,500)
        self.init_parameters()

        # maximize the window
        self.attributes('-fullscreen', True)

        # layout
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 2, uniform = 'a')
        self.columnconfigure(1, weight = 6, uniform = 'a')

        #CANVAS DATA
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        # widgets
        # importButton (frame with button)
        self.image_import = ImageImport(self,self.import_image)

        # run
        self.mainloop()

    def init_parameters(self):
        self.pos_vars = {
            'rotate':ctk.DoubleVar(value = ROTATE_DEFAULT),
            'zoom': ctk.DoubleVar(value = ZOOM_DEFAULT),
            'tool': ctk.StringVar(value = TOOL_OPTIONS[0]),
            'rectangles': ctk.StringVar(value = RECTANGLES_DEFAULT)
        }

        self.color_vars = {
            'brightness': ctk.DoubleVar(value = BRIGHTNESS_DEFAULT),
            'grayscale': ctk.BooleanVar(value = GRAYSCALE_DEFAULT),
            'invert': ctk.BooleanVar(value = INVERT_DEFAULT),
            'vibrance' :ctk.DoubleVar(value = VIBRANCE_DEFAULT)
        }

        self.effect_vars = {
            'blur': ctk.DoubleVar(value = BLUR_DEFAULT),
            'contrast': ctk.IntVar(value = CONTRAST_DEFAULT),
            'effect': ctk.StringVar(value = EFFECT_OPTIONS[0])
        }
        
        # tracing 
        combined_vars = list(self.pos_vars.values()) + list(self.color_vars.values()) + list(self.effect_vars.values())
        for var in combined_vars:
            var.trace('w', self.manipulate_image)


    def manipulate_image(self, *args):
        self.image = self.original
        
        #rotaate
        if self.pos_vars['rotate'].get() != ROTATE_DEFAULT:
            self.image = self.image.rotate(self.pos_vars['rotate'].get())

        # ZOOM
        if self.pos_vars['zoom'].get() != ZOOM_DEFAULT:
            self.image = ImageOps.crop(image = self.image, border = self.pos_vars['zoom'].get())

        # tool
        if self.pos_vars['tool'].get() != TOOL_OPTIONS[0]:
            if self.pos_vars['tool'].get() == 'Draw':
                self.drawShape()
            if self.pos_vars['tool'].get() == 'Hand':
                self.moveShape()
            if self.pos_vars['tool'].get() == 'Scissor':
                self.deleteShape()

        # Rectangles
        self.pos_vars['rectangles'].set(self.coords)

        print('Pos vas')
        print(self.pos_vars)

        # brightness & vibrance
        if self.color_vars['brightness'].get() != BRIGHTNESS_DEFAULT:
            brightness_enhancer = ImageEnhance.Brightness(self.image)
            self.image = brightness_enhancer.enhance(self.color_vars['brightness'].get())

        if self.color_vars['vibrance'].get() != VIBRANCE_DEFAULT:
            vibrance_enhancer = ImageEnhance.Color(self.image)
            self.image = vibrance_enhancer.enhance(self.color_vars['vibrance'].get())

        #colors : grayscale and invert#
        if self.color_vars['grayscale'].get():
            self.image = ImageOps.grayscale(self.image)

        if self.color_vars['invert'].get():
            self.image = ImageOps.invert(self.image)

        #blur and contrast
        if self.effect_vars['blur'].get() != BLUR_DEFAULT:
            self.image = self.image.filter(ImageFilter.GaussianBlur(self.effect_vars['blur'].get()))
        if self.effect_vars['contrast'].get() != CONTRAST_DEFAULT:
            self.image = self.image.filter(ImageFilter.UnsharpMask(self.effect_vars['contrast'].get()))
        
        if self.effect_vars['effect'].get() == 'Emboss':
            self.image = self.image.filter(ImageFilter.EMBOSS)

        #
        if self.effect_vars['effect'].get() == 'Find Edges':
            self.image = self.image.filter(ImageFilter.FIND_EDGES)

        #
        if self.effect_vars['effect'].get() == 'Contour':
            self.image = self.image.filter(ImageFilter.CONTOUR)
        #
        if self.effect_vars['effect'].get() == 'Edge enhance':
            self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        #

        self.place_image()

    def drawShape(self):
        try:
            self.scissors.stop_scissoring()
        except:
            print("no scissor")
        try:
            self.manipulator.stop_hand()
        except:
            print("no mani")

        self.drawer = ShapeDrawer(self.image_output, self.coords, self.pos_vars)
        
    def moveShape(self):
        # Stop drawing
        try:
            self.drawer.stop_drawing()
        except:
            print("no draw")

        # Know where the user has clicked
        self.manipulator = ShapeMan(self.image_output, self.coords)
        # If on rectangle, highlight rectangle
        #   Able to resize, and delete rectagle  

    def deleteShape(self):
        # Stop drawing
        try:
            self.drawer.stop_drawing()
        except:
            print("no draw")
        try:
            self.manipulator.stop_hand()
        except:
            print("no man")


        # Know where the user has clicked
        self.scissors = ScissorMan(self.image_output, self.coords, self.pos_vars)
        # If on rectangle, highlight rectangle
        #   Able to resize, and delete rectagle  


    def import_image(self,path):
        # go back to none tool
        self.pos_vars['tool'].set(TOOL_OPTIONS[0])

        self.original = Image.open(path)
        self.image = self.original
        self.image_ratio = self.image.size[0] / self.image.size[1]          # width / height
        self.coords = []                                                    # change to make different file on upload 

        self.image_tk = ImageTk.PhotoImage(self.image)

        # Store the image raio and the sizes:
        universal.setImageHeight(self.image.size[1])
        universal.setImageWidth(self.image.size[0])
        
        #hide imageImport widget
        self.image_import.grid_forget()
        self.image_output = ImageOutput(self, self.resize_image)
        self.close_button = CloseOutput(self, self.close_edit, path)
        self.menu = Menu(self,self.pos_vars, self.color_vars, self.effect_vars, path)      


    def close_edit(self):
        # make the file for edited images
        if (len(self.coords) != 0):
            file_name = os.path.splitext(os.path.basename(self.close_button.path))[0] 
            var = self.coords
            with open('./02_edited_images/' + file_name + '.txt', 'w') as file:
                print(f'{file_name}: {var}', file=file)

        # hide the image and then close button
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu.grid_forget()
        # recreate the import button
        self.image_import = ImageImport(self, self.import_image)

    def resize_image(self, event):
        # current canvas ratio
        canvas_ratio = event.width / event.height

        # update canvas attributes
        self.canvas_width = event.width
        self.canvas_height = event.height

        # resize
        # need to know aspect ratio of image and of canvas
        if canvas_ratio > self.image_ratio: # canvas is wider than image
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
            self.scale = self.image_height / self.image.size[1] 
        else: # canvas is taller than image
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)
            self.scale = self.image_width / self.image.size[0] 

        universal.setScaleRatio(self.scale)
        
        self.place_image()

    def place_image(self):
        print(self.coords)
        # place image
        self.image_output.delete('all')
        resized_image = self.image.resize((self.image_width,self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        # creates and decides center maybe best for zooming in random places
        self.image_output.create_image(self.canvas_width / 2, self.canvas_height / 2, image = self.image_tk)
        self.redraw_rectangles()

    def redraw_rectangles(self):
        self.passover = []

        for rec in self.coords:
            self.rect = self.image_output.create_rectangle(rec["conates"][0],rec["conates"][1],rec["conates"][2],rec["conates"][3], outline ='red', width=2)
            self.passover.append({"id": self.rect, "conates":(rec["conates"][0],rec["conates"][1],rec["conates"][2],rec["conates"][3]), "class": rec["class"]})

        self.coords.extend(self.passover)

        seen_values = set()
        for i in range(len(self.coords) - 1, -1, -1):
            if self.coords[i]["conates"] in seen_values:
                del self.coords[i]
            else:
                seen_values.add(self.coords[i]["conates"])
App()