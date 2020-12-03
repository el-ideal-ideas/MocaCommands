"""
*** This script will be reload automatically. So you can change your response dynamically.***
*** If this file raise a Exception (without SanicException) when reloading, system will use old data.***
The function named `moca` will be called, when received a request.
`moca` function must return a Sanic response.
Request object will be passed to `moca` function.
"""

# -- Imports --------------------------------------------------------------------------

from sanic.request import Request
from sanic.response import HTTPResponse, text
from random import choice

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

data = 'This is a sample data'
end = ['!', '?', '.', '!!', '!?']

# -------------------------------------------------------------------------- Variables --

# -- Moca --------------------------------------------------------------------------


def moca(request: Request) -> HTTPResponse:
    return text(data + choice(end))

# -------------------------------------------------------------------------- Moca --
