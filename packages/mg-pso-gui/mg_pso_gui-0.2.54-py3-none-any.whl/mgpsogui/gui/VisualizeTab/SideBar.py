from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
from customtkinter import CTkTextbox
from customtkinter import CTkImage
from customtkinter import CTkOptionMenu
from PIL import Image
import os

from . import MatrixEditor as me

import pandas as pd

class SideBar(CTkScrollableFrame):
    def __init__(self, *args,
                 option_manager: None,
                 home_page: None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.option_manager = option_manager
        self.home_page = home_page
        
        self.render()

    def clear(self):
        self.containerFrame.destroy()

    def refresh(self):
        self.clear()
        self.render()

    def render(self):

        self.containerFrame = CTkFrame(self, width=300, fg_color="transparent")
        self.containerFrame.grid(row=0, column=0, padx=(
            0, 0), pady=(0, 0), sticky="ew")
        self.containerFrame.grid_columnconfigure(0, weight=1)
        
        selected_graph = self.option_manager.get("selected_graph").get()
        
        if (selected_graph == "Best Cost Stacked"):
            #self.graph_label = CTkLabel(self.containerFrame, text="Best Cost Stacked")
            #self.graph_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
            pass
        elif (selected_graph == "Best Cost by Round"):
            #self.graph_label = CTkLabel(self.containerFrame, text="Best Cost by Round")
            #self.graph_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
            pass
        elif (selected_graph == "Iteration Table"):
            #self.graph_label = CTkLabel(self.containerFrame, text="Iteration Table")
            #self.graph_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
            pass
        elif (selected_graph == "Calibrated Parameters"):
            #self.graph_label = CTkLabel(self.containerFrame, text="Calibrated Parameters")
            #self.graph_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
            pass
        elif (selected_graph == "Custom CSV"):
            
            folder = self.option_manager.get_project_folder()
            if not os.path.exists(folder):
                os.makedirs(folder)
                
            # Get all CSV files in the folder and add their paths to a list
            path_map = {}
            name_list = []
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith(".csv"):
                        name = file.replace(".csv", "")
                        name_list.append(name)
                        path_map[name] = os.path.join(root, file)
            
            if (len(name_list) == 0):
                name_list.append("No files found...")
            else:
                if (self.option_manager.get("selected_csv").get() not in name_list):
                    self.option_manager.get("selected_csv").set(name_list[0])
            
            file_label = CTkLabel(self.containerFrame, text="CSV File:")
            file_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 5), sticky="w")
            
            self.home_page.csv_file_selector = CTkOptionMenu(self.containerFrame, values=name_list, variable=self.option_manager.get("selected_csv"), command=self.home_page.update_graph)
            self.home_page.csv_file_selector.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
            
            selected_file = self.option_manager.get("selected_csv").get()
            if (selected_file in path_map and selected_file != self.home_page.open_file):
                self.home_page.csv_data = self.load_special_csv(path_map[selected_file])
                print(self.home_page.csv_data)
                self.home_page.open_file = selected_file
                
            if (self.home_page.csv_data is not None):
                # Get all column names of CSV
                columns = self.home_page.csv_data["data"].columns
                
                x_axis_label = CTkLabel(self.containerFrame, text="X Axis:")
                x_axis_label.grid(row=2, column=0, padx=(20, 20), pady=(40, 5), sticky="w")
                
                self.home_page.csv_x_selector = CTkOptionMenu(self.containerFrame, values=columns, variable=self.option_manager.get("selected_x"), command=self.home_page.update_graph)
                self.home_page.csv_x_selector.grid(row=3, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
                
                if (self.home_page.csv_x_selector.get() not in columns):
                    self.home_page.csv_x_selector.set(columns[1])
                
                y1_axis_label = CTkLabel(self.containerFrame, text="Y Axis:")
                y1_axis_label.grid(row=4, column=0, padx=(20, 20), pady=(20, 5), sticky="w")
                
                self.home_page.csv_y1_selector = CTkOptionMenu(self.containerFrame, values=columns, variable=self.option_manager.get("selected_y1"), command=self.home_page.update_graph)
                self.home_page.csv_y1_selector.grid(row=5, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
                
                if (self.home_page.csv_y1_selector.get() not in columns):
                    self.home_page.csv_y1_selector.set(columns[2])
                
                y2_axis_label = CTkLabel(self.containerFrame, text="Secondary Y Axis:")
                y2_axis_label.grid(row=6, column=0, padx=(20, 20), pady=(20, 5), sticky="w")
                
                self.home_page.csv_y2_selector = CTkOptionMenu(self.containerFrame, values=columns, variable=self.option_manager.get("selected_y2"), command=self.home_page.update_graph)
                self.home_page.csv_y2_selector.grid(row=7, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
                
                if (self.home_page.csv_y2_selector.get() not in columns):
                    self.home_page.csv_y2_selector.set(columns[3])
                    
        elif (selected_graph == "Compare CSV"):
            folder = self.option_manager.get_project_folder()
            if not os.path.exists(folder):
                os.makedirs(folder)
                
            # Get all CSV files in the folder and add their paths to a list
            path_map = {}
            name_list = []
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith(".csv"):
                        name = file.replace(".csv", "")
                        name_list.append(name)
                        path_map[name] = os.path.join(root, file)
            
            if (len(name_list) == 0):
                name_list.append("No files found...")
            else:
                if (self.option_manager.get("selected_csv").get() not in name_list):
                    self.option_manager.get("selected_csv").set(name_list[0])
                if (self.option_manager.get("selected_csv2").get() not in name_list):
                    self.option_manager.get("selected_csv2").set(name_list[0])
            
            file_label = CTkLabel(self.containerFrame, text="CSV Files:")
            file_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 5), sticky="w")
            
            self.home_page.csv_file_selector = CTkOptionMenu(self.containerFrame, values=name_list, variable=self.option_manager.get("selected_csv"), command=self.home_page.update_graph)
            self.home_page.csv_file_selector.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
            
            self.home_page.csv_file_selector2 = CTkOptionMenu(self.containerFrame, values=name_list, variable=self.option_manager.get("selected_csv2"), command=self.home_page.update_graph)
            self.home_page.csv_file_selector2.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
            
            selected_file = self.option_manager.get("selected_csv").get()
            if (selected_file in path_map and selected_file != self.home_page.open_file):
                self.home_page.csv_data = self.load_special_csv(path_map[selected_file])
                print(self.home_page.csv_data)
                self.home_page.open_file = selected_file
                
            selected_file2 = self.option_manager.get("selected_csv2").get()
            if (selected_file2 in path_map and selected_file2 != self.home_page.open_file2):
                self.home_page.csv_data2 = self.load_special_csv(path_map[selected_file2])
                print(self.home_page.csv_data2)
                self.home_page.open_file2 = selected_file2
                
            if (self.home_page.csv_data is not None and self.home_page.csv_data2 is not None):
                # Get all column names of CSV
                columns = self.home_page.csv_data["data"].columns
                columns2 = self.home_page.csv_data2["data"].columns
                
                x_axis_label = CTkLabel(self.containerFrame, text="X Axis:")
                x_axis_label.grid(row=3, column=0, padx=(20, 20), pady=(40, 5), sticky="w")
                
                self.home_page.csv_x_selector = CTkOptionMenu(self.containerFrame, values=columns, variable=self.option_manager.get("selected_x"), command=self.home_page.update_graph)
                self.home_page.csv_x_selector.grid(row=4, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
                
                if (self.home_page.csv_x_selector.get() not in columns):
                    self.home_page.csv_x_selector.set(columns[1])
                
                y1_axis_label = CTkLabel(self.containerFrame, text="Y Axis:")
                y1_axis_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 5), sticky="w")
                
                self.home_page.csv_y1_selector = CTkOptionMenu(self.containerFrame, values=columns, variable=self.option_manager.get("selected_y1"), command=self.home_page.update_graph)
                self.home_page.csv_y1_selector.grid(row=6, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
                
                if (self.home_page.csv_y1_selector.get() not in columns):
                    self.home_page.csv_y1_selector.set(columns[2])
                
                y2_axis_label = CTkLabel(self.containerFrame, text="Secondary Y Axis:")
                y2_axis_label.grid(row=7, column=0, padx=(20, 20), pady=(20, 5), sticky="w")
                
                self.home_page.csv_y2_selector = CTkOptionMenu(self.containerFrame, values=columns2, variable=self.option_manager.get("selected_y2"), command=self.home_page.update_graph)
                self.home_page.csv_y2_selector.grid(row=8, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
                
                if (self.home_page.csv_y2_selector.get() not in columns2):
                    self.home_page.csv_y2_selector.set(columns2[2])
                    
        elif (selected_graph == "Sampling CSV"):
            
            folder = self.option_manager.get_project_folder()
            if not os.path.exists(folder):
                os.makedirs(folder)
                
            # Get all CSV files in the folder and add their paths to a list
            path_map = {}
            name_list = []
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith(".csv"):
                        name = file.replace(".csv", "")
                        name_list.append(name)
                        path_map[name] = os.path.join(root, file)
            
            if (len(name_list) == 0):
                name_list.append("No files found...")
            else:
                if (self.option_manager.get("selected_csv").get() not in name_list):
                    self.option_manager.get("selected_csv").set(name_list[0])
            
            file_label = CTkLabel(self.containerFrame, text="CSV File:")
            file_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 5), sticky="w")
            
            self.home_page.csv_file_selector = CTkOptionMenu(self.containerFrame, values=name_list, variable=self.option_manager.get("selected_csv"), command=self.home_page.update_graph)
            self.home_page.csv_file_selector.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
            
            selected_file = self.option_manager.get("selected_csv").get()
            if (selected_file in path_map and selected_file != self.home_page.open_file):
                self.home_page.csv_data = pd.read_csv(path_map[selected_file])
                print(self.home_page.csv_data)
                self.home_page.open_file = selected_file
                
            if (self.home_page.csv_data is not None):
                # Get all column names of CSV
                columns = self.home_page.csv_data.columns
                
                x_axis_label = CTkLabel(self.containerFrame, text="X Axis:")
                x_axis_label.grid(row=2, column=0, padx=(20, 20), pady=(40, 5), sticky="w")
                
                self.home_page.csv_x_selector = CTkOptionMenu(self.containerFrame, values=columns, variable=self.option_manager.get("selected_x"), command=self.home_page.update_graph)
                self.home_page.csv_x_selector.grid(row=3, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
                
                if (self.home_page.csv_x_selector.get() not in columns):
                    self.home_page.csv_x_selector.set(columns[1])
                
                y1_axis_label = CTkLabel(self.containerFrame, text="Y Axis:")
                y1_axis_label.grid(row=4, column=0, padx=(20, 20), pady=(20, 5), sticky="w")
                
                self.home_page.csv_y1_selector = CTkOptionMenu(self.containerFrame, values=columns, variable=self.option_manager.get("selected_y1"), command=self.home_page.update_graph)
                self.home_page.csv_y1_selector.grid(row=5, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
                
                if (self.home_page.csv_y1_selector.get() not in columns):
                    self.home_page.csv_y1_selector.set(columns[2])
                
                y2_axis_label = CTkLabel(self.containerFrame, text="Secondary Y Axis:")
                y2_axis_label.grid(row=6, column=0, padx=(20, 20), pady=(20, 5), sticky="w")
                
                self.home_page.csv_y2_selector = CTkOptionMenu(self.containerFrame, values=columns, variable=self.option_manager.get("selected_y2"), command=self.home_page.update_graph)
                self.home_page.csv_y2_selector.grid(row=7, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
                
                if (self.home_page.csv_y2_selector.get() not in columns):
                    self.home_page.csv_y2_selector.set(columns[3])

                style_label = CTkLabel(self.containerFrame, text="Figure Style:")
                style_label.grid(row=8, column=0, padx=(20, 20), pady=(20, 5), sticky="w")
                
                self.home_page.figure_style_selector = CTkOptionMenu(self.containerFrame, values=["Scatter", "Bars", "Lines", "Area", "Box"], variable=self.option_manager.get("figure_style"), command=self.home_page.update_graph)
                self.home_page.figure_style_selector.grid(row=9, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")

        elif (selected_graph == "Matrix Editor"):
            
            folder = self.option_manager.get_project_folder()
            if not os.path.exists(folder):
                os.makedirs(folder)
                
            # Get all CSV files in the folder and add their paths to a list
            path_map = {}
            name_list = []
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith(".csv"):
                        name = file.replace(".csv", "")
                        name_list.append(name)
                        path_map[name] = os.path.join(root, file)
            
            if (len(name_list) == 0):
                name_list.append("No files found...")
            else:
                if (self.option_manager.get("selected_csv").get() not in name_list):
                    self.option_manager.get("selected_csv").set(name_list[0])
            
            file_label = CTkLabel(self.containerFrame, text="CSV File:")
            file_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 5), sticky="w")
            
            self.home_page.csv_file_selector = CTkOptionMenu(self.containerFrame, values=name_list, variable=self.option_manager.get("selected_csv"), command=self.home_page.update_graph)
            self.home_page.csv_file_selector.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
            
            selected_file = self.option_manager.get("selected_csv").get()
            if (selected_file in path_map and selected_file != self.home_page.open_file):
                self.home_page.csv_data = pd.read_csv(path_map[selected_file])
                print(self.home_page.csv_data)
                self.home_page.open_file = selected_file
                
            if (self.home_page.csv_data is not None):
                # Get all column names of CSV
                columns = self.home_page.csv_data.columns
                
                style_label = CTkLabel(self.containerFrame, text="Figure Style:")
                style_label.grid(row=2, column=0, padx=(20, 20), pady=(20, 5), sticky="w")
                
                self.home_page.figure_style_selector = CTkOptionMenu(self.containerFrame, values=["Scatter", "Bars", "Lines", "Area", "Box"], variable=self.option_manager.get("figure_style"), command=self.home_page.update_graph)
                self.home_page.figure_style_selector.grid(row=3, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")

                x_axis_label = CTkLabel(self.containerFrame, text="Y Axis:")
                x_axis_label.grid(row=4, column=0, padx=(20, 20), pady=(40, 5), sticky="w")
                
                self.home_page.csv_x_selector = CTkOptionMenu(self.containerFrame, values=columns, variable=self.option_manager.get("selected_x"), command=self.home_page.update_graph)
                self.home_page.csv_x_selector.grid(row=5, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
                
                if (self.home_page.csv_x_selector.get() not in columns):
                    self.home_page.csv_x_selector.set(columns[1])
                
                self.matrix_editor = me.MatrixEditor(self.containerFrame, width=280, option_manager=self.option_manager, home_page=self.home_page, columns=columns)
                self.matrix_editor.grid(row=6, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
                self.matrix_editor.grid_columnconfigure(0, weight=1)
                self.matrix_editor.grid_rowconfigure(0, weight=1)


                #y1_axis_label = CTkLabel(self.containerFrame, text="Y Axis:")
                #y1_axis_label.grid(row=6, column=0, padx=(20, 20), pady=(20, 5), sticky="w")

                #self.home_page.csv_y1_selector = CTkOptionMenu(self.containerFrame, values=columns, variable=self.option_manager.get("selected_y1"), command=self.home_page.update_graph)
                #self.home_page.csv_y1_selector.grid(row=7, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
                
                #if (self.home_page.csv_y1_selector.get() not in columns):
                #    self.home_page.csv_y1_selector.set(columns[2])

    def load_special_csv(self, file_path):
        file_metadata = {}
        data_metadata = {}
        mode = "file_metadata"
        columns = []
        data_lines = []
        
        with open(file_path, "r") as file:
            lines = file.readlines()
            
            if (not lines[0].startswith("@")):
                return {
                    "file_attributes": {},
                    "data_attributes": {},
                    "data": pd.read_csv(file_path)
                }
            
            for line in lines:
                if (line.startswith("@H,")):
                    mode = "data_metadata"
                    columns = line.strip().rstrip(",").split(",")[1:]
                    continue
                elif (line.startswith("@T,")):
                    mode = "file_metadata"
                    continue
                elif (line.startswith(",") and mode == "data_metadata"):
                    mode = "file_data"
                    
                if (mode == "file_metadata"):
                    try:
                        key, value = line.strip().rstrip(",").split(",")
                        file_metadata[key] = value
                    except:
                        pass
                    
                elif (mode == "data_metadata"):
                    try:
                        values = line.strip().rstrip(",").split(",")
                        key = values[0]
                        values = values[1:]
                        if len(values) == len(columns):
                            data_metadata[key] = {}
                            for i in range(len(columns)):
                                data_metadata[key][columns[i]] = values[i]
                    except:
                        pass
                    
                elif (mode == "file_data"):
                    try:
                        values = line.strip().rstrip(",").split(",")[1:]
                        if len(values) == len(columns):
                            data_lines.append(values)
                    except:
                        pass
                        
        return {
            "file_attributes": file_metadata,
            "data_attributes": data_metadata,
            "data": pd.DataFrame(data_lines, columns=columns)
        }