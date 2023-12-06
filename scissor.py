class ScissorMan:
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

       spec_coords = []

    #    for rectangle_id in self.rectangles:
    #     coords = self.canvas.coords(rectangle_id)
    #     if self.start_x == coords[0] and self.start_y == coords[1]:
    #        # Delete the rectangle from the canvas
    #        self.canvas.delete(rectangle_id)
    #        break

       for i,coords in enumerate(self.rectangles):
        #    if ((coords["conates"][0]<self.start_x and self.start_x < coords["conates"][2]) and (self.start_y == coords["conates"][1] or self.start_y == coords["conates"][3])):
           if ((coords["conates"][0] < self.start_x < coords["conates"][2]) and ((self.start_y - 5 <= coords["conates"][1] <= self.start_y + 5) or (self.start_y - 5 <= coords["conates"][3] <= self.start_y + 5))):
               print("on x rectangle")
               print(coords["conates"])
               spec_coords = coords["conates"]
               # Change the color of the clicked rectangle to red
            #    self.canvas.itemconfig(coords["id"], state='hidden')
               self.canvas.delete(coords["id"])
               self.rectangles.pop(i)
               
        #    if ((coords["conates"][1]<=self.start_y and self.start_y <= coords["conates"][3]) and (self.start_x == coords["conates"][0] or self.start_x == coords["conates"][2])):
           if ((coords["conates"][1] < self.start_y < coords["conates"][3]) and ((self.start_x - 5 <= coords["conates"][0] <= self.start_x + 5) or (self.start_x - 5 <= coords["conates"][2] <= self.start_x + 5))):
               print("on y rectangle")
               print(coords["conates"])
               spec_coords = coords["conates"]
               # Change the color of the clicked rectangle to red
            #    self.canvas.itemconfig(coords["id"], state='hidden')
               self.canvas.delete(coords["id"])
               self.rectangles.pop(i)

    
       print(spec_coords)
               

   def on_move_press(self, event):
       print("do nothing")


       # If a rectangle already exists, delete it
    #    if self.rect:
    #        self.canvas.delete(self.rect)

    #    # Create a new rectangle based on the current mouse position
    #    curX, curY = (event.x, event.y)
    #    self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, curX, curY, outline='red', width=2)

   def on_button_release(self, event):
       print("test")

   def stop_scissoring(self):
       self.canvas.unbind("<ButtonPress-1>")
       self.canvas.unbind("<B1-Motion>")
       self.canvas.unbind("<ButtonRelease-1>")
