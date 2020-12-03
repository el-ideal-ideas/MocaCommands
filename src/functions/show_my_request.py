# -- Imports --------------------------------------------------------------------------

from sanic.request import Request
from sanic.response import HTTPResponse, json as original_json
from orjson import dumps as orjson_dumps
from functools import partial
json = partial(original_json, dumps=orjson_dumps)

# -------------------------------------------------------------------------- Imports --

# -- Function --------------------------------------------------------------------------


def show_my_request(request: Request, *args, **kwargs) -> HTTPResponse:
    data = {
        'ip': request.ip,
        'headers': dict(request.headers),
        'json': request.json,
        'form': request.form,
        'files': request.files,
        'token': request.token,
        'cookies': request.cookies,
        'port': request.port,
        'socket': request.socket,
        'server_name': request.server_name,
        'forwarded': request.forwarded,
        'server_port': request.server_port,
        'remote_addr': request.remote_addr,
        'scheme': request.scheme,
        'host': request.host,
        'content_type': request.content_type,
        'match_info': request.match_info,
        'path': request.path,
        'query_string': request.query_string,
        'url': request.url,
    }
    return json(data)


# -------------------------------------------------------------------------- Function --
