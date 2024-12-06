import json
import logging
import os
from random import randint

logger = logging.getLogger("processcube.configuration")

NO_DEFAULT = randint(0, 10)

from ..helpers import str2bool

class Config:

    def __init__(self, config: dict):
        self._config = config

    def get(self, *parts: str, default=NO_DEFAULT):
        config_value = default

        current_config = self._config

        assert current_config is not None, f"current_config is empty '{current_config}'"

        for part in parts:
            if not type(current_config) == dict:
                assert default is not NO_DEFAULT, f"{'->'.join(parts)} not in {self._config}."

                config_value = default
                break

            # default kann nicht None sein und has_key existiert nicht !!!
            if (current_config is not None and part in current_config.keys()) or default is not NO_DEFAULT:
                pass
            else:
                env_value = Config.get_from_env(*parts)

                if env_value is not None:
                    config_value = env_value
                    break
                assert False, f"{part} missing is not given in {current_config}; {'->'.join(parts)} not in {self._config}; and not given as environment variable {':'.join(parts).upper()}"

            if default is not NO_DEFAULT:
                current_config = current_config.get(part, default)
            else:
                current_config = current_config.get(part, config_value)

            config_value = current_config

        return config_value

    @staticmethod
    def get_from_env(*parts: str):
        sep = os.environ.get('CONFIG_ENV_SEP', ':')

        env_value = os.environ.get(f"{sep.join(parts).upper()}")

        return env_value

    @staticmethod
    def override_from_env() -> bool:
        return str2bool(os.environ.get('CONFIG_OVERRIDE_FROM_ENV', 'True'))

    @staticmethod
    def from_env(env_name='CONFIG_FILE'):
        filename = os.environ.get(env_name)

        assert filename is not None, f"{env_name} is not given."

        return Config.from_file(filename)

    @staticmethod
    def from_file(filename: str):
        assert os.path.isfile(filename), f"{filename} did'nt exist or is not a file"

        with open(filename) as f:
            data = json.load(f)

        config = Config(data)

        return config

    @staticmethod
    def from_json_str(json_string: str):

        data = json.loads(json_string)

        config = Config(data)

        return config

if __name__ == '__main__':
    d = {
        'hello': 'world',
        'sample_service': {
                'config_key': 'config_value'
            }
        }
    
    start_debugging()
    start_debugging()

    c = Config(d)

    print(c.get('hello'))
    print(c.get('hello__'))
    print(c.get('foo', 'bar'))
    print(c.get('helo', default='default'))
    print(c.get('no_give', 'config_key', default=None))
    print(c.get('sample_service', 'config_key', default='default_value'))
    print(c.get('sample_service', 'not_defined_config_key', default='default_value'))

    try:
        print(c.get('sample_service', 'not_defined_config_key'))
    except Exception as e:
        print("Exception raised")
        print(f"\t{e}")
