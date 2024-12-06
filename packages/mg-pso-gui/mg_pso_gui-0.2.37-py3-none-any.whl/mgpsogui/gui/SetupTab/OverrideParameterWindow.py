from typing import Union, Tuple, Optional

from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
from customtkinter import CTkInputDialog
from .OverrideParameterMetrics import OverrideParameterMetrics as ListView

class OverrideParameterWindow(CTkInputDialog):
    """
    Dialog with extra window, message, entry widget, cancel and ok button.
    For detailed information check out the documentation.
    """

    def __init__(self, *args,
                 step_index: 0,
                 option_manager: None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        
        self.geometry("400x800")
        
        self.step_index = step_index
        self.option_manager = option_manager
        self.bounds = None

    def _create_widgets(self):

        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self.bounds = ListView(
                self, step_index=self.step_index, option_manager=self.option_manager)
        self.bounds.grid(row=0, column=0, columnspan=2, padx=(10, 10),
                    pady=(10, 10), sticky="nsew")
        self.bounds.grid_columnconfigure(0, weight=1)

    def _on_closing(self):
        self.grab_release()
        self.destroy()
