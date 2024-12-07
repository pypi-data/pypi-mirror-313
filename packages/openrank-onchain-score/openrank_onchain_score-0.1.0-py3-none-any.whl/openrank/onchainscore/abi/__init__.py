"""On-chain score contract ABI."""

import importlib.resources
import json
from typing import Any

DEFAULT_ABI = 'v1'


def load_bundled(name: str = DEFAULT_ABI) -> dict[str, Any]:
    """
    Load an ABI object bundled with this package.

    :param name: The name of the ABI to load.
    :return: the ABI object.
    """
    assert name.isalnum()  # fend off "../../" attacks
    pkg = importlib.import_module('.', package=__package__)

    files = importlib.resources.files(pkg)
    with files.joinpath(f'{name}.json').open('r') as f:
        return json.load(f)
