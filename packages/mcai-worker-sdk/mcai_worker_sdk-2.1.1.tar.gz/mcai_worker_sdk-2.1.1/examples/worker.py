import logging
import time

import mcai_worker_sdk as mcai


class McaiWorkerParameters(mcai.WorkerParameters):
    action: str
    number: int
    array_of_strings: list[str]
    array_of_integers: list[int]
    source_path: str
    destination_path: str


class McaiWorkerTest(mcai.Worker):
    model: str

    def __init__(self, params, desc):
        super().__init__(params, desc)
        # You should avoid doing stuff here as error handling won't be done properly...

    def setup(self) -> None:
        """
        Optional worker setup function. May be used to load models, do some checks...
        """
        self.model = "Loading the statistic model to use it during process"

    def process(
        self, handle_callback, parameters: McaiWorkerParameters, job_id: int
    ) -> dict:
        """
        Standard worker process function.
        """
        logging.info(f"This is the model loaded during setup: {self.model}")

        i = 0
        while i < 5:
            time.sleep(1)
            handle_callback.publish_job_progression(25 * i)
            i += 1

        # By default, the job status is set to "completed" if the process returns properly. If an error is raised,
        # the job status is set to "error" and the error message is returned as a response.
        # However, the job status can be overwritten by calling:
        #
        #   handle_callback.set_job_status("stopped")
        #
        # This function return whether the status has been correctly set.
        # Possible job status values are: "completed", "stopped" and "error".
        return {"destination_paths": ["/path/to/generated/file.ext"],
                "parameters": [{"id": "my_parameter", "kind": "string", "value": "hello"}]}


if __name__ == "__main__":
    desc = mcai.WorkerDescription(__package__) # This allows retrieving information from the worker, such as name, version, license...
    worker = McaiWorkerTest(McaiWorkerParameters, desc)
    worker.start()
