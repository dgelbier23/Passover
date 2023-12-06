import customtkinter as ctk
from pssettings import *

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
    def __init__(self, parent, *args):
        super().__init__(master = parent, text = 'Revert', command = self.revert)
        self.pack(side='bottom', pady=10)
        self.args = args
    def revert(self):
        for var,value in self.args:
            var.set(value)


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

    #    self.data_vars = data_var
    #    for var in self.data_vars:
    #        var.trace('w', self.update_text)

   def update_text(self, *args):
        # self.labelname.configure(text = self.data_var.get())
        print("var.get" + self.data_var.get())
        string_list = self.data_var.get().split('", "')
        print("this is length" + str(len(string_list)))
        print("this is row number" + str(self.current_row))
        print(string_list[len(string_list)-1])
        sep = string_list[len(string_list)-1][:-2]
        if (sep != ""):
            # panel = Panel(self)
            # labelnames = ctk.CTkLabel(self, text=sep, font=("Arial", 12))
            # labelnames.grid(column=0, row=self.current_row, sticky='W', padx=10, pady=5)
            # self.current_row += 1
            # new_panel = Panel2(self, click_callback=lambda event, panel=new_panel: self.on_panel_click(new_panel))
            # new_panel.set_label_content(sep)
            new_panel = Panel2(self)
            new_panel.set_label_content(sep)

            # Use a lambda function with a default argument to capture the current panel
            new_panel.bind("<Button-1>", lambda event, panel=new_panel: self.on_panel_click(panel))
            self.panel_instances.append(new_panel)
            print(new_panel)
            

            # # Add a label to the Panel
            # label_names = ctk.CTkLabel(panel, text=sep, font=("Arial", 12))
            # label_names.grid(column=0, row=0, sticky='W', padx=10, pady=5)
            
            # Add the Panel to the grid of the TextPanel
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
