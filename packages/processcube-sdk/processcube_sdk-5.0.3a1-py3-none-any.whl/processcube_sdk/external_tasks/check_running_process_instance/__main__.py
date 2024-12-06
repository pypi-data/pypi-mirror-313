import logging

from processcube_client.external_task import ExternalTaskClient
import typer

from ...configuration import Config
from . import create_external_task, DEFAULT_ENGINE_URL

app = typer.Typer()

@app.command()
def main(engine_url: str = DEFAULT_ENGINE_URL):
    config_data = {
        "engine": {
            "url": engine_url
        }
    }

    config = Config(config_data)
    handler = create_external_task(config)

    client = ExternalTaskClient(engine_url)
    client.subscribe_to_external_task_for_topic(handler.get_topic(), handler, max_tasks=5)
    client.start()

if __name__ == '__main__':

    format_template = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    level = logging.INFO
    logging.basicConfig(level=level, format=format_template)

    app()