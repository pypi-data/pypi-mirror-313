from dataclasses import dataclass
import logging
import os

import papermill as pm

from .base_handler import BaseHandler
from processcube_sdk.jupyter import NotebookRunner

logger = logging.getLogger('processcube.external_tasks')

@dataclass
class JupyterConfig:
    notebooks_path: str
    notebook_name: str
    temp_path: str

class JupyterHandler(BaseHandler):

    def __init__(self, topic: str='jupyter_notebook', jupyter_config: JupyterConfig=None):
        super(JupyterHandler, self).__init__(topic)

        self._jupyter_config: JupyterConfig = jupyter_config

    def get_input_filename(self):

        notebook_name = self._jupyter_config.notebook_name
        notebooks_path = self._jupyter_config.notebooks_path

        input_filename = os.path.join(notebooks_path, f"{notebook_name}.ipynb")
        return input_filename


    def prepare_parameters(self, **additional_parameters):
        parameters = {}
        parameters.update(additional_parameters)

        return parameters

    def handle_task(self, payload, task=None):
        input_filename = self.get_input_filename()

        parameters = self.prepare_parameters(**payload)
        parameters['task'] = task
      
        temp_path = self._jupyter_config.temp_path
        runner = NotebookRunner(temp_path)

        _ = runner.execute(input_filename, parameters)

        return runner.result_to_dict()
