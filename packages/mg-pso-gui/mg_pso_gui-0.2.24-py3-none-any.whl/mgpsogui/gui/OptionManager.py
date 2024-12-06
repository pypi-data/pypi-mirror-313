from tkinter import StringVar as sv
import json
import os

class OptionManager():
    
    def __init__(self):

        self._service_modes = ["Sampling: Halton", "Sampling: Random", "Sensitivity Analysis", "Optimization"]

        self._default_sampling = json.load(open(os.path.join("./defaults", "sampling.json")))
        self._default_sensitivity = json.load(open(os.path.join("./defaults", "sensitivity.json")))
        self._default_optimization = json.load(open(os.path.join("./defaults", "optimization.json")))

        self._mode_sv = sv()
        self.init_lists()

    def init_lists(self): 
        self._project_data = {"name": "", "path": ""}
        self._data = {}

        self._mode_sv.set("Sampling: Halton")

        for service in self._service_modes:
            self._data[service] = {
                    "url": sv(),
                    "files": {},
                    "steps": [],
                    "model_parameters": [],
                    "hyperparameters": [],
                    "service_parameters": [],
                    "service_request_data": [],
                    "figure_parameters": [],
                    "sensitivity_parameters": [],
                    "sensitivity_positiveBestMetrics": [],
                    "sensitivity_negativeBestMetrics": [],

                    "sensitivity_analysis_path": sv(),
                    "sampling_output_mode": sv(),
                    "selected_graph": sv(),
                    "graph_theme": sv(),
                    "selected_csv": sv(),
                    "selected_csv2": sv(),
                    "selected_x": sv(),
                    "selected_y1": sv(),
                    "selected_y2": sv(),
                    "figure_style": sv(),
                    "matrix_values": []}
            
            self._data[service]["selected_graph"].set("Best Cost Stacked")
            self._data[service]["graph_theme"].set("Dark")
            self._data[service]["selected_csv"].set("No files found...")
            self._data[service]["selected_csv2"].set("No files found...")
            self._data[service]["selected_x"].set("time")
            self._data[service]["selected_y1"].set("NONE")
            self._data[service]["selected_y2"].set("NONE")
            self._data[service]["figure_style"].set("Scatter")
            self._data[service]["matrix_values"].append(sv())
            self._data[service]["matrix_values"][0].set("NONE")

            
            if service == "Sampling: Halton" or service == "Sampling: Random":
                self._data[service]["model_parameters"] = self.deserialize_data(self._default_sampling["model_parameters"])
                self._data[service]["hyperparameters"] = self.deserialize_data(self._default_sampling["hyperparameters"])
                self._data[service]["service_parameters"] = self.deserialize_data(self._default_sampling["service_parameters"])
            elif service == "Sensitivity Analysis":
                self._data[service]["model_parameters"] = self.deserialize_data(self._default_sensitivity["model_parameters"])
                self._data[service]["hyperparameters"] = self.deserialize_data(self._default_sensitivity["hyperparameters"])
                self._data[service]["service_parameters"] = self.deserialize_data(self._default_sensitivity["service_parameters"])
            elif service == "Optimization":
                self._data[service]["model_parameters"] = self.deserialize_data(self._default_optimization["model_parameters"])
                self._data[service]["hyperparameters"] = self.deserialize_data(self._default_optimization["hyperparameters"])
                self._data[service]["service_parameters"] = self.deserialize_data(self._default_optimization["service_parameters"])

            
    def serialize_data(self, data):
        if isinstance(data, dict):
            return {key: self.serialize_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.serialize_data(item) for item in data]
        elif isinstance(data, sv):
            return data.get()
        else:
            return data
        
    def deserialize_data(self, data):
        if isinstance(data, dict):
            return {key: self.deserialize_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.deserialize_data(item) for item in data]
        elif isinstance(data, (str, int, float)):
            return sv(value=str(data))
        else:
            return data
        
    def save_project(self, filename):
        with open(filename, 'w') as file:
            results = {"project_data": self._project_data, 
                       "mode": self._mode_sv.get(),
                       "data": self.serialize_data(self._data)}
            json.dump(results, file)

    def get_all_data(self):
        return self.serialize_data(self._data)

    def load_project(self, filename):
        self._mode_sv = sv()
        self.init_lists()

        with open(filename, 'r') as file:
            results = json.load(file)
            new_project_data = results["project_data"]
            for key, value in new_project_data.items():
                self._project_data[key] = value
            self._mode_sv.set(results["mode"])
            new_data = self.deserialize_data(results["data"])
            for key, value in new_data.items():
                self._data[key] = value


    def add_arguments(self, arguments):
            
        if ("mode" in arguments):
            self._data["mode"].set(arguments["mode"])

        if ("url" in arguments):
            self._data["url"][self._data["mode"].get()].set(arguments["url"])
            
        if ("files" in arguments):
            for file in arguments["files"]:
                name = file["name"]
                value = file["value"]
                obj = {"name": sv(), "value": sv()}
                obj["name"].set(name)
                obj["value"].set(value)
                self._data["files"][name] = obj
        
        for param in arguments["model_parameters"]:
            name = param["name"]
            value = param["value"]
            obj = {"name": sv(), "value": sv()}
            obj["name"].set(name)
            obj["value"].set(value)
            self._data["model_parameters"].append(obj)
            
        for param in arguments["hyperparameters"]:
            name = param["name"]
            value = param["value"]
            obj = {"name": sv(), "value": sv()}
            obj["name"].set(name)
            obj["value"].set(value)
            self._data["hyperparameters"].append(obj)

        for param in arguments["service_parameters"]:
            name = param["name"]
            value = param["value"]
            obj = {"name": sv(), "value": sv()}
            obj["name"].set(name)
            obj["value"].set(value)
            self._data["service_parameters"].append(obj)
            
    def add_steps(self, steps):
        for step in steps:
            obj = {"parameter_objects": [], 
                    "override_parameter": [],
                    "objective_functions": [], 
                    "name": sv(), 
                    "open": True}
            obj["name"].set("Group " + str(len(self._data[self._mode_sv.get()]["steps"]) + 1))
            
            if "parameter_objects" in step:
                for param in step["parameter_objects"]:
                    param_obj = {
                        "name": sv(), 
                        "min_bound": sv(),
                        "max_bound": sv(),
                        "default_value": sv(), 
                        "optimal_value": sv(), 
                        "type": sv(),
                        "calibration_strategy": sv()
                    }
                    param_obj["name"].set(param["name"])

                    if "min_bound" in param:
                        param_obj["min_bound"].set(param["min_bound"]) 
                    else: 
                        param_obj["min_bound"].set(0)

                    if "max_bound" in param:
                        param_obj["max_bound"].set(param["max_bound"]) 
                    else: 
                        param_obj["max_bound"].set(0)
                        
                    if "type" in param:
                        param_obj["type"].set(param["type"])
                    else:
                        param_obj["type"].set("float")
                        
                    if "default_value" in param:
                        param_obj["default_value"].set(param["default_value"])
                    else:
                        param_obj["default_value"].set(1)
                        
                    if "optimal_value" in param:
                        param_obj["optimal_value"].set(param["optimal_value"])
                    else:
                        param_obj["optimal_value"].set(0)
                        
                    if "calibration_strategy" in param:
                        param_obj["calibration_strategy"].set(param["calibration_strategy"])
                    else:
                        param_obj["calibration_strategy"].set("none")
                        
                    obj["parameter_objects"].append(param_obj)
            
            if "override_parameter" in step:
                for override in step["override_parameter"]:
                    override_obj = {"name": sv(), "value": sv()}
                    override_obj['name'].set(override['name'])
                    override_obj['value'].set(override['value'])
                    obj['override_parameter'].append(override_obj)

            if "objective_functions" in step:
                for objective_function in step["objective_functions"]:
                    objective_function_object = {"name": sv(), 
                                    "objective_function": sv(), 
                                    "weight": sv(), 
                                    "custom_function": sv(),
                                    "custom_function_goal": sv(),
                                    "custom_function_value": sv(),
                                    "data_observed": sv(),
                                    "data_simulated": sv()}
                    objective_function_object["name"].set(objective_function["name"])
                    objective_function_object["objective_function"].set(objective_function["objective_function"])
                    objective_function_object["custom_function_goal"].set("Positive Best")
                    
                    if ("weight" in objective_function): 
                        objective_function_object["weight"].set(objective_function["weight"])
                    else:
                        objective_function_object["weight"].set(1)
                        
                    if ("custom_function" in objective_function):
                        objective_function_object["custom_function"].set(objective_function["custom_function"])
                    if ("custom_function_goal" in objective_function):
                        objective_function_object["custom_function_goal"].set(objective_function["custom_function_goal"])
                    if ("custom_function_value" in objective_function):
                        objective_function_object["custom_function_value"].set(objective_function["custom_function_value"])

                    objective_function_object["data_observed"].set(objective_function["data_observed"])
                    objective_function_object["data_simulated"].set(objective_function["data_simulated"]) 
                    obj["objective_functions"].append(objective_function_object)
            
            self._data[self._mode_sv.get()]["steps"].append(obj)
    
    def add_function(self, step_index):
        obj = {"name": sv(), 
                "objective_function": sv(), 
                "weight": sv(), 
                "custom_function": sv(),
                "data_observed": sv(),
                "data_simulated": sv()}
        obj["name"].set("ns")
        obj["objective_function"].set("ns")
        obj["weight"].set(1)
        obj["data_observed"].set("")
        obj["data_simulated"].set("")
        obj["custom_function"].set("") 
        
        self._data[self._mode_sv.get()]["steps"][step_index]["objective_functions"].append(obj)
        
    def remove_function(self, step_index, index):
        self._data[self._mode_sv.get()]["steps"][step_index]["objective_functions"].pop(index)
        
    def dupe_function(self, step_index, index):
        my_func = self._data[self._mode_sv.get()]["steps"][step_index]["objective_functions"][index]
        
        new_object = {"name": sv(), 
                        "objective_function": sv(), 
                        "weight": sv(), 
                        "custom_function": sv(),
                        "custom_function_goal": sv(),
                        "custom_function_value": sv(),
                        "data_observed": sv(),
                        "data_simulated": sv()}
        new_object["name"].set(my_func["name"].get())
        new_object["objective_function"].set(my_func["objective_function"].get())
        new_object["weight"].set(my_func["weight"].get())
        new_object["data_observed"].set(my_func["data_observed"].get())
        new_object["data_simulated"].set(my_func["data_simulated"].get())
        new_object["custom_function"].set(my_func["custom_function"].get())
        new_object["custom_function_goal"].set(my_func["custom_function_goal"].get())
        new_object["custom_function_value"].set(my_func["custom_function_value"].get())
        
        self._data[self._mode_sv.get()]["steps"][step_index]["objective_functions"].append(new_object)
    
    def add_bound(self, step_index, 
                  name="name", 
                  min=0, 
                  max=1,
                  type="float",
                  default_value=1,
                  optimal_value=0,
                  calibration_strategy="none"):
        obj = {
            "name": sv(), 
            "min_bound": sv(),
            "max_bound": sv(),
            "default_value": sv(), 
            "optimal_value": sv(),
            "type": sv(),
            "calibration_strategy": sv()
        }
        obj["name"].set(name)
        obj["type"].set(type)
        obj["default_value"].set(default_value)
        obj["optimal_value"].set(optimal_value)
        obj["calibration_strategy"].set(calibration_strategy)
        obj["min_bound"].set(min)
        obj["max_bound"].set(max)
        self._data[self._mode_sv.get()]["steps"][step_index]["parameter_objects"].append(obj)
        
    def remove_bound(self, step_index, index):
        self._data[self._mode_sv.get()]["steps"][step_index]["parameter_objects"].pop(index)
        
    def add_override(self, step_index, name, value):
        obj = {"name": sv(), "value": sv()}
        obj["name"].set(name)
        obj["value"].set(value)
        self._data[self._mode_sv.get()]["steps"][step_index]["override_parameter"].append(obj)

    def remove_override(self, step_index, index):
        self._data[self._mode_sv.get()]["steps"][step_index]["override_parameter"].pop(index)

    def get_override(self, step_index):
        return self._data[self._mode_sv.get()]["steps"][step_index]["override_parameter"]

    def add_key_value(self, list_name, key, value, type="string", destination="args"):
        obj = {"name": sv(), "value": sv(), "type": sv(), "destination": sv()}
        obj["name"].set(key)
        obj["value"].set(value)
        obj["type"].set(type)
        obj["destination"].set(destination)
        self._data[self._mode_sv.get()][list_name].append(obj)

    def remove_key_value(self, list_name, index):
        self._data[self._mode_sv.get()][list_name].pop(index)
            
    def move_step_up(self, index):
        if index > 0:
            self._data[self._mode_sv.get()]["steps"][index], self._data[self._mode_sv.get()]["steps"][index - 1] = self._data[self._mode_sv.get()]["steps"][index - 1], self._data[self._mode_sv.get()]["steps"][index]
            
    def move_step_down(self, index):
        if index < len(self._data[self._mode_sv.get()]["steps"]) - 1:
            self._data[self._mode_sv.get()]["steps"][index], self._data[self._mode_sv.get()]["steps"][index + 1] = self._data[self._mode_sv.get()]["steps"][index + 1], self._data[self._mode_sv.get()]["steps"][index]
            
    def toggle_step_open(self, index):
        self._data[self._mode_sv.get()]["steps"][index]["open"] = not self._data[self._mode_sv.get()]["steps"][index]["open"]

    def remove_step(self, index):
        self._data[self._mode_sv.get()][self._mode_sv.get()]["steps"].pop(index)
            
    def get_project_data(self):
        return self._project_data
            
    def set_path(self, filename):
        file_name = filename.split("/")[-1].replace(".json", "")
        path = filename.replace(file_name + ".json", "")
        self._project_data["path"] = path
        self._project_data["name"] = file_name
            
    def get_data(self):
        return self._data[self._mode_sv.get()]
    
    def get_steps(self):
        return self._data[self._mode_sv.get()]["steps"]
    
    def get_mode(self):
        return self._mode_sv.get()
    
    def get_mode_sv(self):
        return self._mode_sv
    
    def get_service_modes(self):
        return self._service_modes
    
    def get_list(self, list_name):
        return self._data[self._mode_sv.get()][list_name]
    
    def get(self, key):
        return self._data[self._mode_sv.get()][key]
    
    def set_data(self, key, value):
        self._data[self._mode_sv.get()][key] = value

    def set_var(self, key, value):
        self._data[self._mode_sv.get()][key].set(value)
        
    def get_all_as_json(self):
        obj = {"arguments": self._data, "steps": self._data[self._mode_sv.get()]["steps"]}
        return obj
    
    def get_project_folder(self):
        return os.path.join(self._project_data['path'], self._project_data['name'])

    
    def get_metrics(self):

        self._data["url"].set(self._data["urls"][self._data["mode"].get()].get())

        result = {}
        result['arguments'] = {}
        result['hyperparameters'] = []
        result['service_parameters'] = []
        result['service_parameters'] = {}
        result['project_data'] = self._project_data
        for key, value in self._data.items():
            if key == 'url' or key == 'mode':
                result['arguments'][key] = value.get()
            elif key == 'files':
                result['arguments'][key] = {}
                #for name, obj in value.items():
                #    result['arguments'][key].append({'name': obj['name'].get(), 'value': obj['value'].get()})
            elif key == 'param':
                result['arguments'][key] = []
                for obj in value:
                    result['arguments'][key].append({'name': obj['name'].get(), 'value': obj['value'].get()})
            elif key == "hyperparameters":
                #result['hyperparameters'][key] = []
                for obj in value:
                    result['hyperparameters'].append({'name': obj['name'].get(), 'value': obj['value'].get()})
            elif key == "service_parameters":
                #result['service_parameters'][key] = []
                for obj in value:
                    result['service_parameters'].append({'name': obj['name'].get(), 'value': obj['value'].get()})
        result['steps'] = []
        for step in self._data[self._mode_sv.get()]["steps"]:
            step_result = {}
            #step_result['name'] = step['name'].get()
            #step_result['open'] = step['open']
            step_result['param'] = []
            for param in step['param']:
                # try converting the bounds to numbers
                #try:
                if param['type'].get() == 'float':
                    step_result['param'].append(
                        {
                            'name': param['name'].get(), 
                            'bounds': (float(param['bounds'][0].get()), 
                                       float(param['bounds'][1].get())),
                            'default_value': float(param['default_value'].get()),
                            'optimal_value': float(param['optimal_value'].get()),
                            'type': 'float',
                            'calibration_strategy': param['calibration_strategy'].get()
                        }
                    )
                elif param['type'].get() == 'list':
                    step_result['param'].append(
                        {
                            'name': param['name'].get(), 
                            'bounds': (float(param['bounds'][0].get()), 
                                       float(param['bounds'][1].get())),
                            'default_value': param['default_value'].get(),
                            'optimal_value': param['optimal_value'].get(),
                            'type': 'list',
                            'calibration_strategy': param['calibration_strategy'].get()
                        }
                    )
            step_result['objfunc'] = []
            for objfunc in step['objfunc']:
                step_result['objfunc'].append({'name': objfunc['name'].get(), 'of': objfunc['of'].get(), 'weight': float(objfunc['weight'].get()), 'data': (objfunc['data'][0].get(), objfunc['data'][1].get())})
            result['steps'].append(step_result)
        return result