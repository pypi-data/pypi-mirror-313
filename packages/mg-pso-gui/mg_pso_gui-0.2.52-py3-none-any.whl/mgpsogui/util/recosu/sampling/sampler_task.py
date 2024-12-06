import os
from csip import Client


class SamplerTask:
    task_id: int
    parameters: dict[str, any]
    objectives: list[dict[str, any]]
    static_parameters: dict[str, any]
    url: str
    files: list[str]
    metainfo: dict[str, any]
    conf: dict[str, any]
    result: dict[str, any]

    def __init__(self, task_id: int, parameters: dict[str, any], objectives: list[dict[str, any]],
                 static_parameters: dict[str, any], url: str, files: list[str] = None, metainfo: dict[str, any] = None,
                 conf: dict[str, any] = None):
        self.task_id = task_id
        assert (parameters is not None and len(parameters) > 0)
        self.parameters = parameters
        assert (objectives is not None and len(objectives) > 0)
        self.objectives = objectives
        self.static_parameters = static_parameters if static_parameters is not None else []
        assert (url is not None and len(url) > 0)
        self.url = url
        self.files = files if files is not None else []
        self.metainfo = metainfo
        self.conf = conf

    def create_request(self) -> Client:
        request: Client = Client(metainfo=self.metainfo)

        for key, value in self.static_parameters.items():
            request.add_data(key, value)

        for key, value in self.parameters.items():
            request.add_data(key, value)

        for of in self.objectives:
            request.add_cosu(of['name'], of['of'], of['data'])

        return request

    def run_task(self) -> bool:
        self.result = {}
        request: Client = self.create_request()
        async_call: bool = self.conf.get('async_call', True) if self.conf is not None else True
        # save response, set it to a folder if responses should be saved.
        save_resp = self.conf.get('save_response_to', None) if self.conf is not None else None
        successful: bool = False

        response: Client = None
        try:
            if async_call:
                response = request.execute_async(self.url, files=self.files, conf=self.conf)
            else:
                response = request.execute(self.url, files=self.files, conf=self.conf)

            successful = response.is_finished()
            if not successful:
                print(response)

            if save_resp:
                response.save_to(os.path.join(save_resp, 'task_{}.json'.format(self.task_id)))

            objectives: list[dict[str, str]] = response.get_metainfo("cosu")
            for of in objectives:
                self.result[of["name"]] = of["value"]
        except Exception as ex:
            print(ex)
            print(response)
            successful = False

        return successful
