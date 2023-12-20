import customtkinter as ctk
from tkinter.simpledialog import askstring
from pssettings import *

class ShapeDrawer:
   def __init__(self, canvas, rectangles, pos_vars):
       self.canvas = canvas
       self.rect = None
       self.start_x = None
       self.start_y = None
       self.rectangles = rectangles
       self.canvas.bind("<ButtonPress-1>", self.on_button_press)
       self.canvas.bind("<B1-Motion>", self.on_move_press)
       self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
       self.pos_vars = pos_vars

   def on_button_press(self, event):
       # Set the starting coordinates for the rectangle
       self.start_x = event.x
       self.start_y = event.y

   def on_move_press(self, event):
       # If a rectangle already exists, delete it
       if self.rect:
           self.canvas.delete(self.rect)

       # Create a new rectangle based on the current mouse position
       curX, curY = (event.x, event.y)
       self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, curX, curY, outline='red', width=2)
       

   def on_button_release(self, event):
        if self.start_x is None or self.start_y is None:
            return
        
        coord1 = [self.start_x, self.start_y]
        coord2 = [event.x, event.y]

        if coord1[0] < coord2[0]:
            left, right = coord1[0], coord2[0]
        else:
            left, right = coord2[0], coord1[0]
    
        if coord1[1] < coord2[1]:
            top, bottom = coord1[1], coord2[1]
        else:
            top, bottom = coord2[1], coord1[1]

        # create a combobox widget
        entry_value = self.open_window()

        self.rect = self.canvas.create_rectangle(left, top, right, bottom, outline='red', width=2)
        self.rectangles.append({"id": self.rect, "conates":(left,top,right,bottom), "class": entry_value})
        self.pos_vars['rectangles'].set(self.rectangles)
        # Reset the starting coordinates and rectangle
        self.start_x = None
        self.start_y = None
        self.rect = None

   def stop_drawing(self):
       self.canvas.unbind("<ButtonPress-1>")
       self.canvas.unbind("<B1-Motion>")
       self.canvas.unbind("<ButtonRelease-1>")

   def open_window(self):
        # create a new window
        ctk.set_appearance_mode('dark')
        window = ctk.CTkToplevel(self.canvas)
        window.title('Select an option')

        # set the topmost attribute to True
        window.wm_attributes('-topmost', True)

        # create a combobox widget
        combobox = ctk.CTkComboBox(window, values=CAPTURE_OPTIONS)
        combobox.pack()

        # create a class variable to store the selected value
        self.selected_value = None

        def submit():
            # get the selected value
            self.selected_value = combobox.get()
            print("Selected value:", self.selected_value)

            # close the window
            window.destroy()

        # create a submit button
        button = ctk.CTkButton(window, text='Submit', command=submit)
        button.pack()

        # set the size and position of the window
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width + 50, height + 50, x, y))

        # bring the new window to the front
        window.lift()

        # wait for the window to be closed
        window.wait_window()

        # return the selected value
        return self.selected_value