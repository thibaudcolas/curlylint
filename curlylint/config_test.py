import tempfile

from .config import parse_config


def test():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b'hello = "worl" + "d"\n')
        f.seek(0)
        config = parse_config(f.name)
        assert config == {'hello': 'world'}
