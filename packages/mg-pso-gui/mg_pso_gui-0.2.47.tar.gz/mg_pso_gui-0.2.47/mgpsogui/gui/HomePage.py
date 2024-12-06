#!/usr/local/bin/python3.10

import os 
import time
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
print(dir_path)

# minikube kubectl -- create -f ../start.yaml ; sleep 60 ; minikube service pf8087-csu-csip-oms -n csip

import requests

import tkinter as tk
import tkinter.messagebox
import customtkinter
from customtkinter import ThemeManager
import json
import os
from PIL import Image, ImageTk
import traceback
from multiprocessing import Process
from multiprocessing import Queue

import re
import pandas as pd
import numpy as np
import ast
import platform
import time

from queue import Empty

from ..util import PSORunner
from ..util import GraphGenerator
from ..util.CTkToolTip import CTkToolTip as ctt
from ..util import helpers as hp

import subprocess
import plotly.express as px
import plotly.graph_objs as go

from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

from . import OptionManager as om

from .SetupTab import SetupTab as st
from .PlatformTab import PlatformTab as pt
from .RunTab import RunTab as rt
from .VisualizeTab import VisualizeTab as vt

from ..util.CTkToolTip import CTkToolTip as ctt

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

results_queue = Queue()
stdout_queue = Queue()
stderr_queue = Queue()

class App(customtkinter.CTk):
	def __init__(self):
		super().__init__()
		
		self.option_manager = om.OptionManager()
		
		# self.graph_selector_value = tk.StringVar()
		# self.graph_selector_value.set("Best Cost Stacked")

		# self.graph_theme_value = tk.StringVar()
		# self.graph_theme_value.set("Dark")

		# self.selected_csv = tk.StringVar()
		# self.selected_csv.set("No files found...")
		self.open_file = "None"
		self.csv_data = None

		# self.selected_csv2 = tk.StringVar()
		# self.selected_csv2.set("No files found...")
		self.open_file2 = "None"
		self.csv_data2 = None

		# self.selected_x = tk.StringVar()
		# self.selected_x.set("time")

		# self.selected_y1 = tk.StringVar()
		# self.selected_y1.set("NONE")

		# self.selected_y2 = tk.StringVar()
		# self.selected_y2.set("NONE")

		# self.figure_style = tk.StringVar()
		# self.figure_style.set("Scatter")

		# self.matrix_values = []
		# self.matrix_values.append(tk.StringVar())
		# self.matrix_values[0].set("NONE")

		self.running_config = None
		self.selected_graph_name = None

		self.train_process = None
		self.minikube_process = None
		self.data_x = [0]
		self.data_y = [0]
		
		self.image_scale = 1
		self.image_width = 1280
		self.image_height = 720
		self.progress_data = None
		self.calibration_data = None
		self.testing = False

		# configure window
		self.title("COSU Manager")
		self.geometry(f"{1920}x{1080}")

		# configure grid layout (4x4)
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(1, weight=1)

		header_padding_x = (5, 5)
		header_padding_y = (10, 10)
		
		self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
		self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
		self.sidebar_frame.grid_columnconfigure(4, weight=1)
		self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="COSU Manager", font=customtkinter.CTkFont(size=20, weight="bold"))
		self.logo_label.grid(row=0, column=0, padx=(20, 10), pady=header_padding_y)
		self.save_button = customtkinter.CTkButton(self.sidebar_frame, text="Save", width=60, command=self.save_project)
		self.save_button.grid(row=0, column=1, padx=header_padding_x, pady=header_padding_y)
		self.load_button = customtkinter.CTkButton(self.sidebar_frame, text="Load", width=60, command=self.load_project)
		self.load_button.grid(row=0, column=2, padx=header_padding_x, pady=header_padding_y)
		
		# 4 is service URL
		self.service_label = customtkinter.CTkLabel(self.sidebar_frame, text="Service:", anchor="w")
		self.service_label.grid(row=0, column=3, padx=(80, 5), pady=header_padding_y)
		self.service_url = customtkinter.CTkEntry(self.sidebar_frame, textvariable=self.option_manager.get("url"))
		self.service_url.grid(row=0, column=4, columnspan=1, padx=header_padding_x, pady=header_padding_y, sticky="nsew")
		refresh_image = customtkinter.CTkImage(Image.open(os.path.join("./images", "refresh.png")), size=(20, 20))
		self.refresh_button = customtkinter.CTkButton(self.sidebar_frame, text=None, width=30, image=refresh_image, command=self.load)
		ctt(self.refresh_button, delay=0.1, alpha=0.95, message="Connect to Service")
		self.refresh_button.grid(row=0, column=5, padx=header_padding_x, pady=header_padding_y)

		self.algorithm_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, variable=self.option_manager.get_mode_sv(), values=self.option_manager.get_service_modes(), width=50, command=self.refresh_step_view)
		self.algorithm_optionmenu.grid(row=0, column=6, padx=(5, 80), pady=header_padding_y)
		
		self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Scale:", anchor="w")
		self.scaling_label.grid(row=0, column=7, padx=header_padding_x, pady=header_padding_y)
		self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["50%", "75%", "100%", "125%", "150%", "175%", "200%"], width=60,
																command=self.change_scaling_event)
		self.scaling_optionemenu.grid(row=0, column=8, padx=(5, 20), pady=header_padding_y)
		self.scaling_optionemenu.set("100%")
		
		expand_image = customtkinter.CTkImage(Image.open(os.path.join("./images", "expand.png")), size=(20, 20))
		#self.new_window = customtkinter.CTkButton(self.sidebar_frame, text=None, width=30, image=expand_image, command=self.open_new_window)
		#ctt(self.new_window, delay=0.1, alpha=0.95, message="Open New Window")
		#self.new_window.grid(row=0, column=9, padx=(5, 20), pady=header_padding_y)
		
		self.tabview = customtkinter.CTkTabview(self, bg_color="transparent", fg_color="transparent")
		self.tabview.grid(row=1, column=0, padx=(0, 0), pady=(10, 10), sticky="nsew")
		tab1 = "Platform"
		tab2 = "Setup"
		tab3 = "Logs"
		tab4 = "Results"
		
		self.tabview.add(tab1)
		self.tabview.add(tab2)
		self.tabview.add(tab4)
		self.tabview.add(tab3)
		
		pt.create_tab(self, self.tabview.tab(tab1))
		st.create_tab(self, self.tabview.tab(tab2))
		rt.create_tab(self, self.tabview.tab(tab3))
		vt.create_tab(self, self.tabview.tab(tab4))
		
		self.footer_frame = customtkinter.CTkFrame(self, corner_radius=0)
		self.footer_frame.grid(row=2, column=0, sticky="nsew")
		self.footer_frame.grid_columnconfigure(4, weight=1)
		
		self.footer_progress_label = customtkinter.CTkLabel(self.footer_frame, text="Stopped", width=150, font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
		self.footer_progress_label.grid(row=0, column=0, padx=(20, 5), pady=header_padding_y)

		self.footer_progress_bar = customtkinter.CTkProgressBar(self.footer_frame)
		self.footer_progress_bar.grid(row=0, column=4, padx=(50, 100), pady=header_padding_y, sticky="ew")
		self.footer_progress_bar.set(0)

		play_image = customtkinter.CTkImage(Image.open(os.path.join("./images", "play.png")), size=(20, 20))
		self.run_button = customtkinter.CTkButton(self.footer_frame, text=None, width=30, image=play_image, command=self.run)
		ctt(self.run_button, delay=0.1, alpha=0.95, message="Start Job")
		self.run_button.grid(row=0, column=7, padx=(20, 5), pady=header_padding_y)

		test_image = customtkinter.CTkImage(Image.open(os.path.join("./images", "test.png")), size=(20, 20))
		self.test_button = customtkinter.CTkButton(self.footer_frame, text=None, width=30, image=test_image, command=self.run_test)
		ctt(self.test_button, delay=0.1, alpha=0.95, message="Start Testing")
		self.test_button.grid(row=0, column=8, padx=(5, 5), pady=header_padding_y)
		
		stop_image = customtkinter.CTkImage(Image.open(os.path.join("./images", "stop.png")), size=(20, 20))
		self.stop_button = customtkinter.CTkButton(self.footer_frame, text=None, width=30, image=stop_image, command=self.stop)
		ctt(self.stop_button, delay=0.1, alpha=0.95, message="Stop")
		self.stop_button.grid(row=0, column=9, padx=(5, 20), pady=header_padding_y)

		download_image = customtkinter.CTkImage(Image.open(os.path.join("./images", "down.png")), size=(20, 20))
		self.download_button = customtkinter.CTkButton(self.footer_frame, text=None, width=30, image=download_image, command=self.stop)
		ctt(self.download_button, delay=0.1, alpha=0.95, message="Download Results")
		self.download_button.grid(row=0, column=10, padx=(5, 20), pady=header_padding_y)

		self.after(1000, self.running_loop)

	def update_graph(self, value):
		self.vis_sidebar.refresh()
		GraphGenerator.generate_graphs(self)
			
	def save_project(self):
		filename = asksaveasfilename(filetypes=[("JSON", "*.json")], initialfile="config", defaultextension="json", title="Save Project")
		
		try:
			self.option_manager.set_path(filename)
			self.option_manager.save_project(filename)

			folder = self.option_manager.get_project_folder()
			if not os.path.exists(folder):
				os.makedirs(folder)

			if not os.path.exists(os.path.join(folder, "results")):
				os.makedirs(os.path.join(folder, "results"))
				
			self.save_button.configure(text="Saved!")
			self.after(3000, lambda: self.save_button.configure(text="Save"))
		except Exception as e:
			self.save_button.configure(text="Error!")
			print(e)
			self.after(3000, lambda: self.save_button.configure(text="Save"))
	
	def refresh_step_view(self, value):
		mode = self.option_manager.get_mode()
		self.service_url.configure(textvariable=self.option_manager.get("url"))
		self.graph_theme.configure(variable=self.option_manager.get("graph_theme"))
		self.graph_selector.configure(variable=self.option_manager.get("selected_graph"))

		if mode == "Optimization":
			self.test_button.configure(state="normal")
			self.test_button.configure(fg_color=get_color("CTkButton"))
			self.download_button.configure(state="normal")
			self.download_button.configure(fg_color=get_color("CTkButton"))
		else:
			self.test_button.configure(state="disabled")
			self.test_button.configure(fg_color="gray")
			self.download_button.configure(state="disabled")
			self.download_button.configure(fg_color="gray")

		self.vis_sidebar.clear()
		self.vis_sidebar.render()

		self.steps_frame.clear()
		self.steps_frame.render()

		self.static_param_frame.clear()
		self.static_param_frame.render()
		
		self.calib_param_frame.clear()
		self.calib_param_frame.render()

		self.service_param_frame.clear()
		self.service_param_frame.render()

		#self.optimal_param_frame.clear()
		#self.optimal_param_frame.render()

	def open_new_window(self):
		# Shell out and run ./main.py
		subprocess.Popen(["python3", "../mgpsogui.py"])
	
	def load_project(self):
		
		filename = askopenfilename(filetypes=[("JSON", "*.json")], title="Open Project", multiple=False)
		print(filename)
		
		try:
		
			self.option_manager.load_project(filename)
			self.option_manager.set_path(filename)

			folder = self.option_manager.get_project_folder()
			if not os.path.exists(folder):
				os.makedirs(folder)

			if not os.path.exists(os.path.join(folder, "results")):
				os.makedirs(os.path.join(folder, "results"))
			
			self.refresh_step_view(0)
			
			self.load_button.configure(text="Loaded!")
			self.after(3000, lambda: self.load_button.configure(text="Load"))

			self.load()
			
		except Exception as e:
			print(e)
			# Print stack trace 
			traceback.print_exc()
			

			self.load_button.configure(text="Error!")
			self.after(3000, lambda: self.load_button.configure(text="Load"))

	def change_appearance_mode_event(self, new_appearance_mode: str):
		customtkinter.set_appearance_mode(new_appearance_mode)

	def change_scaling_event(self, new_scaling: str):
		new_scaling_float = int(new_scaling.replace("%", "")) / 100
		customtkinter.set_widget_scaling(new_scaling_float)
		
	def change_scaling_event(self, new_scaling: str):
		new_scaling_float = int(new_scaling.replace("%", "")) / 100
		customtkinter.set_widget_scaling(new_scaling_float)
		
	def make_request(self):
		service_url = self.service_url.get()
		try:
			response = requests.get(service_url, timeout=5)
				
			response_json = json.loads(response.text)
			status = response.status_code
			
			self.option_manager.set_data("service_request_data", response_json)
			
			self.service_status.delete('0.0', tk.END)
			self.service_status.insert(text=str(status), index='0.0')
			self.service_name.delete('0.0', tk.END)
			self.service_name.insert(text=str(response_json["metainfo"]["name"]), index='0.0')
			self.service_description.delete('0.0', tk.END)
			self.service_description.insert(text=str(response_json["metainfo"]["description"]), index='0.0')
			self.service_details.delete('0.0', tk.END)
			self.service_details.insert(text=json.dumps(response_json, indent=4), index='0.0')

			self.refresh_button.configure(fg_color="green")
		except Exception as e:
			self.refresh_button.configure(fg_color="red")
			self.after(1000, lambda: self.refresh_button.configure(fg_color=get_color("CTkButton")))

		self.refresh_step_view(0)
		
	
	def load(self):
		# Make HTTP request to service_url and save the result to bounds.json
		
		self.refresh_button.configure(fg_color="gray")
		
		self.after(10, self.make_request)
		self.after(3000, lambda: self.refresh_button.configure(fg_color=get_color("CTkButton")))
		
	def run_test(self):
		self.testing = True
		self.run()	

	def run(self):
		
		data = self.option_manager.get_all_data()
		mode = self.option_manager.get_mode()
		data = data[mode]

		self.running_config = data
		
		#if self.testing:
		#	steps = metrics['steps']
		#	for step in steps:
		#		for param in step['param']:
		#			param['default_value'] = param['optimal_value']
		self.testing = False

		self.progress_data = None
		self.calibration_data = None

		#self.progress_bar.configure(mode="indeterminnate")
		#self.progress_bar.start()
		self.footer_progress_bar.configure(mode="indeterminnate")
		self.footer_progress_bar.start()
		
		self.data_x = [0]
		self.data_y = [0]
		
		#self.progress_message_middle.configure(text="Job starting...")
		self.footer_progress_label.configure(text="Starting...")
		
		self.textbox.insert("0.0", "Starting job...\n\n")
		self.textbox.insert("0.0", "Job Parameters:\n")
		self.textbox.insert("0.0", json.dumps(data, indent=4) + "\n\n")
		try:
			folder = self.option_manager.get_project_folder()
			
			self.train_process = Process(target=PSORunner.run_process, args=(stdout_queue, stderr_queue, results_queue, data, folder, mode))
			self.train_process.daemon = True
			self.train_process.start()
			self.after(1000, self.watch_loop)
			self.string_cache = ""
			self.data_cache = ""
			
		except Exception as e:
			self.textbox.insert("0.0", "An exception occurred!\n Exception: " + str(e) + "\n\n")
			self.textbox.insert("0.0", "Stack trace:\n")
			self.textbox.insert("0.0", traceback.format_exc())
			self.textbox.insert("0.0", "\n\n")
			self.textbox.insert("0.0", "Job failed!")
			#self.progress_message_left.configure(text="")
			#self.progress_message_middle.configure(text="Job failed! See error log below.")
			#self.progress_message_right.configure(text="")
			self.footer_progress_label.configure(text="Failed")
			#self.progress_bar.stop()
			self.footer_progress_bar.stop()
			#self.progress_bar.configure(mode="determinate")
			self.footer_progress_bar.configure(mode="determinate")
			#self.progress_bar.set(0)
			self.footer_progress_bar.set(0)
	
			
	def stop(self):
		print("Stopping...")
		self.train_process.terminate()
		
		folder = self.option_manager.get_project_folder()
			
		if not os.path.exists(folder):
			os.makedirs(folder)
		
		# Stop the process
		#if (os.path.exists(os.path.join(folder, 'output.txt'))):
		#	os.remove(os.path.join(folder, 'output.txt'))
		
		#if (os.path.exists(os.path.join(folder, 'error.txt'))):
		#	os.remove(os.path.join(folder, 'error.txt'))
			
		self.textbox.insert("0.0", "Job terminated!\n")
		#self.progress_bar.stop()
		self.footer_progress_bar.stop()
		#self.progress_bar.configure(mode="determinate")
		self.footer_progress_bar.configure(mode="determinate")
		#self.progress_bar.set(0)
		self.footer_progress_bar.set(0)
		#self.progress_message_left.configure(text="")
		#self.progress_message_middle.configure(text="Job stopped!")
		self.footer_progress_label.configure(text="Stopped")
		#self.progress_message_right.configure(text="")
		
	def running_loop(self):
		try:
			active_tab = self.tabview.get()
			if (active_tab == "Results"):
				GraphGenerator.generate_graphs(self)
		finally:
			self.after(1000, self.running_loop)

	def watch_loop(self):
		print("Watch loop running...")

		folder = self.option_manager.get_project_folder()
			
		if not os.path.exists(folder):
			os.makedirs(folder)
			
		while True:
			try:
				stdout_line = stdout_queue.get_nowait()
				
				print("# " + stdout_line, flush=True)
				with open(os.path.join(folder, 'output.txt'), 'a') as f:
					f.write(stdout_line)
			except Empty:
				break
			
		while True:
			try:
				stderr_line = stderr_queue.get_nowait()
				print("? " + stderr_line, flush=True)
				with open(os.path.join(folder, 'error.txt'), 'a') as f:
					f.write(stderr_line)
				
			except Empty:
				break

		while True:
			try:
				trace = results_queue.get_nowait()
				
				print("TRACE " + str(trace), flush=True)
	
				final_results = hp.extract_final_round_values(trace)
				print("Final results: " + str(final_results), flush=True)
	
				all_steps = self.option_manager.get_steps()
				data = final_results["data"]
				index = 0
				for step in data:
					for param in step.keys():
						value = step[param]
						target_step = all_steps[index]
						for target_param in target_step['parameter_objects']:
							if target_param['name'].get() == param:
								target_param['optimal_value'].set(value)
					index += 1
				print("Applied optimal values")
			except Empty:
				break
			except Exception as e:
				print("Some error happened when getting the trace!")
				print(e)
		
		# Write output to textbox
		if (os.path.exists(os.path.join(folder, 'output.txt'))):
			with open(os.path.join(folder, 'output.txt'), 'r') as f:
				lines = f.readlines()
				lines_string = "".join(lines)
				
				new_characters = lines_string.replace(self.string_cache, "")
				# Update the textbox with characters not in self.string_cache
				self.textbox.insert('0.0', new_characters)
				self.string_cache = lines_string
				print(new_characters, end="")
				
			try:
				# REPLACE THIS WITH READING THE STEP TRACE JSON for PSO
				with open(os.path.join(folder, "output.txt"), "r") as f:
					text = f.read()

				calibrated_params_pattern = r"calibrated params: ({.*?})"
				best_particle_values_pattern = r"best particle values: (\[.*?\])"
				progress_pattern = r"Progress -  best_round_cost:(.*?), rel_round_tol:(.*?), rtol:(.*?)\n"

				calibrated_params = re.findall(calibrated_params_pattern, text)
				best_particle_values = re.findall(best_particle_values_pattern, text)
				progress_values = re.findall(progress_pattern, text)

				for index, pp in enumerate(best_particle_values):
					pp = pp.strip()
					pp = pp.replace('[ ', '[')
					pp = pp.replace('  ', ',')
					pp = pp.replace(' ', ',')
					best_particle_values[index] = pp

				calibrated_params = [ast.literal_eval(i) for i in calibrated_params]
				best_particle_values = [ast.literal_eval(i) for i in best_particle_values]
				progress_values = [tuple(map(float, i)) for i in progress_values]
				self.calibration_data = calibrated_params
				
			except Exception as e:
				traceback.print_exc()
				print(e)
				
		# Parse data into interface
		mode = self.option_manager.get_mode()
		if mode == "Optimization":
			if (os.path.exists(os.path.join(folder, 'error.txt'))):
				data = hp.parse_pso_error(os.path.join(folder, 'error.txt'), len(self.option_manager.get_steps()))
				print(data)
				self.progress_data = data["data"]
				self.footer_progress_bar.stop()
				self.footer_progress_bar.configure(mode="determinate")
				self.footer_progress_bar.set(data["percent"]/100)
				self.footer_progress_label.configure(text="Round: " + str(data["round"]) + " - Step: " + str(data["step"]))
		else:
			if (os.path.exists(os.path.join(folder, 'output.txt'))):
				data = hp.parse_sampling_output(os.path.join(folder, 'output.txt'))
				print(data)
				self.footer_progress_bar.stop()
				self.footer_progress_bar.configure(mode="determinate")
				self.footer_progress_bar.set(data["percent"]/100)
				self.footer_progress_label.configure(text=str(round(data["percent"])) + "%")
				
				
				
		if self.train_process.is_alive():
			self.after(1000, self.watch_loop)
		else:
			#self.progress_bar.stop()
			self.footer_progress_bar.stop()
			#self.progress_bar.configure(mode="indeterminate")
			self.footer_progress_bar.configure(mode="indeterminate")
			#self.progress_bar.start()
			self.footer_progress_bar.start()
			#self.progress_message_left.configure(text="")
			#self.progress_message_middle.configure(text="Job finished!")
			#self.progress_message_right.configure(text="")
			self.textbox.insert("0.0", "\nJob finished!\n")

			# IF "./crash.txt" exists write it to the textbox
			if (os.path.exists(os.path.join(folder, 'crash.txt'))):
				with open(os.path.join(folder, 'crash.txt'), 'r') as f:
					lines = f.readlines()
					lines_string = "".join(lines)
					print("CRASH OCCURRED!")
					print(lines_string)
					self.textbox.insert('0.0', lines_string)
					self.textbox.insert('0.0', "CRASH OCCURRED!\n")
				# Delete the file
				os.remove(os.path.join(folder, 'crash.txt'))

def get_color(class_name, property = "fg_color"):
    return ThemeManager.theme[class_name][property]

def start():
	app = App()
	app.mainloop()

if __name__ == "__main__":
	app = App()
	app.mainloop()