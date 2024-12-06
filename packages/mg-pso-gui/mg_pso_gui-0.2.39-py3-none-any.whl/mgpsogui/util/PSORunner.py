
import sys
from multiprocessing import Process, Queue
from queue import Empty
import threading
import time
import os
from .recosu.sampling.sampling import run_sampler
from .recosu.pso import global_best
from csip import Client
import traceback
import urllib
import shutil
import json
import numpy as np

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def run_process(stdout_queue, stderr_queue, results_queue, data, folder, mode):
    """_summary_

    Args:
        stdout_queue (_type_): _description_
        stderr_queue (_type_): _description_
        results_queue (_type_): _description_
        data (_type_): _description_
        folder (_type_): _description_
        mode (_type_): _description_
    """
    try:
        # Setup folders
        if not os.path.exists(folder):
            os.makedirs(folder)

        if not os.path.exists(os.path.join(folder, "results")):
            os.makedirs(os.path.join(folder, "results"))

        if (os.path.exists(os.path.join(folder, 'output.txt'))):
            os.remove(os.path.join(folder, 'output.txt'))
            
        if (os.path.exists(os.path.join(folder, 'error.txt'))):
            os.remove(os.path.join(folder, 'error.txt'))

        # Redirect stdout and stderr to files
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        read_stdout, write_stdout = os.pipe()
        read_stderr, write_stderr = os.pipe()
        
        sys.stdout = os.fdopen(write_stdout, 'w')
        sys.stderr = os.fdopen(write_stderr, 'w')
        
        stdout_thread = threading.Thread(target=enqueue_output, args=(os.fdopen(read_stdout, 'r'), stdout_queue))
        stderr_thread = threading.Thread(target=enqueue_output, args=(os.fdopen(read_stderr, 'r'), stderr_queue))
        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()

        if mode == "Sampling: Halton":
            run_sampling(data, "halton", folder, results_queue)
        elif mode == "Sampling: Random":
            run_sampling(data, "random", folder, results_queue)
        elif mode == "Sensitivity Analysis":
            run_sensitivity_analysis(data, folder, results_queue)
        elif mode == "Optimization":
            run_optimization(data, folder, results_queue)
        else:
            print("Invalid mode")

        stdout_thread.join()
        stderr_thread.join()
        
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    except Exception as e:
        print("An exception occurred: ", flush=True)
        print(str(e))
        # Print stack trace
        import traceback
        traceback.print_exc()

        # Write all of this information to a crash file
        with open(os.path.join(folder, 'crash.txt'), 'w') as f:
            f.write(str(e))
            f.write("\n")
            traceback.print_exc(file=f)
    finally:
        stdout_thread.join()
        stderr_thread.join()
        
        sys.stdout = old_stdout
        sys.stderr = old_stderr

def process_list(data, parameter_map, args, options, oh_strategy, config, metainfo, list_name):
    """_summary_

    Args:
        data (_type_): _description_
        parameter_map (_type_): _description_
        args (_type_): _description_
        options (_type_): _description_
        oh_strategy (_type_): _description_
        config (_type_): _description_
        metainfo (_type_): _description_
        list_name (_type_): _description_
    """
    for obj in data[list_name]:
        name = obj['name']
        type = obj['type']
        destination = obj['destination']
        original_value = obj['value']
        converted_value = original_value
        if type == "integer":
            converted_value = int(converted_value)
        elif type == "float":
            converted_value = float(converted_value)
        elif type == "boolean":
            converted_value = True if converted_value == "True" else False

        if destination == "args":
            args['param'].append((name, obj['value']))
        elif destination == "kwargs":
            parameter_map[name] = original_value
        elif destination == "conf":    
            config[name] = converted_value
        elif destination == "metainfo":
            metainfo[name] = converted_value
        elif destination == "options":
            option_name = name.replace("options_", "")
            options[option_name] = converted_value
        elif destination == "oh_strategy":
            strategy_name = name.replace("strategy_", "")
            oh_strategy[strategy_name] = converted_value

def process_steps(data):
    """_summary_

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """

    steps = data['steps']
    output_steps = []
    for step in steps:
        output_step = {}
        output_step['param'] = []
        output_step['objfunc'] = []
        for parameter in step['parameter_objects']:
            parameter_object = {}
            type = parameter['type']
            if type != "list":
                parameter_object['name'] = parameter['name']
                parameter_object['bounds'] = (float(parameter['min_bound']), float(parameter['max_bound']))
                output_step['param'].append(parameter_object)
            else:
                parameter_object['name'] = parameter['name']
                parameter_object['bounds'] = (float(parameter['min_bound']), float(parameter['max_bound']))
                parameter_object['type'] = "list"
                parameter_object['calibration_strategy'] = parameter['calibration_strategy']
                parameter_object['default_value'] = [float(x) for x in parameter['default_value'].replace("[", "").replace("]", "").split(",")]
                output_step['param'].append(parameter_object)
            
        for function in step['objective_functions']:
            out_object = {}
            out_object['name'] = function['name']
            out_object['of'] = function['objective_function']
            out_object['weight'] = float(function['weight'])
            out_object['data'] = [
                function["data_observed"],
                function["data_simulated"]
            ]
            output_step['objfunc'].append(out_object)
        output_steps.append(output_step)
    return output_steps

def pp(parameter, parameter_map, default=None):
    """_summary_

    Args:
        parameter (_type_): _description_
        parameter_map (_type_): _description_
        default (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    if parameter in parameter_map.keys():
        if parameter_map[parameter] != ""  \
        and parameter_map[parameter] != "None" \
        and parameter_map[parameter] != "null" \
        and parameter_map[parameter] != "NULL":
            return parameter_map[parameter]
        else:
            return default
    return default

def run_sampling(data, mode, folder, results_queue):
    """_summary_

    Args:
        data (_type_): _description_
        mode (_type_): _description_
        folder (_type_): _description_
        results_queue (_type_): _description_
    """

    parameter_map = {}
    args = {
        "param": [],
        "url": data["url"],
        "files": {}
    }
    options = {}
    oh_strategy = {}
    config = {}
    metainfo = {}

    process_list(data, parameter_map, args, options, oh_strategy, config, metainfo, "model_parameters")
    process_list(data, parameter_map, args, options, oh_strategy, config, metainfo, "hyperparameters")
    process_list(data, parameter_map, args, options, oh_strategy, config, metainfo, "service_parameters")

    output_steps = process_steps(data)

    config['step_trace'] = os.path.join(folder, 'pso_step_trace.json')

    print("Parsing Parameters...\n", flush=True)
    print("steps: ", output_steps, flush=True)
    print("args: ", args, flush=True)
    print("options: ", options, flush=True)
    print("oh_strategy: ", oh_strategy, flush=True)
    print("config: ", config, flush=True)
    print("metainfo: ", metainfo, flush=True)
    print("kwargs: ", parameter_map, flush=True)

    print("Running Sampling..\n", flush=True)
    trace = run_sampler(output_steps, 
                        args, 
                        int(pp('count', parameter_map)), 
                        int(pp('num_threads', parameter_map)), 
                        mode, 
                        conf=config, 
                        metainfo=metainfo if len(metainfo) > 0 else None,
                        trace_file=os.path.join(folder, 'results', mode + '_trace.csv'),
                        offset=pp('offset', parameter_map))
    results_queue.put(trace)
    print(trace, flush=True)
    print("\n", flush=True)

def run_optimization(data, folder, results_queue):
    """_summary_

    Args:
        data (_type_): _description_
        folder (_type_): _description_
        results_queue (_type_): _description_
    """
    parameter_map = {}
    args = {
        "param": [],
        "url": data["url"],
        "files": {}
    }
    options = {}
    oh_strategy = {}
    config = {}
    metainfo = {}

    process_list(data, parameter_map, args, options, oh_strategy, config, metainfo, "model_parameters")
    process_list(data, parameter_map, args, options, oh_strategy, config, metainfo, "hyperparameters")
    process_list(data, parameter_map, args, options, oh_strategy, config, metainfo, "service_parameters")

    output_steps = process_steps(data)

    config['step_trace'] = os.path.join(folder, 'pso_step_trace.json')

    print("Parsing Parameters...\n", flush=True)
    print("steps: ", output_steps, flush=True)
    print("args: ", args, flush=True)
    print("options: ", options, flush=True)
    print("oh_strategy: ", oh_strategy, flush=True)
    print("config: ", config, flush=True)
    print("metainfo: ", metainfo, flush=True)
    print("kwargs: ", parameter_map, flush=True)

    print("Running MG-PSO Optimization...\n", flush=True)
    optimizer, trace = global_best(output_steps,   
            rounds=(int(pp('min_rounds', parameter_map)), int(pp('max_rounds', parameter_map))),              
            args=args,      
            n_particles=int(pp('n_particles', parameter_map, 10)),
            iters=int(pp('iters', parameter_map, 1)),  
            n_threads=int(pp('n_threads', parameter_map, 4)),      
            rtol=float(pp('rtol', parameter_map, 0.001)),      
            ftol=float(pp('ftol', parameter_map, -np.inf)),      
            ftol_iter=int(pp('ftol_iter', parameter_map, 1)),      
            rtol_iter=int(pp('rtol_iter', parameter_map, 1)),      
            options=options,
            oh_strategy=oh_strategy, 
            metainfo=metainfo if len(metainfo) > 0 else None,
            cost_target=float(pp('cost_target', parameter_map, -np.inf)),   
            conf=config
        )
    
    results_queue.put(trace)
    print(trace, flush=True)
    pass



def run_sensitivity_analysis(data, folder, results_queue):
    """_summary_

    Args:
        data (_type_): _description_
        folder (_type_): _description_
        results_queue (_type_): _description_
    """
    print("Running Sensitivity Analysis", flush=True)

    shutil.copyfile(data["sensitivity_analysis_path"], os.path.join(folder, 'results', 'trace.csv'))
    trace_path = os.path.join(folder, 'results', 'trace.csv')

    output_steps = process_steps(data)

    # Get list of parameters from steps
    parameters = []
    for param in output_steps[0]['param']:
        parameters.append(param['name'])

    request_json = {
        "metainfo": {
            "service_url": None,
            "description": "",
            "name": "",
            "mode": "async"
        },
        "parameter": [
            {
            "name": "parameters",
            "value": parameters
            },
            {
            "name": "positiveBestMetrics",
            "value": ["ns","kge","mns","kge09","nslog2"]
            },
            {
            "name": "zeroBestMetrics",
            "value": ["pbias","rmse"]
            }
        ]
    }
    
    with open(os.path.join(folder, 'results', 'request.json'), 'w') as json_file:
        json.dump(request_json, json_file, indent=4)
    
    request_path = os.path.join(folder, 'results', 'request.json')

    output_directory = os.path.join(folder, 'results')

    print("Starting ", data['url'], request_path, trace_path, output_directory, flush=True)

    sensitivity_analysis(data['url'], request_path, trace_path, output_directory)

    print("Finished Sensitivity Analysis", flush=True)








def create_request(request_file: str) -> Client:
    request: Client = Client.from_file(request_file)
    return request

def download_output(response: Client, target_directory) -> None:
    data_names: list[str] = response.get_data_names()
    for name in data_names:
        url = response.get_data_value(name)
        file_path = os.path.join(target_directory, name)
        urllib.request.urlretrieve(url, file_path)

def sensitivity_analysis(url, request_file, trace_file, output_directory):
    request: Client = create_request(request_file)
    files: list[str] = [trace_file] if os.path.isfile(trace_file) else []
    conf = {
        'service_timeout': 60.0,  # (sec)
    }
    result: Client = Client()
    try:
        result = request.execute(url, files=files, sync=True, conf=conf)
    except Exception as ex:
        traceback.print_exc()
        exit(1)

    if result.is_finished():
        download_output(result, output_directory)
















"""
def run_process_old(stdout_queue, stderr_queue, results_queue, data, folder):
    steps = data['steps']
    args = data['arguments']
    calib = data['calibration_parameters']
    
    my_mode = args["mode"]

    # If "mode" in args remove it
    if "mode" in args:
        del args["mode"]
    
    calibration_map = {}
    for param in calib:
        param_name = param['name']
        param_value = param['value']
        calibration_map[param_name] = param_value
        
    if not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(os.path.join(folder, "results")):
        os.makedirs(os.path.join(folder, "results"))

    if (os.path.exists(os.path.join(folder, 'output.txt'))):
        os.remove(os.path.join(folder, 'output.txt'))
        
    if (os.path.exists(os.path.join(folder, 'error.txt'))):
        os.remove(os.path.join(folder, 'error.txt'))
    
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    read_stdout, write_stdout = os.pipe()
    read_stderr, write_stderr = os.pipe()
    
    sys.stdout = os.fdopen(write_stdout, 'w')
    sys.stderr = os.fdopen(write_stderr, 'w')
    
    stdout_thread = threading.Thread(target=enqueue_output, args=(os.fdopen(read_stdout, 'r'), stdout_queue))
    stderr_thread = threading.Thread(target=enqueue_output, args=(os.fdopen(read_stderr, 'r'), stderr_queue))
    stdout_thread.daemon = True
    stderr_thread.daemon = True
    stdout_thread.start()
    stderr_thread.start()
    
    try:
        
        options = {}
        oh_strategy = {}
        
        for key in calibration_map.keys():
            if "options_" in key:
                options[key.replace("options_", "")] = float(calibration_map[key])
            if "strategy_" in key:
                oh_strategy[key.replace("strategy_", "")] = calibration_map[key]

        config = {}

        if my_mode == "Sampling":
            config = {
                'service_timeout': int(calibration_map['service_timeout']),
                'http_retry': int(calibration_map['http_retry']),
                'allow_redirects': True if calibration_map['allow_redirects'] == "True" else False,
                'async_call': True if calibration_map['async_call'] == "True" else False,
                'conn_timeout': int(calibration_map['conn_timeout']),
                'read_timeout': int(calibration_map['read_timeout']),
                'step_trace': os.path.join(folder, 'pso_step_trace.json')
            }
        elif my_mode == "Optimization":
            config = {
                'service_timeout': int(calibration_map['service_timeout']),
                'http_retry': int(calibration_map['http_retry']),
                'http_allow_redirects': True if calibration_map['allow_redirects'] == "True" else False,
                'async_call': True if calibration_map['async_call'] == "True" else False,
                'http_conn_timeout': int(calibration_map['conn_timeout']),
                'http_read_timeout': int(calibration_map['read_timeout']),
                'particles_fail': int(calibration_map['particles_fail']),
                'step_trace': os.path.join(folder, 'pso_step_trace.json')
            }

        print("\n")
        print(steps)
        print("\n")
        print(args)
        print("\n")
        print(calibration_map)
        print("\n")
        print(options)
        print("\n")
        print(oh_strategy)
        print("\n")
        print(config)
        print("\n", flush=True)

        if my_mode == "Sampling: Halton":
            print("Running Halton Sampling..\n", flush=True)
            trace = run_sampler(steps, 
                                args, 
                                int(calibration_map['count']), 
                                int(calibration_map['num_threads']), 
                                "halton", 
                                conf=config, 
                                trace_file=os.path.join(folder, 'results', 'halton_trace.csv'),
                                offset=int(calibration_map['offset']))
            results_queue.put(trace)
            print(trace, flush=True)
            print("\n", flush=True)
            
        elif my_mode == "Sampling: Random":
            print("Running Random Sampling...\n", flush=True)
            trace = run_sampler(steps, 
                    args, 
                    int(calibration_map['count']), 
                    int(calibration_map['num_threads']), 
                    "random", 
                    conf=config, 
                    trace_file=os.path.join(folder, 'results', 'random_trace.csv'))
            results_queue.put(trace)
            print(trace, flush=True)
            print("\n", flush=True)

        elif my_mode == "Sensitivity Analysis":
            
            print("Running Sensitivity Analysis", flush=True)

            shutil.copyfile(data["sensitivity_analysis_path"], os.path.join(folder, 'results', 'trace.csv'))
            trace_path = os.path.join(folder, 'results', 'trace.csv')

            # Get list of parameters from steps
            parameters = []
            for param in steps[0]['param']:
                parameters.append(param['name'])

            request_json = {
                "metainfo": {
                    "service_url": None,
                    "description": "",
                    "name": "",
                    "mode": "async"
                },
                "parameter": [
                    {
                    "name": "parameters",
                    "value": parameters
                    },
                    {
                    "name": "positiveBestMetrics",
                    "value": ["ns","kge","mns","kge09","nslog2"]
                    },
                    {
                    "name": "zeroBestMetrics",
                    "value": ["pbias","rmse"]
                    }
                ]
            }
            
            with open(os.path.join(folder, 'results', 'request.json'), 'w') as json_file:
                json.dump(request_json, json_file, indent=4)
            
            request_path = os.path.join(folder, 'results', 'request.json')

            output_directory = os.path.join(folder, 'results')

            print("Starting ", args['url'], request_path, trace_path, output_directory, flush=True)

            sensitivity_analysis(args['url'], request_path, trace_path, output_directory)

            print("Finished Sensitivity Analysis", flush=True)
        else:
            print("Running MG-PSO Optimization...\n", flush=True)
            optimizer, trace = global_best(steps,   
                    rounds=(int(calibration_map['min_rounds']), int(calibration_map['max_rounds'])),              
                    args=args,      
                    n_particles=int(calibration_map['n_particles']),      
                    iters=int(calibration_map['iters']),  
                    n_threads=int(calibration_map['n_threads']),      
                    options=options,
                    oh_strategy=oh_strategy, 
                    conf=config
                )
            
            results_queue.put(trace)
            print(trace, flush=True)
        
        print("Finishing up...", flush=True)
        time.sleep(5)
    except Exception as e:
        print("An exception occurred: ", flush=True)
        print(str(e))
        # Print stack trace
        import traceback
        traceback.print_exc()

        # Write all of this information to a crash file
        with open(os.path.join(folder, 'crash.txt'), 'w') as f:
            f.write(str(e))
            f.write("\n")
            traceback.print_exc(file=f)
    finally:
        stdout_thread.join()
        stderr_thread.join()
        
        sys.stdout = old_stdout
        sys.stderr = old_stderr
"""