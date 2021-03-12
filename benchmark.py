import cProfile
from pstats import Stats

from curlylint.tests.utils import BlackRunner

from curlylint.cli import main

from memory_profiler import profile

runner = BlackRunner()

pr = cProfile.Profile()
pr.enable()

result = runner.invoke(main, ["--verbose", "tests/django/wagtailadmin/"])

pr.disable()
p = Stats(pr)

p.strip_dirs().sort_stats("cumulative").print_stats(10)

print(result.exit_code)
print(runner.stdout_bytes.decode())
print(runner.stderr_bytes.decode())

print("Measuring memory consumption")


@profile(precision=6)
def memory_consumption_run():
    runner.invoke(
        main,
        [
            "--verbose",
            "tests/django/wagtailadmin/pages/listing/_page_title_choose.html",
        ],
    )


memory_consumption_run()
