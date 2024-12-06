from .debugging import start_debugging
from .configuration.config import Config


def main():
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

if __name__ == '__main__':
    main()