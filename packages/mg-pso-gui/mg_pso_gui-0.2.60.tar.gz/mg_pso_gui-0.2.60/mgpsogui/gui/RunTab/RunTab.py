
import customtkinter
import json
import os
from multiprocessing import Process
import traceback
import re
import ast
import pandas as pd
import numpy as np
import os
import platform
import subprocess

from ...util import PSORunner
from ...util import GraphGenerator
from ...util.CTkToolTip import CTkToolTip as ctt
import customtkinter

from . import OptimalParameterView as opv

def create_tab(self, tab):
    
    # URL
    tab.grid_columnconfigure(0, weight=1)
    tab.grid_columnconfigure(1, weight=5)
    tab.grid_columnconfigure(2, weight=1)
    tab.grid_rowconfigure(0, weight=200)

    #self.progress_container = customtkinter.CTkFrame(tab)
    #self.progress_container.grid_columnconfigure(0, weight=1)
    #self.progress_container.grid_columnconfigure(1, weight=1)
    #self.progress_container.grid_columnconfigure(2, weight=1)
    #self.progress_container.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    # Add progress bar to progress container
    #self.progress_message_left = customtkinter.CTkLabel(self.progress_container, text="")
    #self.progress_message_left.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
    
    #self.progress_message_middle = customtkinter.CTkLabel(self.progress_container, text="Calibration not running...")
    #self.progress_message_middle.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")
    
    #self.progress_message_right = customtkinter.CTkLabel(self.progress_container, text="")
    #self.progress_message_right.grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="e")
    
    self.optimal_param_frame = opv.OptimalParameterView(tab, option_manager=self.option_manager, label_text="Optimal Parameters")
    self.optimal_param_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    self.optimal_param_frame.grid_columnconfigure(0, weight=1)
    self.optimal_param_frame.grid_rowconfigure(0, weight=1)

    self.textbox = customtkinter.CTkTextbox(tab)
    self.textbox.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
    self.textbox.insert("0.0", "Welcome to the CSIP PSO Calibration Tool!\n\nUse the Setup tab to define steps and calibration parameters. Use this tab to view logs and manage your Project. Once finished, use the Results tab to generate figures and graphs.")
        
    self.project_editor = customtkinter.CTkScrollableFrame(tab, label_text="Project Editor")
    self.project_editor.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
    self.project_editor.grid_columnconfigure(0, weight=1)
    self.project_editor.grid_rowconfigure(0, weight=1)

    customtkinter.CTkLabel(self.project_editor, text="Copy Data to Current Mode:").grid(row=0, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")

    def copy_sense():
        self.option_manager.copy_list("Sensitivity Analysis")
        self.refresh_step_view(0)

    def copy_halton():
        self.option_manager.copy_list("Sampling: Halton")
        self.refresh_step_view(0)
    
    def copy_random():
        self.option_manager.copy_list("Sampling: Random")
        self.refresh_step_view(0)

    def copy_optim():
        self.option_manager.copy_list("Optimization")
        self.refresh_step_view(0)

    def open_project_folder():
        # Open the file in the default program
        folder = self.option_manager.get_project_folder()
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        if platform.system() == "Windows":
            os.startfile(folder)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", folder])
        else:
            subprocess.Popen(["xdg-open", folder])

    self.analysis_copy = customtkinter.CTkButton(self.project_editor, text="From Sensitivity Analysis", command=copy_sense)
    self.analysis_copy.grid(row=1, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")

    self.halton_copy = customtkinter.CTkButton(self.project_editor, text="From Sampling: Halton", command=copy_halton)
    self.halton_copy.grid(row=2, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")

    self.random_copy = customtkinter.CTkButton(self.project_editor, text="From Sampling: Random", command=copy_random)
    self.random_copy.grid(row=3, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")

    self.optimization_copy = customtkinter.CTkButton(self.project_editor, text="From Optimization", command=copy_optim)
    self.optimization_copy.grid(row=4, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")

    customtkinter.CTkLabel(self.project_editor, text="Project Management:").grid(row=5, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")

    self.open_folder = customtkinter.CTkButton(self.project_editor, text="Open Project Folder", command=open_project_folder)
    self.open_folder.grid(row=6, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")

    customtkinter.CTkLabel(self.project_editor, text="Project Name:").grid(row=7, column=0, padx=(20, 20), pady=(10, 5), sticky="ew")
    self.project_name_label = customtkinter.CTkLabel(self.project_editor, text=self.option_manager.get_project_data()["name"])
    self.project_name_label.grid(row=8, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")

    customtkinter.CTkLabel(self.project_editor, text="Project Path:").grid(row=9, column=0, padx=(20, 20), pady=(10, 5), sticky="ew")
    self.project_path_label = customtkinter.CTkLabel(self.project_editor, text=self.option_manager.get_project_data()["path"])
    self.project_path_label.grid(row=10, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")