import logging

from ..configuration.config_accessor import ConfigAccessor


def setup_logging(default_log_level=logging.INFO):
    ConfigAccessor.ensure_from_env()
    config = ConfigAccessor.current()

    logging_level = config.get('logging', 'level', default="info")

    log_level = getattr(logging, logging_level.upper(), default_log_level)

    format_template = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=log_level, format=format_template)

    return logging.getLogger()
