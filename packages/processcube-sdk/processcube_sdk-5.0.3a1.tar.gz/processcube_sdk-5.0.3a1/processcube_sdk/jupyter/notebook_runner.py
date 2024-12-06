from pathlib import Path
from typing import Any

import pandas
import papermill as pm
import scrapbook as sb

class NotebookRunner:

    def __init__(self, temp_path: str):
        self._temp_path = temp_path
        self._notebook = None

    def get(self, key) -> Any:
        if self._notebook is None:
            return None

        result = self._notebook.scraps[key].data

        return result

    def keys(self) -> list:
        if self._notebook is None:
            return []

        return self._notebook.scraps.keys()

    def result_to_dict(self) -> dict:
        result = {}

        for key in self.keys():
            value = self.get(key)
            
            if type(value) == pandas.DataFrame:
                value = value.to_dict('list')
            
            result[key] = value

        return result


    def execute(self, input_path: str, parameters: dict ={}) -> 'NotebookRunner':
        input_filename = Path(input_path)

        if ":/" in self._temp_path:
            output_filename = f"{self._temp_path}/{input_filename.name}"
        else:
            output_temp_dir = Path(self._temp_path)
            if not output_temp_dir.exists():
                output_temp_dir.mkdir(parents=True)
                
            output_filename = str(output_temp_dir.joinpath(input_filename.name))

        pm.execute_notebook(
            input_filename,
            output_filename,
            parameters=parameters,
            request_save_on_cell_execute=False,
            progress_bar=False,
            report_mode=True
        )

        self._notebook = sb.read_notebook(str(output_filename))

        return self
