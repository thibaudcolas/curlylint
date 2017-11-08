from pathlib import Path


def parse_config(path):
    path = Path(path)
    with path.open('r') as f:
        source = f.read()
    config = {}
    exec(source, config)
    config = dict(config)
    del config['__builtins__']
    return config
