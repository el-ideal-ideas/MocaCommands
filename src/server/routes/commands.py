# -- Imports --------------------------------------------------------------------------

from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, text
from sanic.exceptions import Forbidden, ServerError, abort
from limits import parse_many
from subprocess import CalledProcessError
from ...functions import functions
from ... import moca_modules as mzk
from ... import core
from .utils import check_root_pass

# -------------------------------------------------------------------------- Imports --

# -- Blueprint --------------------------------------------------------------------------

commands: Blueprint = Blueprint('commands', '/commands')


@commands.route('/run', {'GET', 'POST', 'OPTIONS'})
async def run_commands(request: Request) -> HTTPResponse:
    """Run registered commands."""
    cmd_name, password, args = mzk.get_args(
        request,
        ('cmd_name|name', str, None, {'max_length': 64}),
        ('password|pass', str, None, {'max_length': 1024}),
        ('arguments|args', str, '', {'max_length': 8192, 'invalid_str': ["'", "\\", ";"]}),
    )
    ip = mzk.get_remote_address(request)
    if cmd_name is None:
        raise Forbidden('cmd-name parameter is required and must be less than 64 or equal to 64 characters.')
    cmd = request.app.commands.get(cmd_name, None)
    if cmd is None:
        raise Forbidden('Unknown command.')
    elif not cmd.get('status', True):
        raise Forbidden('This command is offline.')
    elif cmd.get('pass', None) != password and request.app.system_config.get_config('root_pass') != password:
        raise Forbidden('Password error.')
    elif cmd.get('ip', None) is not None \
            and cmd['ip'] != '*' \
            and ip not in cmd['ip']:
        raise Forbidden("This command can't use from your ip address.")
    rate_limit = cmd.get('rate', '*')
    if rate_limit != '*':
        for item in parse_many(rate_limit):  # check rate limit.
            if not request.app.rate_limiter.hit(item, cmd_name):
                abort(429, 'Too many requests.')
    rate_per_ip = cmd.get('rate_per_ip', '*')
    if rate_per_ip != '*':
        for item in parse_many(rate_per_ip):  # check rate limit.
            if not request.app.rate_limiter.hit(item, f'{cmd_name}-{ip}'):
                abort(429, 'Too many requests.')
    try:
        if "cmd" in cmd:
            if cmd['cmd'].startswith('[moca]'):
                func = functions.get(cmd['cmd'][6:])
                if func is None:
                    raise ServerError('Unknown function.')
                return func(request, args)
            else:
                res = mzk.check_output(f"{cmd['cmd']} '{args}'", shell=True)
                return text(res.decode())
        elif "cmd_path" in cmd:
            if cmd["cmd_path"].startswith("/"):
                res = mzk.check_output(f"{cmd['cmd_path']} '{args}'", shell=True)
            else:
                res = mzk.check_output(f"{core.COMMANDS_DIR.joinpath(cmd['cmd_path'])} '{args}'", shell=True)
            return text(res.decode())
        else:
            raise ServerError('Command format error.')
    except CalledProcessError:
        raise ServerError("Can't execute this command.")


@commands.route('/run-any', {'GET', 'POST', 'OPTIONS'})
async def run_any_commands(request: Request) -> HTTPResponse:
    """Run any commands"""
    check_root_pass(request)
    cmd, *_ = mzk.get_args(
        request,
        ('command|cmd', str, None, {'max_length': 16384})
    )
    if cmd is None:
        raise Forbidden('command parameter format error')
    try:
        res = mzk.check_output(cmd, shell=True)
        return text(res.decode())
    except CalledProcessError:
        raise ServerError("Can't execute this command.")


@commands.route('/run-any-py', {'GET', 'POST', 'OPTIONS'})
async def run_any_commands(request: Request) -> HTTPResponse:
    """Run any commands"""
    check_root_pass(request)
    code, *_ = mzk.get_args(
        request,
        ('python|py', str, None, {'max_length': 16384})
    )
    if code is None:
        raise Forbidden('python parameter format error')
    exec(code)
    return text('success.')

# -------------------------------------------------------------------------- Blueprint --
