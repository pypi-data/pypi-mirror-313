from typing import Union, Tuple, Optional

from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
from customtkinter import CTkInputDialog
from .CustomFunctionMetrics import CustomFunctionsMetricsView as ListView

class CustomFunctionEditorWindow(CTkInputDialog):
    """
    Dialog with extra window, message, entry widget, cancel and ok button.
    For detailed information check out the documentation.
    """

    def __init__(self, *args,
                 step_index: 0,
                 function_index: 0,
                 option_manager: None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        
        self.geometry("400x800")
        
        self.step_index = step_index
        self.function_index = function_index  
        self.option_manager = option_manager
        self.bounds = None

    def _create_widgets(self):

        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self.bounds = ListView(
                self, step_index=self.step_index, function_index=self.function_index, option_manager=self.option_manager)
        self.bounds.grid(row=0, column=0, columnspan=2, padx=(10, 10),
                    pady=(10, 10), sticky="nsew")
        self.bounds.grid_columnconfigure(0, weight=1)

        self._ok_button = CTkButton(master=self,
                                    width=100,
                                    border_width=0,
                                    fg_color=self._button_fg_color,
                                    hover_color=self._button_hover_color,
                                    text_color=self._button_text_color,
                                    text='Save',
                                    command=self._ok_event)
        self._ok_button.grid(row=2, column=0, columnspan=1, padx=(20, 10), pady=(0, 20), sticky="ew")

        self._cancel_button = CTkButton(master=self,
                                        width=100,
                                        border_width=0,
                                        fg_color=self._button_fg_color,
                                        hover_color=self._button_hover_color,
                                        text_color=self._button_text_color,
                                        text='Cancel',
                                        command=self._cancel_event)
        self._cancel_button.grid(row=2, column=1, columnspan=1, padx=(10, 20), pady=(0, 20), sticky="ew")
        
    def _ok_event(self, event=None):
        # Save values in bounds editor...
        
        self.bounds.push_to_option_manager()
        
        self.grab_release()
        self.destroy()

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def _cancel_event(self):
        self.grab_release()
        self.destroy()