# -- Imports --------------------------------------------------------------------------

from typing import (
    List
)
from sanic import Blueprint
from .commands import commands
from .dynamic import dynamic

# -------------------------------------------------------------------------- Imports --

# -- Blueprints --------------------------------------------------------------------------

blueprints: List[Blueprint] = [commands, dynamic]

# -------------------------------------------------------------------------- Blueprints --
