from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
from customtkinter import CTkOptionMenu
from customtkinter import CTkImage
from .CustomFunctionEditorWindow import CustomFunctionEditorWindow as CFEW
import os
import PIL
from PIL import Image
import tkinter as tk

class FunctionsList(CTkFrame):
    def __init__(self, *args,
                 option_manager: None,
                 step_index: 0,
                 **kwargs):
        super().__init__(*args, **kwargs)
        

        self.option_manager = option_manager
        self.step_index = step_index

        self.edit_mode = False
        self.render()
    
    def refresh(self, op=None):
        self.clear()
        self.render()

    def clear(self):
        self.containerFrame.destroy()
        
    def toggle_edit_mode(self):
        self.clear()
        self.edit_mode = not self.edit_mode
        self.render()
        
    def render(self):
        
        self.containerFrame = CTkFrame(self, fg_color="transparent")
        self.containerFrame.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.containerFrame.grid_columnconfigure((0, 1), weight=1)
        
        row = 1
        
        funcs = self.option_manager.get_steps()[self.step_index]["objective_functions"]
        
        index = 0
        for func in funcs:
            
            CTkLabel(self.containerFrame, text="Name:").grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
            CTkLabel(self.containerFrame, text="Objective:").grid(row=row, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")
            CTkLabel(self.containerFrame, text="Weight:").grid(row=row, column=2, padx=(5, 5), pady=(5, 5), sticky="nsew")
            
            row += 1
            
            columns = ["absdiff",
                       "absdifflog",
                       "ave",
                       "bias",
                       "fhf",
                       "ioa",
                       "ioa2",
                       "kge",
                       "kge09",
                       "mns",
                       "mse",
                       "ns",
                       "ns2log",
                       "nslog1p",
                       "nslog2",
                       "pbias",
                       "pmcc",
                       "rmse",
                       "trmse",
                       "custom"]
            
            CTkEntry(self.containerFrame, textvariable=func["name"]).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
            CTkOptionMenu(self.containerFrame, values=columns, variable=func["objective_function"], command=self.refresh).grid(row=row, column=1, padx=(5, 5), pady=(5, 5), sticky="ew")
            CTkEntry(self.containerFrame, textvariable=func["weight"]).grid(row=row, column=2, padx=(5, 5), pady=(5, 5), sticky="ew")
            
            row += 1

            if func["objective_function"].get() == "custom":

                CTkLabel(self.containerFrame, text="Custom Function:").grid(row=row, column=0, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="nsew")
                #CTkLabel(self.containerFrame, text="Target:").grid(row=row, column=2, padx=(5, 5), pady=(5, 5), sticky="nsew")

                row += 1

                CTkEntry(self.containerFrame, textvariable=func["custom_function"]).grid(row=row, column=0, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="ew")
                #CTkOptionMenu(self.containerFrame, values=["Positive Best", "Zero Best"], variable=func["custom_function_goal"]).grid(row=row, column=2, padx=(5, 5), pady=(5, 5), sticky="ew")

                def button_click_event(function_index):
                    dialog = CFEW(title="Edit Custom Function", step_index=self.step_index, function_index=function_index, option_manager=self.option_manager)


                open_window = lambda event=None, function_index=index: (button_click_event(function_index))
                expand_image = CTkImage(Image.open(os.path.join("./images", "expand.png")), size=(20, 20))
                button = CTkButton(self.containerFrame, width=30, text=None, image=expand_image, command=open_window)
                button.grid(row=row, column=3, padx=(5, 5), pady=(5, 5), sticky="new")


                row += 1
            
            CTkLabel(self.containerFrame, text="Observed and Simulated Data:").grid(row=row, column=0, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="nsew")
            
            row += 1
            
            CTkEntry(self.containerFrame, textvariable=func["data_observed"]).grid(row=row, column=0, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="nsew")
            row += 1
            CTkEntry(self.containerFrame, textvariable=func["data_simulated"]).grid(row=row, column=0, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="nsew")
            row += 1

            if self.edit_mode:
                remove_func = lambda index=index: (self.clear(), self.option_manager.remove_function(self.step_index, index), self.render())
                dupe_func = lambda index=index: (self.clear(), self.option_manager.dupe_function(self.step_index, index), self.render())
                CTkButton(self.containerFrame, text="Duplicate", command=dupe_func).grid(row=row, column=0, columnspan=1, padx=(5, 5), pady=(5, 5), sticky="ew")
                CTkButton(self.containerFrame, text="Remove", command=remove_func).grid(row=row, column=1, columnspan=1, padx=(5, 5), pady=(5, 5), sticky="ew")
                row += 1
                pass
            else:
                pass
            index += 1
            row += 1
            
        add_function = lambda: (self.clear(), self.option_manager.add_function(self.step_index), self.render())
        if len(funcs) > 0:
            if self.edit_mode:
                CTkButton(self.containerFrame, text="Exit", command=self.toggle_edit_mode).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
            else:
                CTkButton(self.containerFrame, text="Edit", command=self.toggle_edit_mode).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
            CTkButton(self.containerFrame, text="Add Objective Function", command=add_function).grid(row=row, column=1, columnspan=2, padx=(5, 5), pady=(5, 5), sticky="ew")
        else:
            CTkButton(self.containerFrame, text="Add Objective Function", command=add_function).grid(row=row, column=0, columnspan=2, padx=(5, 5), pady=(5, 5), sticky="ew")