from collections.abc import Iterable
import math
import asyncio
import concurrent
import datetime
from ..utils import utils
from ..sampling.halton.halton import HaltonSampleGenerator
from ..sampling.random.random_sampler import RandomSampleGenerator
from ..sampling.sampler_task import SamplerTask
from ..sampling.sample_trace_writer import SampleTraceWriter


def weighted_value(weight: float, lower: float, upper: float) -> float:
    return lower + weight * (upper - lower)


def get_static_parameters(args: dict[str, any]) -> dict[str, any]:
    static_parameters: dict[str, any] = {}
    for param in args["param"]:
        static_parameters[param["name"]] = param["value"]
    return static_parameters


def get_objective_names(objfunc: dict[str, any]) -> list[str]:
    objective_names: list[str] = []
    for of in objfunc:
        objective_names.append(of["name"])
    return objective_names


def thread_function(task: SamplerTask) -> tuple[bool, SamplerTask]:
    return task.run_task(), task


def create_generator(method: str, count: int, num_parameters: int, **kwargs) -> Iterable[tuple[int, list[float]]]:
    if method == "halton":
        offset: int = 0
        if "offset" in kwargs:
            offset = kwargs["offset"]
        return HaltonSampleGenerator(count, offset, num_parameters)
    elif method == "random":
        return RandomSampleGenerator(count, num_parameters)

    raise Exception("Sampling method is not recognized")


def run_sampler(steps: list[dict[str, any]], args: dict[str, any], count: int, num_threads: int, method: str = "halton",
                metainfo: dict[str, any] = None, conf: dict[str, any] = None, trace_file: str = "trace.csv",
                **kwargs) -> dict[int, tuple[dict[str, any], dict[str, any]]]:
    param_names, bounds, objfunc = utils.get_step_info(steps, 0)
    generator: Iterable[tuple[int, list[float]]] = create_generator(method, count, len(param_names), **kwargs)
    objective_names: list[str] = get_objective_names(objfunc)
    static_parameters: dict[str, any] = get_static_parameters(args)
    url: str = args["url"]
    files: list[str] = args["files"]

    trace: dict[int, tuple[dict[str, float], dict[str, float]]] = {}
    trace_writer: SampleTraceWriter = SampleTraceWriter(trace_file)
    trace_writer.write_header(param_names, objective_names)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for sample_id, sample in generator:
            params: dict[str, float] = {}
            index: int = 0
            while index < len(sample):
                params[param_names[index]] = weighted_value(sample[index], bounds[0][index], bounds[1][index])
                index += 1

            task: SamplerTask = SamplerTask(sample_id, params, objfunc, static_parameters, url, files, metainfo, conf)
            futures.append(executor.submit(thread_function, task))
        # for future in concurrent.futures.as_completed(futures):
        #     pass
        num_finished: int = 0
        percentage: float
        last_percentage: float = 0
        for future in concurrent.futures.as_completed(futures):
            try:
                successful, task = future.result()

                if successful:
                    trace[task.task_id] = (task.parameters, task.result)
                    trace_writer.append_sample(task.task_id, task.parameters, task.result)
                else:
                    print("Failed to successfully execute task: {}", task.task_id, flush=True)
            except asyncio.CancelledError as ce:
                pass
            except asyncio.InvalidStateError as ise:
                pass
            except Exception as ex:
                print(ex, flush=True)

            num_finished = num_finished + 1
            percentage = math.trunc(num_finished / count * 1000) / 10
            if percentage > last_percentage:
                last_percentage = percentage
                print("{}% Done {}".format(percentage, datetime.datetime.now()), flush=True)

    return trace
