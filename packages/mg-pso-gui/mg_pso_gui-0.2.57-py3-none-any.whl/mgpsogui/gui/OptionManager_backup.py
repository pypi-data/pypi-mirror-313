from tkinter import StringVar as sv
from tkinter import IntVar as iv
from tkinter import BooleanVar as bv
from tkinter import DoubleVar as dv
import json

class OptionManager():
    
    def __init__(self):
        
        self.project_data = {"name": "", "path": ""}
        self.arguments = {"param": [],
                 "url": sv(),
                 "urls": {},
                 "mode": sv(),
                 "files": {},
                 "calibration_parameters": [],
                 "service_parameters": [],
                 "figure_parameters": [],
                 "sensitivity_parameters": [],
                 "sensitivity_positiveBestMetrics": [],
                 "sensitivity_negativeBestMetrics": []}
        
        self.steps = []
        self.service_parameters = {}

        self.service_modes = ["Sampling: Halton", "Sampling: Random", "Sensitivity Analysis", "Optimization"]
        for mode in self.service_modes:
            self.arguments["urls"][mode] = sv()

            
    def clear(self):
        self.arguments['param'].clear()
        self.arguments['url'].set("")
        for mode in self.service_modes:
            self.arguments["urls"][mode].set("")
        self.arguments['mode'].set("Optimization")
        self.arguments['files'] = {}
        self.arguments['calibration_parameters'].clear()
        self.arguments['service_parameters'].clear()
        self.arguments['figure_parameters'].clear()
        self.arguments['sensitivity_parameters'].clear()
        self.arguments['sensitivity_positiveBestMetrics'].clear()
        self.arguments['sensitivity_negativeBestMetrics'].clear()
        self.steps = []
        self.service_parameters = {}
    
    def add_arguments(self, arguments):
            
        if ("mode" in arguments):
            self.arguments["mode"].set(arguments["mode"])

        if ("url" in arguments):
            self.arguments["urls"][self.arguments["mode"].get()].set(arguments["url"])
            
        if ("files" in arguments):
            for file in arguments["files"]:
                name = file["name"]
                value = file["value"]
                obj = {"name": sv(), "value": sv()}
                obj["name"].set(name)
                obj["value"].set(value)
                self.arguments["files"][name] = obj
        
        for param in arguments["param"]:
            name = param["name"]
            value = param["value"]
            obj = {"name": sv(), "value": sv()}
            obj["name"].set(name)
            obj["value"].set(value)
            self.arguments["param"].append(obj)
            
        for param in arguments["calibration_parameters"]:
            name = param["name"]
            value = param["value"]
            obj = {"name": sv(), "value": sv()}
            obj["name"].set(name)
            obj["value"].set(value)
            self.arguments["calibration_parameters"].append(obj)

        for param in arguments["service_parameters"]:
            name = param["name"]
            value = param["value"]
            obj = {"name": sv(), "value": sv()}
            obj["name"].set(name)
            obj["value"].set(value)
            self.arguments["service_parameters"].append(obj)
            
    def add_steps(self, steps):
        for step in steps:
            obj = {"param": [], 
                    "overrideparam": [],
                    "objfunc": [], 
                    "name": sv(), 
                    "open": False}
            obj["name"].set("Group " + str(len(self.steps) + 1))
            
            if "param" in step:
                for param in step["param"]:
                    param_obj = {
                        "name": sv(), 
                        "bounds": (sv(), sv()), 
                        "default_value": sv(), 
                        "optimal_value": sv(), 
                        "type": sv(),
                        "calibration_strategy": sv()
                    }
                    param_obj["name"].set(param["name"])
                    if "bounds" in param:
                        param_obj["bounds"][0].set(param["bounds"][0])
                        param_obj["bounds"][1].set(param["bounds"][1]) 
                    else: 
                        param_obj["bounds"][0].set(0)
                        param_obj["bounds"][1].set(1)
                        
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
                        
                    obj["param"].append(param_obj)
            
            if "overrideparam" in step:
                for override in step["overrideparam"]:
                    override_obj = {"name": sv(), "value": sv()}
                    override_obj['name'].set(override['name'])
                    override_obj['value'].set(override['value'])
                    obj['overrideparam'].append(override_obj)

            if "objfunc" in step:
                for objfunc in step["objfunc"]:
                    objfunc_obj = {"name": sv(), 
                                    "of": sv(), 
                                    "weight": sv(), 
                                    "custom_function": sv(),
                                    "custom_function_goal": sv(),
                                    "custom_function_value": sv(),
                                    "data": (sv(), sv())}
                    objfunc_obj["name"].set(objfunc["name"])
                    objfunc_obj["of"].set(objfunc["of"])
                    objfunc_obj["custom_function_goal"].set("Positive Best")
                    
                    if ("weight" in objfunc): 
                        objfunc_obj["weight"].set(objfunc["weight"])
                    else:
                        objfunc_obj["weight"].set(1)
                        
                    if ("custom_function" in objfunc):
                        objfunc_obj["custom_function"].set(objfunc["custom_function"])
                    if ("custom_function_goal" in objfunc):
                        objfunc_obj["custom_function_goal"].set(objfunc["custom_function_goal"])
                    if ("custom_function_value" in objfunc):
                        objfunc_obj["custom_function_value"].set(objfunc["custom_function_value"])

                    objfunc_obj["data"][0].set(objfunc["data"][0])
                    objfunc_obj["data"][1].set(objfunc["data"][1]) 
                    obj["objfunc"].append(objfunc_obj)
            
            self.steps.append(obj)
    
    def add_function(self, step_index):
        obj = {"name": sv(), 
                "of": sv(), 
                "weight": sv(), 
                "custom_function": sv(),
                "custom_function_goal": sv(),
                "custom_function_value": sv(),
                "data": (sv(), sv())}
        obj["name"].set("ns")
        obj["of"].set("ns")
        obj["weight"].set(1)
        obj["data"][0].set("")
        obj["data"][1].set("")
        obj["custom_function"].set("") 
        obj["custom_function_goal"].set("")
        obj["custom_function_value"].set("") 
        
        self.steps[step_index]["objfunc"].append(obj)
        
    def remove_function(self, step_index, index):
        self.steps[step_index]["objfunc"].pop(index)
        
    def dupe_function(self, step_index, index):
        my_func = self.steps[step_index]["objfunc"][index]
        
        new_object = {"name": sv(), 
                        "of": sv(), 
                        "weight": sv(), 
                        "custom_function": sv(),
                        "custom_function_goal": sv(),
                        "custom_function_value": sv(),
                        "data": (sv(), sv())}
        new_object["name"].set(my_func["name"].get())
        new_object["of"].set(my_func["of"].get())
        new_object["weight"].set(my_func["weight"].get())
        new_object["data"][0].set(my_func["data"][0].get())
        new_object["data"][1].set(my_func["data"][1].get())
        new_object["custom_function"].set(my_func["custom_function"].get())
        new_object["custom_function_goal"].set(my_func["custom_function_goal"].get())
        new_object["custom_function_value"].set(my_func["custom_function_value"].get())
        
        self.steps[step_index]["objfunc"].append(new_object)
    
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
            "bounds": (sv(), sv()), 
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
        obj["bounds"][0].set(min)
        obj["bounds"][1].set(max)
        self.steps[step_index]["param"].append(obj)
        
    def remove_bound(self, step_index, index):
        self.steps[step_index]["param"].pop(index)
        
    def add_override(self, step_index, name, value):
        obj = {"name": sv(), "value": sv()}
        obj["name"].set(name)
        obj["value"].set(value)
        self.steps[step_index]["overrideparam"].append(obj)

    def remove_override(self, step_index, index):
        self.steps[step_index]["overrideparam"].pop(index)

    def get_override(self, step_index):
        return self.steps[step_index]["overrideparam"]

    def add_argument(self, key, value):
        obj = {"name": sv(), "value": sv()}
        obj["name"].set(key)
        obj["value"].set(value)
        self.arguments["param"].append(obj)
        
    def add_calibration_param(self, key, value):
        obj = {"name": sv(), "value": sv()}
        obj["name"].set(key)
        obj["value"].set(value)
        self.arguments["calibration_parameters"].append(obj)

    def add_service_param(self, key, value):
        obj = {"name": sv(), "value": sv()}
        obj["name"].set(key)
        obj["value"].set(value)
        self.arguments["service_parameters"].append(obj)

    def add_figure_param(self, key, value):
        obj = {"name": sv(), "value": sv()}
        obj["name"].set(key)
        obj["value"].set(value)
        self.arguments["figure_parameters"].append(obj)

    def add_sensitivity_param(self, key, value):
        obj = {"name": sv(), "value": sv()}
        obj["name"].set(key)
        obj["value"].set(value)
        self.arguments["sensitivity_parameters"].append(obj)

    def add_sensitivity_positiveBestMetrics(self, key, value):
        obj = {"name": sv(), "value": sv()}
        obj["name"].set(key)
        obj["value"].set(value)
        self.arguments["sensitivity_positiveBestMetrics"].append(obj)

    def add_sensitivity_negativeBestMetrics(self, key, value):
        obj = {"name": sv(), "value": sv()}
        obj["name"].set(key)
        obj["value"].set(value)
        self.arguments["sensitivity_negativeBestMetrics"].append(obj)
    
    def move_argument_up(self, index):
        if index > 0:
            self.arguments["param"][index], self.arguments["param"][index - 1] = self.arguments["param"][index - 1], self.arguments["param"][index]
            
    def move_argument_down(self, index):
        if index < len(self.arguments["param"]) - 1:
            self.arguments["param"][index], self.arguments["param"][index + 1] = self.arguments["param"][index + 1], self.arguments["param"][index]
            
    def move_step_up(self, index):
        if index > 0:
            self.steps[index], self.steps[index - 1] = self.steps[index - 1], self.steps[index]
            
    def move_step_down(self, index):
        if index < len(self.steps) - 1:
            self.steps[index], self.steps[index + 1] = self.steps[index + 1], self.steps[index]
            
    def toggle_step_open(self, index):
        self.steps[index]["open"] = not self.steps[index]["open"]
            
    def remove_argument(self, index):
        self.arguments["param"].pop(index)
        
    def remove_calibration_parameter(self, index):
        self.arguments["calibration_parameters"].pop(index)

    def remove_service_parameter(self, index):
        self.arguments["service_parameters"].pop(index)

    def remove_figure_parameter(self, index):
        self.arguments["figure_parameters"].pop(index)

    def remove_sensitivity_parameter(self, index):
        self.arguments["sensitivity_parameters"].pop(index)

    def remove_sensitivity_positiveBestMetrics(self, index):
        self.arguments["sensitivity_positiveBestMetrics"].pop(index)

    def remove_sensitivity_negativeBestMetrics(self, index):
        self.arguments["sensitivity_negativeBestMetrics"].pop(index)
        
    def remove_step(self, index):
        self.steps.pop(index)
            
    def get_project_data(self):
        return self.project_data
            
    def set_path(self, filename):
        file_name = filename.split("/")[-1].replace(".json", "")
        path = filename.replace(file_name + ".json", "")
        self.project_data["path"] = path
        self.project_data["name"] = file_name
            
    def get_arguments(self):
        return self.arguments
    
    def get_steps(self):
        return self.steps
        
    def get_all_as_json(self):
        obj = {"arguments": self.arguments, "steps": self.steps}
        return obj
    
    def set_service_parameters(self, service_parameters):
        self.service_parameters = service_parameters
    
    def get_service_parameters(self):
        return self.service_parameters

    def get_metrics(self):

        self.arguments["url"].set(self.arguments["urls"][self.arguments["mode"].get()].get())

        result = {}
        result['arguments'] = {}
        result['calibration_parameters'] = []
        result['service_parameters'] = []
        result['service_parameters'] = {}
        result['project_data'] = self.project_data
        for key, value in self.arguments.items():
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
            elif key == "calibration_parameters":
                #result['calibration_parameters'][key] = []
                for obj in value:
                    result['calibration_parameters'].append({'name': obj['name'].get(), 'value': obj['value'].get()})
            elif key == "service_parameters":
                #result['service_parameters'][key] = []
                for obj in value:
                    result['service_parameters'].append({'name': obj['name'].get(), 'value': obj['value'].get()})
        result['steps'] = []
        for step in self.steps:
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
                #except ValueError:
                #    step_result['param'].append(
                #        {
                #            'name': param['name'].get(), 
                #            'bounds': (param['bounds'][0].get(), 
                #                       param['bounds'][1].get())
                #        }
                #    )
            step_result['objfunc'] = []
            for objfunc in step['objfunc']:
                step_result['objfunc'].append({'name': objfunc['name'].get(), 'of': objfunc['of'].get(), 'weight': float(objfunc['weight'].get()), 'data': (objfunc['data'][0].get(), objfunc['data'][1].get())})
            result['steps'].append(step_result)
        return result
