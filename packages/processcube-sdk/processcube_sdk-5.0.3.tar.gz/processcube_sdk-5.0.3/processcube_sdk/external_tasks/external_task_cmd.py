
import logging
from typing import List

from processcube_sdk.configuration import ConfigAccessor
from processcube_client.external_task import ExternalTaskClient

logger = logging.getLogger("processcube.external_tasks")

def start_external_task(handler_factories: List, loop=None):
    ConfigAccessor.ensure_from_env()
    config = ConfigAccessor.current()

    engine_url = config.get('engine', 'url')

    client = ExternalTaskClient(engine_url, loop=loop)

    for factory in handler_factories:
        handler = factory.create_external_task(config)
        
        logger.info(f"Starting external task worker for topic '{handler.get_topic()}'")

        if loop is None:
            client.subscribe_to_external_task_for_topic(handler.get_topic(), handler)
        else:
            client.subscribe_to_external_task_for_topic(handler.get_topic(), handler, loop=loop)

    if loop is None:
        client.start()
    else:
        client.start(run_forever=False)
