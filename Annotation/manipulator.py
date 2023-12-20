class ShapeMan:
   def __init__(self, canvas, rectangles):
       self.canvas = canvas
       self.rect = None
       self.start_x = None
       self.start_y = None
       self.rectangles = rectangles
       self.canvas.bind("<ButtonPress-1>", self.on_button_press)
       self.canvas.bind("<B1-Motion>", self.on_move_press)
       self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
    

   def on_button_press(self, event):
       # Set the starting coordinates for the rectangle
       self.start_x = event.x
       self.start_y = event.y


       for i,coords in enumerate(self.rectangles):
           if ((coords["conates"][0] < self.start_x < coords["conates"][2]) and ((self.start_y - 5 <= coords["conates"][1] <= self.start_y + 5) or (self.start_y - 5 <= coords["conates"][3] <= self.start_y + 5))):
               # Change the color of the clicked rectangle to red
               self.canvas.itemconfig(coords["id"], outline='blue')
               
           if ((coords["conates"][1] < self.start_y < coords["conates"][3]) and ((self.start_x - 5 <= coords["conates"][0] <= self.start_x + 5) or (self.start_x - 5 <= coords["conates"][2] <= self.start_x + 5))):
               # Change the color of the clicked rectangle to red
               self.canvas.itemconfig(coords["id"], outline='blue')

               
   def on_move_press(self, event):
       print("do nothing")

   def on_button_release(self, event):
       print("test")

   def stop_hand(self):
       self.canvas.unbind("<ButtonPress-1>")
       self.canvas.unbind("<B1-Motion>")
       self.canvas.unbind("<ButtonRelease-1>")


       
