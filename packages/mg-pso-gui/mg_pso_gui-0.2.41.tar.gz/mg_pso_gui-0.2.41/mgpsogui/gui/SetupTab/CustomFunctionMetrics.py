from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
from customtkinter import CTkOptionMenu
import tkinter as tk
import subprocess
import platform
import os

global option_manager

class CustomFunctionsMetricsView(CTkScrollableFrame):
    def __init__(self, *args,
                 option_manager: None,
                 step_index: 0,
                 function_index: 0,
                 **kwargs):
        super().__init__(*args, **kwargs)
        
        self.option_manager = option_manager
        self.step_index = step_index
        self.functions_index = function_index
        self.key_values = []
        
        self.edit_mode = False

        self.columns = ["absdiff",
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
                        "trmse"]
        
        self.positive_best = {"absdiff": True,
                        "absdifflog": True,
                        "ave": True,
                        "bias": True,
                        "fhf": True,
                        "ioa": True,
                        "ioa2": True,
                        "kge": True,
                        "kge09": True,
                        "mns": True,
                        "mse": True,
                        "ns": False,
                        "ns2log": True,
                        "nslog1p": True,
                        "nslog2": True,
                        "pbias": True,
                        "pmcc": True,
                        "rmse": True,
                        "trmse": True}

        equation = self.option_manager.get_steps()[self.step_index]["objective_functions"][self.functions_index]["custom_function"].get()
        
        # Example equation (0 * (1 - ns)) + (bias * 0) + (pbias * 0) + (absdiff * 0)
        try:
            if equation != "":
                equation = equation.replace("1 - ", "")
                equation = equation.replace("(", "")
                equation = equation.replace(")", "")
                equation = equation.replace(" ", "")
                pairs = equation.split("+")
                for pair in pairs:
                    key, value = pair.split("*")
                    self.add_key(key, value)
        except Exception as e:
            self.key_values = []

        self.render()

    def clear(self):
        self.containerFrame.destroy()
        
    def toggle_edit_mode(self):
        self.clear()
        self.edit_mode = not self.edit_mode
        self.render()
        
    def add_key(self, key="ns", value="0"):
        obj = {"name": tk.StringVar(), "value": tk.StringVar()}
        obj['name'].set(key)
        obj['value'].set(value)
        self.key_values.append(obj)
        
    def remove_key(self, index):
        self.key_values.pop(index)
        
    def render(self):
        row = 0
        index = 0
        
        self.containerFrame = CTkFrame(self)
        self.containerFrame.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.containerFrame.grid_columnconfigure((0, 1), weight=1)
        
        CTkLabel(self.containerFrame, text="Objective:").grid(row=row, column=0, columnspan=1, padx=5, pady=5, sticky="")
        CTkLabel(self.containerFrame, text="Weight:").grid(row=row, column=1, columnspan=1, padx=5, pady=5, sticky="")
        row += 1
        
        for key_value_pair in self.key_values:
            CTkOptionMenu(self.containerFrame, values=self.columns, variable=self.key_values[index]["name"]).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")


            if self.edit_mode:
                return_func = lambda index=index: (self.clear(), self.remove_key(index), self.render())
                CTkButton(self.containerFrame, text="Remove", command=return_func).grid(row=row, column=1, padx=(5, 5), pady=(5, 5), sticky="ew")
            else:
                bb = CTkEntry(self.containerFrame)
                bb.grid(row=row, column=1, padx=(5, 5), pady=(5, 5), sticky="ew")
                bb.configure(textvariable=self.key_values[index]["value"])
            row += 1
            index += 1
            
        if self.edit_mode:
            CTkButton(self.containerFrame, text="Exit", command=self.toggle_edit_mode).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
        else:
            CTkButton(self.containerFrame, text="Edit", command=self.toggle_edit_mode).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
            
        add_key_func = lambda: (self.clear(), self.add_key(), self.render())
        CTkButton(self.containerFrame, text="Add", command=add_key_func).grid(row=row, column=1, padx=(5, 5), pady=(5, 5), sticky="ew")
        
        row += 1
        
    def push_to_option_manager(self):
        equation = ""

        for key_value in self.key_values:
            name = key_value["name"].get()
            weight = key_value["value"].get()

            positiveBest = self.positive_best[name]

            if positiveBest:
                equation += f"({name} * {weight}) + "
            else:
                equation += f"((1 - {name}) * {weight}) + "

        equation = equation[:-3]  # Remove the last " + "

        self.option_manager.get_steps()[self.step_index]["objective_functions"][self.functions_index]["custom_function"].set(equation)