import customtkinter as ctk
from tkinter.simpledialog import askstring

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

        # Get user input using tkinter dialog
        ctk.set_appearance_mode('dark')
        entry_value = askstring("Entry Box", "Enter a value:")
        print("Entered value:", entry_value)

        self.rect = self.canvas.create_rectangle(left, top, right, bottom, outline='red', width=2)
        self.rectangles.append({"id": self.rect, "conates":(left,top,right,bottom), "class": entry_value})
        self.pos_vars['rectangles'].set(self.rectangles)
        # Reset the starting coordinates and rectangle
        self.start_x = None
        self.start_y = None
        self.rect = None

    #   return self.rectangles

   def stop_drawing(self):
       self.canvas.unbind("<ButtonPress-1>")
       self.canvas.unbind("<B1-Motion>")
       self.canvas.unbind("<ButtonRelease-1>")
       
