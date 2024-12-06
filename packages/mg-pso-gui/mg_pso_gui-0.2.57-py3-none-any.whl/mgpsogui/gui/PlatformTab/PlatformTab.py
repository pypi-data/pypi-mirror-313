import requests
import json
import os
import subprocess
import customtkinter
import platform

from ..General import ParameterView as pv

import tkinter as tk

def create_tab(self, tab):
    
    def make_request():
        service_url = self.service_url.get()
        response = requests.get(service_url)
            
        response_json = json.loads(response.text)
        status = response.status_code
        
        self.option_manager.set_data(response_json)
        self.tabview.configure(state="enabled")
        
        self.service_status.delete('0.0', tk.END)
        self.service_status.insert(text=str(status), index='0.0')
        self.service_name.delete('0.0', tk.END)
        self.service_name.insert(text=str(response_json["metainfo"]["name"]), index='0.0')
        self.service_description.delete('0.0', tk.END)
        self.service_description.insert(text=str(response_json["metainfo"]["description"]), index='0.0')
        self.service_details.delete('0.0', tk.END)
        self.service_details.insert(text=json.dumps(response_json, indent=4), index='0.0')
        
        self.load_parameters.configure(text="Loaded!")
    
    def load():
        # Make HTTP request to service_url and save the result to bounds.json
        self.load_parameters.configure(text="Loading...")
        self.after(10, make_request)
        self.after(3000, lambda: self.load_parameters.configure(text="Connect"))
        
    def start_cluster():
        process = subprocess.Popen(["minikube", "start"], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print(f"An error occurred: {error}")
            self.custer_details.insert("0.0", error.decode('unicode-escape') + "\n\n")
        else:
            print(f"Output: {output}")
            self.custer_details.insert("0.0", output.decode('unicode-escape') + "\n\n")
            
        process = subprocess.Popen(["minikube", "kubectl", "--", "create", "namespace", "csip"], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print(f"An error occurred: {error}")
            self.custer_details.insert("0.0", error.decode('unicode-escape') + "\n\n")
        else:
            print(f"Output: {output}")
            self.custer_details.insert("0.0", output.decode('unicode-escape') + "\n\n")
            
    def cluster_status():
        process = subprocess.Popen(["minikube", "status"], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print(f"An error occurred: {error}")
            self.custer_details.insert("0.0", error.decode('unicode-escape') + "\n\n")
        else:
            print(f"Output: {output}")
            self.custer_details.insert("0.0", output.decode('unicode-escape') + "\n\n")
            
                
    def open_terminal_and_run_cluster():
        full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'start.yaml'))
        command = "minikube kubectl -- create -f " + full_path + " ; sleep 60 ; minikube service pf8087-csu-csip-oms -n csip"
        #command = "minikube kubectl -- create -f " + full_path + " ; until [[ $(minikube kubectl -- get pods -l app=pf8087-csu-csip-oms -n csip -o \\'jsonpath={..status.conditions[?(@.type==\\\"Ready\\\")].status}\\') == \\\"True\\\" ]]; do echo \\\"waiting for pod\\\" && sleep 1; done ; minikube service pf8087-csu-csip-oms -n csip"
        
        self.create_environment_button.configure(text="Running!")
        
        os.system("osascript -e 'tell app \"Terminal\" to do script \"" + command + "\"'")
        
        self.after(3000, lambda: self.create_environment_button.configure(text="Start Environment"))
        
        # Change the service URL to /csip-oms/m/ages/0.3.0
        self.service_url.cget("textvariable").set("PASTE_URL/csip-oms/m/ages/0.3.0")
        
    def deploy_cluster():
        full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'start.yaml'))
        command = "minikube kubectl -- create -f " + full_path + " ; sleep 60 ; minikube service pf8087-csu-csip-oms -n csip"
        
        #minikube kubectl -- create -f ../start.yaml ; sleep 60 ; minikube service pf8087-csu-csip-oms -n csip
        
        # Get the full path of ../start.yamp
        full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'start.yaml'))
        command = "minikube kubectl -- create -f " + full_path + " ; sleep 60 ; minikube service pf8087-csu-csip-oms -n csip"
        
        # Put that command in your clipboard with tinkter
        self.clipboard_clear()
        self.clipboard_append(command)
        
        # Change the button text breafly to "Copied!"
        self.create_environment_button.configure(text="Copied!")
        self.after(3000, lambda: self.create_environment_button.configure(text="Copy Command"))
        
        # Change the service URL to /csip-oms/m/ages/0.3.0
        self.service_url.cget("textvariable").set("PASTE_URL/csip-oms/m/ages/0.3.0")
        
    def stop_cluster():
        process = subprocess.Popen(["minikube", "delete"], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print(f"An error occurred: {error}")
            self.custer_details.insert("0.0", error.decode('latin_1') + "\n\n")
        else:
            print(f"Output: {output}")
            self.custer_details.insert("0.0", output.decode('latin_1') + "\n\n")
    
    
    tab.grid_columnconfigure(0, weight=1)
    tab.grid_columnconfigure(1, weight=1)
    tab.grid_columnconfigure(2, weight=1)
    tab.grid_rowconfigure(0, weight=1)
    
    """
    self.top_bar_container = customtkinter.CTkFrame(tab)
    self.top_bar_container.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
    self.top_bar_container.grid_columnconfigure(1, weight=1)
    
    cl = customtkinter.CTkLabel(self.top_bar_container, text="Service URL:", anchor="w")
    cl.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="ew")
    
    self.service_url = customtkinter.CTkEntry(self.top_bar_container, textvariable=self.option_manager.get_arguments()['url'])
    self.service_url.grid(row=0, column=1, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    self.load_parameters = customtkinter.CTkButton(self.top_bar_container, text="Connect", command=load)
    self.load_parameters.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    """

    self.service_param_frame = pv.ParameterView(tab, option_manager=self.option_manager, list_name="service_parameters", label_text="Service Parameters")
    self.service_param_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    self.service_param_frame.grid_columnconfigure(0, weight=1)
    self.service_param_frame.grid_rowconfigure(0, weight=1)

            
    self.service_editor = customtkinter.CTkScrollableFrame(tab, label_text="Service Status")
    self.service_editor.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
    self.service_editor.grid_columnconfigure(0, weight=1)
    self.service_editor.grid_rowconfigure(0, weight=1)
    
    cl = customtkinter.CTkLabel(self.service_editor, text="Service Status:", anchor="w")
    cl.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.service_status = customtkinter.CTkTextbox(self.service_editor, height=32)
    self.service_status.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    cl = customtkinter.CTkLabel(self.service_editor, text="Service Name:", anchor="w")
    cl.grid(row=3, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.service_name = customtkinter.CTkTextbox(self.service_editor, height=32)
    self.service_name.grid(row=4, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    cl = customtkinter.CTkLabel(self.service_editor, text="Service Description:", anchor="w")
    cl.grid(row=5, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.service_description = customtkinter.CTkTextbox(self.service_editor, height=32)
    self.service_description.grid(row=6, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    cl = customtkinter.CTkLabel(self.service_editor, text="Service Details:", anchor="w")
    cl.grid(row=7, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.service_details = customtkinter.CTkTextbox(self.service_editor, height=480)
    self.service_details.grid(row=8, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.environment_editor = customtkinter.CTkScrollableFrame(tab, label_text="Minikube Environment Editor")
    self.environment_editor.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
    self.environment_editor.grid_columnconfigure(0, weight=1)
    self.environment_editor.grid_rowconfigure(0, weight=1)
    
    cl = customtkinter.CTkLabel(self.environment_editor, text="Cluster Preset:", anchor="w")
    cl.grid(row=0, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.preset_selector = customtkinter.CTkOptionMenu(self.environment_editor, values=["Local", "Other"])
    self.preset_selector.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    cl = customtkinter.CTkLabel(self.environment_editor, text="Controls:", anchor="w")
    cl.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.start_cluster_button = customtkinter.CTkButton(self.environment_editor, text="Start Minikube", command=start_cluster)
    self.start_cluster_button.grid(row=3, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")
    
    # Check if the os is MacOS
    if (platform.system() == "Darwin"):
        self.create_environment_button = customtkinter.CTkButton(self.environment_editor, text="Create Environment", command=open_terminal_and_run_cluster)
    else:
        self.create_environment_button = customtkinter.CTkButton(self.environment_editor, text="Copy Command", command=deploy_cluster)
        
    self.create_environment_button.grid(row=4, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")
    
    self.get_status = customtkinter.CTkButton(self.environment_editor, text="Minikube Status", command=cluster_status)
    self.get_status.grid(row=5, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")
    
    self.destroy_environment_button = customtkinter.CTkButton(self.environment_editor, text="Stop Minikube", command=stop_cluster)
    self.destroy_environment_button.grid(row=6, column=0, padx=(20, 20), pady=(5,10), sticky="ew")
    
    cl = customtkinter.CTkLabel(self.environment_editor, text="Minikube Status:", anchor="w")
    cl.grid(row=7, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.custer_details = customtkinter.CTkTextbox(self.environment_editor, height=480)
    self.custer_details.grid(row=8, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")