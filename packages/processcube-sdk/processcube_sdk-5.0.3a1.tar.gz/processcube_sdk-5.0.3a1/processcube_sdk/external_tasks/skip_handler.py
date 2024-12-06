from .base_handler import BaseHandler


class SkipHandler(BaseHandler):

    def __init__(self, topic=None, temp_folder=None):
        super(SkipHandler, self).__init__(topic, temp_folder)

    def handle_task(self, payload, task=None):
        return {'skipped': True}
