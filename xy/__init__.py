from nicepy.importer.importer import future_imports
with future_imports(__name__, __path__):
    from .a import *
    from .b import *