# -- Imports --------------------------------------------------------------------------

from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, text, json as original_json
from orjson import dumps as orjson_dumps
from functools import partial
json = partial(original_json, dumps=orjson_dumps)
from sanic.exceptions import NotFound, Forbidden, ServerError, SanicException
from importlib import reload, import_module
from time import time
from js2py import eval_js
from js2py.internals.simplex import JsException
from sys import path
from ... import moca_modules as mzk
from ... import core

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

path.append(str(core.SCRIPTS_DIR.joinpath('python')))

# -------------------------------------------------------------------------- Init --

# -- Blueprints --------------------------------------------------------------------------


dynamic: Blueprint = Blueprint('dynamic', '/dynamic')

# name: (module, update_time, checked_time)
modules = {}

# name: (script, update_time, checked_time)
js_scripts = {}


@dynamic.route('/py/<name>')
async def dynamic_python_route(request: Request, name: str) -> HTTPResponse:
    if isinstance(name, str) and len(name) <= 1024 and '..' not in name and '\\' not in name:
        if name.endswith('.py'):
            module_name = name[:-3].replace('/', '.')
        else:
            module_name = name.replace('/', '.')
        filename = core.SCRIPTS_DIR.joinpath('python').joinpath(mzk.add_dot_py(name))
        if not filename.is_file():
            raise NotFound('Unknown script.')
        if modules.get(module_name) is None:
            module = import_module(module_name)
            modules[module_name] = [module, mzk.get_timestamp(filename), time()]
        elif (time() - modules[module_name][2]) <= 5:
            module = modules[module_name][0]
        else:
            timestamp = mzk.get_timestamp(filename)
            if timestamp == modules[module_name][1]:
                module = modules[module_name][0]
                modules[module_name][2] = time()
            else:
                try:
                    module = reload(modules[module_name][0])
                    modules[module_name] = [module, timestamp, time()]
                except SanicException:
                    raise
                except Exception:
                    module = modules[module_name][0]
        try:
            return module.moca(request)
        except AttributeError:
            raise ServerError("Can't found moca function.")
    else:
        raise Forbidden('Invalid filename.')


@dynamic.route('/js/<name>')
async def dynamic_javascript_route(request: Request, name: str) -> HTTPResponse:
    if isinstance(name, str) and len(name) <= 1024 and '..' not in name and '\\' not in name and name.count('.') <= 1:
        filename = core.SCRIPTS_DIR.joinpath('javascript').joinpath(mzk.add_dot_js(name))
        if not filename.is_file():
            raise NotFound('Unknown script.')
        if js_scripts.get(filename.name) is None:
            js_scripts[filename.name] = [mzk.get_str_from_file(filename), mzk.get_timestamp(filename), time()]
        elif (time() - js_scripts[filename.name][2]) <= 5:
            pass
        else:
            timestamp = mzk.get_timestamp(filename)
            if timestamp == js_scripts[filename.name][1]:
                js_scripts[filename.name][2] = time()
            else:
                new = mzk.get_str_from_file(filename)
                try:
                    _ = eval_js(new)
                    js_scripts[filename.name] = [new, mzk.get_timestamp(filename), time()]
                except JsException:
                    pass
        try:
            result = eval_js(js_scripts[filename.name][0]).to_dict()
            if result['type'] == 'number':
                return text(str(result['data']))
            elif result['type'] == 'string':
                return text(result['data'])
            elif result['type'] == 'array' or result['type'] == 'dictionary':
                return json(result['data'])
            elif result['type'] == 'boolean':
                return text(str(result['data']))
            else:
                raise ServerError('Unknown result type.')
        except JsException as e:
            raise ServerError(str(e))
    else:
        raise Forbidden('Invalid filename.')

# -------------------------------------------------------------------------- Blueprints --
