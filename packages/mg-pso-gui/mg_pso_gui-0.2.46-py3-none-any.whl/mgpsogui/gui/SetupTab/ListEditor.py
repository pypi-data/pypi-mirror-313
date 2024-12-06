from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
from customtkinter import CTkOptionMenu
import tkinter as tk

class ListEditor(CTkFrame):
    def __init__(self, *args,
                 option_manager: None,
                 columns: None,
                 parameter_name: None,
                 parameter_remove_func: None,
                 parameter_add_func: None,
                 title: None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        
        self.option_manager = option_manager
        self.columns = columns  
        self.parameter_name = parameter_name
        self.parameter_remove_func = parameter_remove_func
        self.parameter_add_func = parameter_add_func
        self.key_values = option_manager.get(self.parameter_name)
        self.edit_mode = False
        self.title = title
        
        self.render()

    def clear(self):
        self.containerFrame.destroy()

    def set_columns(self, columns):
        self.columns = columns
        
    def toggle_edit_mode(self):
        self.clear()
        self.edit_mode = not self.edit_mode
        self.render()
        
    def render(self):
        row = 0
        index = 0
        
        self.containerFrame = CTkFrame(self, fg_color="transparent")
        self.containerFrame.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="new")
        self.containerFrame.grid_columnconfigure((0, 1), weight=1)
        
        CTkLabel(self.containerFrame, text=self.title).grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        row += 1

        for key_value_pair in self.key_values:
            if self.edit_mode:
                bb = CTkOptionMenu(self.containerFrame, values=self.columns, variable=self.key_values[index]["value"])
                bb.grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
                
                return_func = lambda index=index: (self.clear(), self.parameter_remove_func(index), self.render())
                CTkButton(self.containerFrame, text="Remove", command=return_func).grid(row=row, column=1, padx=(5, 5), pady=(5, 5), sticky="ew")
            else:
                bb = CTkOptionMenu(self.containerFrame, values=self.columns, variable=self.key_values[index]["value"])
                bb.grid(row=row, column=0, columnspan=2, padx=(5, 5), pady=(5, 5), sticky="ew")
            row += 1
            index += 1
            
        if self.edit_mode:
            CTkButton(self.containerFrame, text="Exit", command=self.toggle_edit_mode).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
        else:
            CTkButton(self.containerFrame, text="Edit", command=self.toggle_edit_mode).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
            
        add_key_func = lambda: (self.clear(), self.parameter_add_func("Param " + str(len(self.key_values)) , self.columns[2]), self.render())
        CTkButton(self.containerFrame, text="Add Parameter", command=add_key_func).grid(row=row, column=1, padx=(5, 5), pady=(5, 5), sticky="ew")