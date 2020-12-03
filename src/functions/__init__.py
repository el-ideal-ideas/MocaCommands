# -- Imports --------------------------------------------------------------------------

from typing import (
    Dict, Callable
)
from .show_my_request import show_my_request

# -------------------------------------------------------------------------- Imports --

# -- Functions --------------------------------------------------------------------------

functions: Dict[str, Callable] = {
    'show_my_request': show_my_request,
}

# -------------------------------------------------------------------------- Functions --
