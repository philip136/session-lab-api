from importlib import import_module
from pkgutil import walk_packages

import backend.infra.database.entities as entities_package


def load_entities():
    prefix = f"{entities_package.__name__}."

    for module in walk_packages(
        entities_package.__path__,
        prefix
    ):
        import_module(module.name)