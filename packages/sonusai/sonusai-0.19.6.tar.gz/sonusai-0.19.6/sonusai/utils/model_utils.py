from typing import Any


def import_module(name: str) -> Any:
    """Import a Python module adding the module file's directory to the Python system path so that relative package
    imports are found correctly.
    """
    import os
    import sys
    from importlib import import_module

    try:
        path = os.path.dirname(name)
        if len(path) < 1:
            path = "./"

        # Add model file location to system path
        sys.path.append(os.path.abspath(path))

        try:
            root = os.path.splitext(os.path.basename(name))[0]
            model = import_module(root)
        except Exception as e:
            raise OSError(f"Error: could not import model from {name}: {e}.") from e
    except Exception as e:
        raise OSError(f"Error: could not find {name}: {e}.") from e

    return model
