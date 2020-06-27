__name__ = "curlylint"
__version__ = "0.11.0"
__description__ = "{{ 🎀}} Experimental linter for Jinja, Nunjucks, Django templates, Twig, Liquid"
__author__ = "Thibaud Colas"
__author_email__ = "thibaudcolas@gmail.com"
__url__ = "https://github.com/thibaudcolas/curlylint"
__license__ = "MIT"
__copyright__ = "Copyright 2020-present Thibaud Colas"

if __name__ == "__main__":
    from .cli import patched_main

    patched_main()
