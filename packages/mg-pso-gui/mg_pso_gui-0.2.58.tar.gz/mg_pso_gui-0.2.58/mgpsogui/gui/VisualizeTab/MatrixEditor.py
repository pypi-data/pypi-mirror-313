from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
from customtkinter import CTkOptionMenu
import tkinter as tk

global option_manager

class MatrixEditor(CTkFrame):
    def __init__(self, *args,
                 option_manager: None,
                 home_page: None,
                 columns: None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        
        self.option_manager = option_manager
        self.home_page = home_page
        self.columns = columns  
        self.key_values = option_manager.get('figure_parameters')
        self.edit_mode = False
        
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
        
        self.containerFrame = CTkFrame(self)
        self.containerFrame.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="new")
        self.containerFrame.grid_columnconfigure((0, 1), weight=1)
        
        CTkLabel(self.containerFrame, text="X Axes:").grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        row += 1

        for key_value_pair in self.key_values:
            if self.edit_mode:
                bb = CTkOptionMenu(self.containerFrame, values=self.columns, variable=self.key_values[index]["value"], command=self.home_page.update_graph)
                bb.grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
                
                return_func = lambda index=index: (self.clear(), self.option_manager.remove_key_value('figure_parameters', index), self.home_page.update_graph(0), self.render())
                CTkButton(self.containerFrame, text="Remove", command=return_func).grid(row=row, column=1, padx=(5, 5), pady=(5, 5), sticky="ew")
            else:
                bb = CTkOptionMenu(self.containerFrame, values=self.columns, variable=self.key_values[index]["value"], command=self.home_page.update_graph)
                bb.grid(row=row, column=0, columnspan=2, padx=(5, 5), pady=(5, 5), sticky="ew")
            row += 1
            index += 1
            
        if self.edit_mode:
            CTkButton(self.containerFrame, text="Exit", width=100, command=self.toggle_edit_mode).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
        else:
            CTkButton(self.containerFrame, text="Edit", width=100, command=self.toggle_edit_mode).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
            
        add_key_func = lambda: (self.clear(), self.option_manager.add_key_value('figure_parameters', "Fig " + str(len(self.key_values)), self.columns[2], destination="NONE"), self.home_page.update_graph(0), self.render())
        CTkButton(self.containerFrame, text="Add Figure", width=100, command=add_key_func).grid(row=row, column=1, padx=(5, 5), pady=(5, 5), sticky="ew")