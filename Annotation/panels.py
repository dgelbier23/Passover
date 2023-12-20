import customtkinter as ctk
from pssettings import *
import os 
import ast
import universal

class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = DARK_GREY)
        self.pack(fill='x',pady=4,ipady=8)


class SliderPanel(Panel):
    def __init__(self, parent, text, data_var, min_value, max_value):
        super().__init__(parent = parent)

        #layout
        self.rowconfigure((0,1), weight = 1)
        self.columnconfigure((0,1), weight = 1)

        self.data_var = data_var
        self.data_var.trace('w',self.update_text)

        ctk.CTkLabel(self, text = text).grid(column = 0, row = 0, sticky = 'W',padx = 10) # topleft
        self.num_label = ctk.CTkLabel(self,text = data_var.get())
        self.num_label.grid(column = 1, row = 0, sticky = 'E', padx = 10) #topright
        ctk.CTkSlider(self,fg_color = SLIDER_BG,
                       variable = self.data_var,
                       from_ = min_value,
                       to = max_value
                       ).grid(row = 1, column = 0, columnspan = 2, sticky = 'ew', padx = 5, pady =5)
        # ctk.CTkLabel(self, text = text).pack()

    def update_text(self,*args):
        self.num_label.configure(text = f'{round(self.data_var.get(),2)}')

class SegmentPanel(Panel):
    def __init__(self,parent, text,data_var,options):
        super().__init__(parent = parent)

        ctk.CTkLabel(self,text = text).pack()
        ctk.CTkSegmentedButton(self,variable = data_var,values=options).pack(expand=True,fill='both',padx=4,pady=4)


class SwitchPanel(Panel):
    def __init__(self, parent, *args):
        super().__init__(parent = parent)

        for var, text in args:
            switch = ctk.CTkSwitch(self, text = text, variable = var, button_color = BLUE, fg_color = SLIDER_BG)
            switch.pack(side = 'left',expand = True, fill = 'both', padx = 5, pady = 5)


class DropDownPanel(ctk.CTkOptionMenu):
    def __init__(self, parent, data_var, options):
        super().__init__(
            master = parent,
            values = options,
            fg_color = DARK_GREY,
            button_color = DROPDOWN_MAIN_COLOR,
            button_hover_color = DROPDOWN_HOVER_COLOR,
            dropdown_fg_color = DROPDOWN_MENU_COLOR,
            variable = data_var
            )
        self.pack(fill='x',pady = 4)

class RevertButton(ctk.CTkButton):
    def __init__(self, parent, filename, coords):
        super().__init__(master = parent, text = 'Save', command = self.revert)
        self.pack(side='bottom', pady=10)
        self.filename = filename
        self.coords = coords
        
    def convert_coordinates_to_yolo(image_width, image_height, box):
        """
        Convert coordinates of bounded boxes to YOLO form.

        Parameters:
            image_width (int): Width of the image.
            image_height (int): Height of the image.
            box (tuple): Tuple containing the coordinates of the bounded box in the format (x_min, y_min, x_max, y_max).

        Returns:
            tuple: Tuple containing the coordinates of the bounded box in YOLO format (x_center, y_center, width, height).
        """
        x_min, y_min, x_max, y_max = box
        x_center = (x_min + x_max) / 2 / image_width
        y_center = (y_min + y_max) / 2 / image_height
        width = (x_max - x_min) / image_width
        height = (y_max - y_min) / image_height
        
        print("x_center:", x_center)
        print("y_center:", y_center)
        print("width:", width)
        print("height:", height)

        return x_center, y_center, width, height
    

    def convert_input_string(self,input_string):
        # Remove the surrounding double quotes and split the string into individual dictionary strings

        id_count = input_string.count('id')
        print("Number of times 'id' appears in the beginning string:", id_count)
        coordinates_class_list = []
        if id_count > 1:
                
                dict_strings = input_string[2:-2].split('", "')
        else:
                dict_strings = input_string[2:-3].split('", "')
            # Create a list to store the dictionaries
        data_list = []
        print(dict_strings)
        # Process each dictionary string
        for d in dict_strings:
            print(d)
            # Convert the string to a dictionary
            d = ast.literal_eval(d)
            data_list.append(d)

        print(data_list)

        for d in data_list:
            coordinates_class_dict = {}
            coordinates_class_dict['conates'] = d['conates']
            coordinates_class_dict['class'] = d['class']
            coordinates_class_list.append(coordinates_class_dict)

        return coordinates_class_list

    def rescaleBoundingBox(self, boundingBox, imageWidth, imageHeight, imageRatio):
        # Extract the coordinates of the bounding box
        x1, y1, x2, y2 = boundingBox

        # Calculate the new dimensions of the bounding box
        newWidth = (x2 - x1) / imageRatio
        newHeight = (y2 - y1) / imageRatio

        # Calculate scaling factors
        widthScale = newWidth / imageWidth
        heightScale = newHeight / imageHeight

        # Calculate scaled centrepoint
        # Calculate scaled center point
        centerX = (x1 + x2) / 2 / imageRatio / imageWidth
        centerY = (y1 + y2) / 2 / imageRatio / imageHeight

        return (centerX, centerY, widthScale, heightScale)

    def revert(self):
        var = self.coords.get()
        print("This is where i change the math")

        print(var)            
        data_list = self.convert_input_string(var)
        print(data_list)
        print(data_list[0]['conates'])
        print(data_list[0]['conates'][0])

        # my_yolo_bounds = self.rescaleBoundingBox(data_list[0]['conates'], universal.imagewidth, universal.imageheight, universal.scaleratio)
        yolo = []

        for dict in data_list:
            my_yolo_bounds = self.rescaleBoundingBox(dict['conates'], universal.imagewidth, universal.imageheight, universal.scaleratio)
            my_yolo_class = dict['class']
            yolo.append([my_yolo_class, my_yolo_bounds])

        print(yolo)

        file_name = os.path.splitext(os.path.basename(self.filename))[0]
        with open('./03_complete_images/' + file_name + '.txt', 'w') as file:
            for item in yolo:
                classItem = 0
                for numerator in range(len(CAPTURE_OPTIONS)):
                    if (item[0] == CAPTURE_OPTIONS[numerator]):
                        classItem = numerator
                        break
                print(f'{classItem} {item[1][0]} {item[1][1]} {item[1][2]} {item[1][3]}', file=file)
        

        # data_list is rectangle coords and class 
        # print(self.convert_coordinates_to_yolo(im_heiht,imwidth,im_ratio,coords))



class Panel2(ctk.CTkFrame):
    def __init__(self, parent, click_callback=None):
        super().__init__(master = parent, fg_color = BACKGROUND_COLOR)
        self.grid(sticky='ew')

        # Example: Creating a Label widget
        self.label_widget = ctk.CTkLabel(self, text="Default Content")
        self.label_widget.grid(column=0, row=0, sticky='W', padx=10, pady=5)

        # Bind the click event to the callback function
        if click_callback:
            self.bind("<Button-1>", click_callback)

    def set_label_content(self, new_content):
        self.label_widget.configure(text=new_content,font=("Arial", 12))

    def get_label_content(self):
        # Replace this with the actual logic to retrieve label content
        return self.label_widget.cget("text")

class TextPanel(ctk.CTkScrollableFrame):
   def __init__(self, parent, text, data_var):
       super().__init__(master=parent, fg_color=DARK_GREY)
       self.pack(fill='x', pady=4, ipady=8)
       
       self.current_row = 1

       # layout
       self.rowconfigure(0, weight=1)
       self.columnconfigure(0, weight=1)

       self.data_var = data_var
       self.data_var.trace('w',self.update_text)

       self.labelname = ctk.CTkLabel(self, text=text)
       self.labelname.grid(column=0, row=0, sticky='W', padx=10, pady=5)

       self.panel_instances = []



   def update_text(self, *args):
        # Clear existing panel instances
        for panel in self.panel_instances:
            panel.destroy()
        self.panel_instances = []

        # Update with new data
        string_list = self.data_var.get().split('", "')
        for sep in string_list:
            sep = sep[:-2]
            if sep != "":
                new_panel = Panel2(self)
                new_panel.set_label_content(sep)
                new_panel.bind("<Button-1>", lambda event, panel=new_panel: self.on_panel_click(panel))
                self.panel_instances.append(new_panel)
                new_panel.grid(column=0, row=self.current_row, sticky='W', padx=10, pady=5)
                self.current_row += 1

   def get_panel_contents(self):
        panel_contents = []
        for panel in self.panel_instances:
            # Access the content of each Panel instance
            # You can customize this based on the attributes or methods of your Panel class
            content = panel.get_label_content()
            panel_contents.append(content)
        return panel_contents
   
   def on_panel_click(self, panel):
        # Callback function when a Panel is clicked
        label_content = panel.get_label_content()
        print("Clicked on Panel with content:", label_content)


        ###### remove rectangle using the id on click, steal some of the scissor code
