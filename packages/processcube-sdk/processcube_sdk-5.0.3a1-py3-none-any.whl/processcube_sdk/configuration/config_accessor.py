from .config import Config

class ConfigAccessor:

    _current_config = None

    @classmethod
    def current(clazz):
        return clazz._current_config

    @classmethod
    def ensure_from_env(clazz, env_name='CONFIG_FILE'):
        if clazz._current_config is None:
            clazz.init_from_env(env_name)

    @classmethod
    def init_from_env(clazz, env_name='CONFIG_FILE'):
        clazz._current_config = Config.from_env(env_name)

    @classmethod
    def init_from_file(clazz, filename: str):
        clazz._current_config = Config.from_file(filename)

    @classmethod
    def init_from_json_str(clazz, json_string: str):
        clazz._current_config = Config.from_json_str(json_string)


