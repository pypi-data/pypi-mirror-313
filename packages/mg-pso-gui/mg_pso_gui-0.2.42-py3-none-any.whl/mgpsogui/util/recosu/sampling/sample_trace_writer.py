import threading


class SampleTraceWriter:
    trace_file: str
    parameter_indices: dict[int, str]
    objective_indices: dict[int, str]
    write_lock: threading.Lock

    def __init__(self, trace_file: str):
        assert(trace_file is not None and len(trace_file) > 0)
        self.trace_file = trace_file
        self.parameter_indices = {}
        self.objective_indices = {}
        self.write_lock = threading.Lock()

    def write_header(self, parameter_names: list[str], objective_names: list[str]) -> None:
        with self.write_lock:
            with open(self.trace_file, 'w') as writer:
                writer.write("id")
                self.parameter_indices = {}
                index: int = 0
                for name in parameter_names:
                    writer.write(",{}".format(name))
                    self.parameter_indices[index] = name
                    index = index + 1
                self.objective_indices = {}
                index = 0
                for name in objective_names:
                    writer.write(",{}".format(name))
                    self.objective_indices[index] = name
                    index = index + 1
                writer.write("\n")

    def append_sample(self, sample_id: int, parameters: dict[str, any], objectives: dict[str, any]) -> None:
        with self.write_lock:
            with open(self.trace_file, 'a') as writer:
                writer.write("{}".format(sample_id))
                index: int = 0
                while index < len(self.parameter_indices):
                    writer.write(",{}".format(parameters[self.parameter_indices[index]]))
                    index = index + 1
                index = 0
                while index < len(self.objective_indices):
                    writer.write(",{}".format(objectives[self.objective_indices[index]]))
                    index = index + 1
                writer.write("\n")