from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
from customtkinter import CTkOptionMenu
from tkinter import StringVar as sv
import tkinter as tk

class ParameterView(CTkScrollableFrame):
    def __init__(self, *args,
                 option_manager: None,
                 list_name: None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        
        self.option_manager = option_manager
        self.list_name = list_name
        self.key_values = option_manager.get_list(self.list_name)
        self.edit_mode = False
        
        self.render()

    def clear(self):
        self.key_values = self.option_manager.get_list(self.list_name)
        self.containerFrame.destroy()
        
    def toggle_edit_mode(self):
        self.clear()
        self.edit_mode = not self.edit_mode
        self.render()
        
    def render(self):
        row = 0
        index = 0
        
        self.containerFrame = CTkFrame(self)
        self.containerFrame.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.containerFrame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        CTkLabel(self.containerFrame, text="Name:").grid(row=row, column=0, columnspan=3, padx=5, pady=5, sticky="")
        CTkLabel(self.containerFrame, text="Value:").grid(row=row, column=3, columnspan=3, padx=5, pady=5, sticky="")
        row += 1
        
        for key_value_pair in self.key_values:
            required = False
            visual_name = "NONE"
            if "required" in key_value_pair:
                required = key_value_pair["required"].get()
            if required and "visual_name" in key_value_pair:
                visual_name = key_value_pair["visual_name"]

            if visual_name != "NONE":
                CTkLabel(self.containerFrame, text=visual_name).grid(row=row, column=0, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="ew")
                #CTkEntry(self.containerFrame, state="disabled", textvariable=self.key_values[index]["visual_name"]).grid(row=row, column=0, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="ew")
            else:
                CTkEntry(self.containerFrame, textvariable=self.key_values[index]["name"]).grid(row=row, column=0, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="ew")
            
            if self.edit_mode and not required:
                type_menu = CTkOptionMenu(self.containerFrame, variable=self.key_values[index]["type"], values=["integer", "float", "date", "boolean", "string"], width=20)
                type_menu.grid(row=row, column=3, columnspan=1, padx=(0, 0), pady=(5, 5), sticky="ew")

                dest_menu = CTkOptionMenu(self.containerFrame, variable=self.key_values[index]["destination"], values=["args", "kwargs", "conf", "options", "oh_strategy", "metainfo"], width=20)
                dest_menu.grid(row=row, column=4, columnspan=1, padx=(0, 0), pady=(5, 5), sticky="ew")


                return_func = lambda index=index: (self.clear(), self.option_manager.remove_key_value(self.list_name, index), self.render())
                
                CTkButton(self.containerFrame, text="Remove", command=return_func).grid(row=row, column=5, columnspan=1, padx=(5, 5), pady=(5, 5), sticky="ew")
            else:
                type = self.key_values[index]["type"].get()

                if type == "boolean":
                    bb = CTkOptionMenu(self.containerFrame, values=["True", "False", "NULL"], variable=self.key_values[index]["value"])
                    bb.grid(row=row, column=3, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="ew")
                elif type == "date":
                    om_text_var = self.key_values[index]["value"]
                    year = sv()
                    month = sv()
                    day = sv()
                    vv = om_text_var.get().split("-")
                    year.set(vv[0])
                    month.set(vv[1])
                    day.set(vv[2])
                    year_options = [str(i) for i in range(1999, 2030)]
                    month_options = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
                    day_options = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
                    
                    update_date = lambda om_text_var=om_text_var, year=year, month=month, day=day: om_text_var.set(f"{year.get()}-{month.get()}-{day.get()}")
                    year_menu = CTkOptionMenu(self.containerFrame, variable=year, values=year_options, width=50, command=update_date)
                    year_menu.grid(row=row, column=3, columnspan=1, padx=(0, 0), pady=(5, 5), sticky="ew")
                    month_menu = CTkOptionMenu(self.containerFrame, variable=month, values=month_options, width=20, command=update_date)
                    month_menu.grid(row=row, column=4, columnspan=1, padx=(0, 0), pady=(5, 5), sticky="ew")
                    day_menu = CTkOptionMenu(self.containerFrame, variable=day, values=day_options, width=20, command=update_date)
                    day_menu.grid(row=row, column=5, columnspan=1, padx=(0, 0), pady=(5, 5), sticky="ew")
                else:
                    bb = CTkEntry(self.containerFrame)
                    bb.grid(row=row, column=3, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="ew")
                    bb.configure(textvariable=self.key_values[index]["value"])
            row += 1
            index += 1
            
        if self.edit_mode:
            CTkButton(self.containerFrame, text="Exit", command=self.toggle_edit_mode).grid(row=row, column=0, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="ew")
        else:
            CTkButton(self.containerFrame, text="Edit", command=self.toggle_edit_mode).grid(row=row, column=0, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="ew")
            
        add_key_func = lambda: (self.clear(), self.option_manager.add_key_value(self.list_name, "name", "value"), self.render())

        CTkButton(self.containerFrame, text="Add Parameter", command=add_key_func).grid(row=row, column=3, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="ew")