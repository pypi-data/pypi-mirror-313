from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
from customtkinter import CTkTextbox
from customtkinter import CTkImage
from customtkinter import CTkOptionMenu
from .OverrideParameterWindow import OverrideParameterWindow as OPW
from PIL import Image
import os

from . import BoundsList
from . import FunctionsList
from . import ListEditor


class StepView(CTkScrollableFrame):
    def __init__(self, *args,
                 option_manager: None,
                 home_page: None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.option_manager = option_manager
        self.analysisFrame = None
        self.containerFrame = None
        self.home_page = home_page

        self.render()

    def refresh(self):
        self.clear()
        self.render()

    def clear(self):
        if self.containerFrame != None:
            self.containerFrame.destroy()

        if self.analysisFrame != None:
            self.analysisFrame.destroy()

    def create_new_step(self):

        self.clear()
        example_step = [{    # step 1
            'parameter_objects': [
                {
                    'name': 'soilOutLPS',
                    'min_bound': 0.0,
                    'max_bound': 2.0
                },
                {
                    'name': 'lagInterflow',
                    'min_bound': 10.0,
                    'max_bound': 80.0
                }
            ],
            'objfunc': [
                {
                    'name': 'ns',
                    'of': 'ns',
                    'data': ('obs_data02_14.csv/obs/orun[1]',
                             'output/csip_run/out/Outlet.csv/output/catchmentSimRunoff')
                }
            ],
            'open': True
        }]
        self.option_manager.add_steps(example_step)

        self.render()

    def render(self):

        row = 0
        index = 0

        self.containerFrame = CTkFrame(self)
        self.containerFrame.grid(row=0, column=0, padx=(
            10, 10), pady=(10, 10), sticky="nsew")
        self.containerFrame.grid_columnconfigure((0, 1), weight=1)

        self.steps = self.option_manager.get_steps()
        self.mode = self.option_manager.get_mode()

        if (self.mode == "Sensitivity Analysis"):
            folder = self.option_manager.get_project_folder()
            
            # File all CSV files in folder and put them into list with strings as path
            files = []
            if os.path.exists(folder):
                files = [f for f in os.listdir(folder) if f.endswith('.csv')]

            if len(files) == 0:
                files = ["      No CSV files found! Run sampling first!       "]
            elif self.option_manager.get("sensitivity_analysis_path").get() not in files:
                self.option_manager.get("sensitivity_analysis_path").set(files[0])

            header_padding_x = (5, 5)
            header_padding_y = (10, 10)

            self.file_selector_frame = CTkFrame(self.containerFrame)
            self.file_selector_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
            self.logo_label = CTkLabel(self.file_selector_frame, text="Select File:")
            self.logo_label.grid(row=0, column=0, padx=(10, 10), pady=header_padding_y)
            
            self.file_selector = CTkOptionMenu(self.file_selector_frame, values=files, width=50, variable=self.option_manager.get("sensitivity_analysis_path"))
            self.file_selector.grid(row=0, column=1, padx=(10, 10), pady=header_padding_y)

            row += 1

        elif (self.mode == "Sampling: Halton" or self.mode == "Sampling: Random"):
            header_padding_x = (5, 5)
            header_padding_y = (10, 10)

            self.file_selector_frame = CTkFrame(self.containerFrame)
            self.file_selector_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
            
            self.logo_label2 = CTkLabel(self.file_selector_frame, text="Output:")
            self.logo_label2.grid(row=0, column=1, padx=(20, 10), pady=header_padding_y)

            self.output_method = CTkOptionMenu(self.file_selector_frame, values=["Replace", "Append"], width=50, variable=self.option_manager.get("sampling_output_mode"))
            if self.option_manager.get("sampling_output_mode").get() == "":
                self.option_manager.get("sampling_output_mode").set("Replace")
            self.output_method.grid(row=0, column=2, padx=(10, 10), pady=header_padding_y)

            row += 1


        for step in self.steps:

            up_image = CTkImage(Image.open(os.path.join("./images", "up.png")), size=(20, 20))
            down_image = CTkImage(Image.open(os.path.join("./images", "down.png")), size=(20, 20))
            trash_image = CTkImage(Image.open(os.path.join("./images", "trash.png")), size=(20, 20))
            expand_image = CTkImage(Image.open(os.path.join("./images", "expand.png")), size=(20, 20))
            collapse_image = CTkImage(Image.open(os.path.join("./images", "collapse.png")), size=(20, 20))
            override_image = CTkImage(Image.open(os.path.join("./images", "plus.png")), size=(20, 20))


            expand_func = lambda index=index: (self.clear(), self.option_manager.toggle_step_open(index), self.render())
            up_func = lambda index=index: (self.clear(), self.option_manager.move_step_up(index), self.render())
            down_func = lambda index=index: (self.clear(), self.option_manager.move_step_down(index), self.render())
            remove_func = lambda index=index: (self.clear(), self.option_manager.remove_step(index), self.render())
            open_override_window = lambda index=index: (OPW(title="Edit Override Parameters", step_index=index, option_manager=self.option_manager))

            if (self.mode == "Optimization"):
                button_container = CTkFrame(self.containerFrame, width=200)
                button_container.grid(row=row, column=1, sticky="nse", padx=(10, 10), pady=(10, 10))
                button_container.grid_rowconfigure(0, weight=1)
                button_container.grid_columnconfigure(0, weight=1)
                
                CTkEntry(self.containerFrame, textvariable=step['name'], width=500).grid(row=row, column=0, padx=(20, 20), pady=(20, 20), sticky="nsw")
            
    
                CTkButton(button_container, width=30, text=None, image=expand_image if not step['open'] else collapse_image, command=expand_func).grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")
                CTkButton(button_container, width=30, text=None, image=override_image, command=open_override_window).grid(row=0, column=1, padx=(5, 5), pady=(10, 10), sticky="nsew")
                CTkButton(button_container, width=30, text=None, image=up_image, state="disabled" if index==0 else "normal", fg_color="gray" if index==0 else None, command=up_func).grid(row=0, column=2, padx=(5, 5), pady=(10, 10), sticky="nsew")
                CTkButton(button_container, width=30, text=None, image=down_image, state="disabled" if index==(len(self.steps)-1) else "normal", fg_color="gray" if index==(len(self.steps)-1) else None, command=down_func).grid(row=0, column=3, padx=(5, 10), pady=(10, 10), sticky="nsew")
                CTkButton(button_container, width=30, text=None, image=trash_image, command=remove_func).grid(row=0, column=4, padx=(5, 20), pady=(10, 10), sticky="nsew")

                row += 1

            if step['open'] or (self.mode == "Sampling: Halton" or self.mode == "Sampling: Random" or self.mode == "Sensitivity Analysis"):
                bounds = BoundsList.BoundsList(
                    self.containerFrame, option_manager=self.option_manager, step_index=index)
                bounds.grid(row=row, column=0, padx=(10, 10),
                            pady=(10, 10), sticky="nsew")
                bounds.grid_columnconfigure(0, weight=1)
                bounds.grid_rowconfigure(0, weight=1)
                
                funcs = FunctionsList.FunctionsList(
                    self.containerFrame, option_manager=self.option_manager, step_index=index)
                funcs.grid(row=row, column=1, padx=(10, 10),
                            pady=(10, 10), sticky="nsew")
                funcs.grid_columnconfigure(0, weight=1)
                funcs.grid_rowconfigure(0, weight=1)
                
            row += 1
            index += 1
            
            if (self.mode != "Optimization"):
                break

        # Create an "Add step button that is centered
        if (self.mode == "Optimization" or len(self.steps) == 0):
            CTkButton(self.containerFrame, text="Add Group", command=self.create_new_step).grid(
                row=row, columnspan=2, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")
            
