import logging

from invoke import Collection, Program, Task

from . import __version__, core, shorthands

logging.basicConfig(level=logging.INFO, format="%(message)s")

version = __version__

namespace = Collection()

# Load up some of our functions into the root namespace.
for core_ns in [core, shorthands]:
    tasks = filter(lambda x: isinstance(x, Task), vars(core_ns).values())
    for task in tasks:
        namespace.add_task(task)

program = Program(namespace=namespace, version=version)
