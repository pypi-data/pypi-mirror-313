import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
import os
import platform
import subprocess
import shutil

from . import SideBar

def create_tab(self, tab):
    
    def open_graph_in_browser():
        # Open the file in the default program
        folder = self.option_manager.get_project_folder()
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file_path = os.path.join(folder, self.selected_graph_name + ".html")
        
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", file_path])
        else:
            subprocess.Popen(["xdg-open", file_path])

    def export_graph():
        
        folder = self.option_manager.get_project_folder()
        
        if not os.path.exists(folder):
            os.makedirs(folder)

        html_file = os.path.join(folder, self.selected_graph_name + ".html")
        json_file = os.path.join(folder, self.selected_graph_name + ".json")
        png_file = os.path.join(folder, self.selected_graph_name + ".png")
        pdf_file = os.path.join(folder, self.selected_graph_name + ".pdf")

        # Make a directory call package
        if not os.path.exists(os.path.join(folder, self.selected_graph_name + "_package")):
            os.makedirs(os.path.join(folder, self.selected_graph_name + "_package"))

        # Check if html_file exists and copy it to the package directory
        if os.path.exists(html_file):
            with open(html_file, 'r') as file:
                data = file.read()
                with open(os.path.join(folder, self.selected_graph_name + "_package", self.selected_graph_name + ".html"), 'w') as new_file:
                    new_file.write(data)

        # Check if json_file exists and copy it to the package directory
        if os.path.exists(json_file):
            with open(json_file, 'r') as file:
                data = file.read()
                with open(os.path.join(folder, self.selected_graph_name + "_package", self.selected_graph_name + ".json"), 'w') as new_file:
                    new_file.write(data)
        
        # Check if png_file exists and copy it to the package directory
        if os.path.exists(png_file):
            with open(png_file, 'rb') as file:
                data = file.read()
                with open(os.path.join(folder, self.selected_graph_name + "_package", self.selected_graph_name + ".png"), 'wb') as new_file:
                    new_file.write(data)

        # Check if pdf_file exists and copy it to the package directory
        if os.path.exists(pdf_file):
            with open(pdf_file, 'rb') as file:
                data = file.read()
                with open(os.path.join(folder, self.selected_graph_name + "_package", self.selected_graph_name + ".pdf"), 'wb') as new_file:
                    new_file.write(data)
        
        # Zip the package directory
        shutil.make_archive(os.path.join(folder, self.selected_graph_name + "_package"), 'zip', os.path.join(folder, self.selected_graph_name + "_package"))

        # Open the directory containing the package
        if platform.system() == "Windows":
            os.startfile(os.path.join(folder, self.selected_graph_name + "_package"))
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", os.path.join(folder, self.selected_graph_name + "_package")])
        else:
            subprocess.Popen(["xdg-open", os.path.join(folder, self.selected_graph_name + "_package")])
    
    def _resize_image(event):
        self.graph_label.update_idletasks()
        new_width = self.graph_label.winfo_width()
        new_height = self.graph_label.winfo_height()
        
        alt_width = new_height * 1.77778
        alt_height = new_width / 1.77778
        
        if (new_width < new_height):
            new_height = alt_height
        else:
            new_width = alt_width
        
        self.image_width = new_width
        self.image_height = new_height
        
        self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(new_width, new_height))
        self.graph_label.configure(image=self.graph_image)
        self.graph_label.update_idletasks()
    
    
    tab.grid_columnconfigure(0, weight=2)
    tab.grid_columnconfigure(1, weight=8)
    tab.grid_rowconfigure(0, weight=1)
    
    self.graph_sidebar = customtkinter.CTkFrame(tab)
    self.graph_sidebar.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    self.graph_container = customtkinter.CTkFrame(tab)
    self.graph_container.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    self.graph_sidebar.grid_columnconfigure(0, weight=1)
    self.graph_sidebar.grid_rowconfigure(1, weight=1)
    self.graph_container.grid_columnconfigure(0, weight=1)
    self.graph_container.grid_rowconfigure(0, weight=1)
    
    self.graph_selector = customtkinter.CTkOptionMenu(self.graph_sidebar, values=["Best Cost Stacked", "Best Cost by Round", "Custom CSV", "Compare CSV", "Sampling CSV", "Matrix Editor"], variable=self.graph_selector_value, command=self.update_graph)
    self.graph_selector.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    # Create SideBar
    self.vis_sidebar = SideBar.SideBar(self.graph_sidebar, option_manager=self.option_manager, home_page=self, fg_color="transparent")
    self.vis_sidebar.grid(row=1, column=0, rowspan=6, padx=(0, 0), pady=(0, 0), sticky="nsew")
    

    self.graph_theme = customtkinter.CTkOptionMenu(self.graph_sidebar, values=["Dark", "Light", "Publication"], variable=self.graph_theme_value, command=self.update_graph)
    self.graph_theme.grid(row=7, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

    self.graph_export = customtkinter.CTkButton(self.graph_sidebar, text="Export", command=export_graph)
    self.graph_export.grid(row=8, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

    # Add a button to call open_graph_in_browser
    self.graph_button = customtkinter.CTkButton(self.graph_sidebar, text="Preview", command=open_graph_in_browser)
    self.graph_button.grid(row=9, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    self.graph_image_obj = Image.open(os.path.join("./images", "refresh_hd.png"))
    self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(1280, 720))
    self.graph_label = customtkinter.CTkLabel(self.graph_container, text=None, image=self.graph_image)
    self.graph_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    #window = customtkinter.CTk()
    #self.graph_label.bind('<Configure>', _resize_image)