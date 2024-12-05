# Copyright (c) 2021 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helpers for the OpenTestFactory orchestrator services."""

from typing import Any, Dict, List, NoReturn, Optional, Tuple, Union

import logging
import os
import sys

from functools import wraps
from uuid import uuid4, UUID

import jwt

from flask import Flask, current_app, make_response, request, g, Response

from toposort import toposort, CircularDependencyError

from .config import (
    ConfigError,
    make_argparser,
    configure_logging,
    read_config,
    read_descriptor,
    get_named,
    get_debug_level,
)
from .auth import (
    initialize_authn_authz,
    get_user_accessible_namespaces,
    is_user_authorized,
)
from .pubsub import make_dispatchqueue, make_event, publish, subscribe, unsubscribe
from .schemas import *


########################################################################
# Constants

DEFAULT_NAMESPACE = 'default'

# Misc. constants

DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'Strict-Transport-Security': 'max-age=31536000; includeSubdomains',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'no-referrer',
    'Content-Security-Policy': 'default-src \'none\'',
}

REASON_STATUS = {
    'OK': 200,
    'Created': 201,
    'Accepted': 202,
    'NoContent': 204,
    'PartialContent': 206,
    'BadRequest': 400,
    'Unauthorized': 401,
    'PaymentRequired': 402,
    'Forbidden': 403,
    'NotFound': 404,
    'AlreadyExists': 409,
    'Conflict': 409,
    'RangeNotSatisfiable': 416,
    'Invalid': 422,
    'TooManyRequests': 429,  # https://datatracker.ietf.org/doc/html/rfc6585
    'InternalError': 500,
}

ALLOWED_ALGORITHMS = [
    'ES256',  # ECDSA signature algorithm using SHA-256 hash algorithm
    'ES384',  # ECDSA signature algorithm using SHA-384 hash algorithm
    'ES512',  # ECDSA signature algorithm using SHA-512 hash algorithm
    'RS256',  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-256 hash algorithm
    'RS384',  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-384 hash algorithm
    'RS512',  # RSASSA-PKCS1-v1_5 signature algorithm using SHA-512 hash algorithm
    'PS256',  # RSASSA-PSS signature using SHA-256 and MGF1 padding with SHA-256
    'PS384',  # RSASSA-PSS signature using SHA-384 and MGF1 padding with SHA-384
    'PS512',  # RSASSA-PSS signature using SHA-512 and MGF1 padding with SHA-512
]

ACCESSLOG_FORMAT = (
    '%(REMOTE_ADDR)s - %(REMOTE_USER)s '
    '"%(REQUEST_METHOD)s %(REQUEST_URI)s %(HTTP_VERSION)s" '
    '%(status)s %(bytes)s "%(HTTP_REFERER)s" "%(HTTP_USER_AGENT)s"'
)

PARAMETERS_KEY = '__PARAMETERS__'

########################################################################
# Config Helpers


def _add_securityheaders(resp):
    """Add DEFAULT_HEADERS to response."""
    for header, value in DEFAULT_HEADERS.items():
        resp.headers[header] = value
    return resp


def _is_authorizer_required() -> bool:
    """Check if ABAC or RBAC is enabled for service."""
    return current_app and (
        'RBAC' in current_app.config['CONTEXT'].get('authorization_mode', [])
        or 'ABAC' in current_app.config['CONTEXT'].get('authorization_mode', [])
    )


def _check_token(authz: str, context: Dict[str, Any]) -> Optional[Response]:
    """Check token validity.

    Token is checked against known trusted authorities and then against
    `token_auth_file`, if any.

    The thread-local object `g` is filled with a `payload` entry (the
    token payload in JWT mode, `{"sub": "username"}` in ABAC mode) and
    possibly a `namespaces` entry (in JWT mode).

    # Required parameters

    - authz: a string ('bearer xxxxxx')
    - context: a dictionary

    # Returned value

    None if the the bearer token is valid.  A status response if the
    token is invalid.
    """
    parts = authz.split()
    if not parts or parts[0].lower() != 'bearer' or len(parts) != 2:
        logging.error(authz)
        return make_status_response('Unauthorized', 'Invalid Authorization header.')
    for mode in context.get('authorization_mode', []) + ['JWT']:
        if mode == 'JWT':
            for i, pubkey in enumerate(context['trusted_keys']):
                try:
                    payload = jwt.decode(
                        parts[1], pubkey[0], algorithms=ALLOWED_ALGORITHMS
                    )
                    logging.debug('Token signed by trusted key #%d', i)
                    g.payload = payload
                    g.namespaces = pubkey[1]
                    return None
                except (ValueError, AttributeError, jwt.InvalidKeyError) as err:
                    logging.error('Invalid trusted key #%d:', i)
                    logging.error(err)
                except jwt.InvalidAlgorithmError as err:
                    logging.error(
                        'Invalid algorithm while verifying token by trusted key #%d:', i
                    )
                    logging.error(err)
                except jwt.InvalidTokenError as err:
                    logging.debug('Token could not be verified by trusted key #%d:', i)
                    logging.debug(err)
        elif mode == 'ABAC':
            for user in context.get('authorization_tokens', []):
                if user[0] == parts[1]:
                    g.payload = {'sub': user[2]}
                    return None
    return make_status_response('Unauthorized', 'Invalid JWT token.')


def _get_contextparameter_spec(app: Flask, name: str) -> Optional[Dict[str, Any]]:
    """Get context parameter specification.

    Initialize cache if needed, ignoring context parameters specs from
    other services.

    Adds the `watchdog_polling_delay_seconds` spec.
    """
    if PARAMETERS_KEY not in app.config:
        app.config[PARAMETERS_KEY] = []
        for manifest in app.config['DESCRIPTOR']:
            if manifest.get('metadata', {}).get('name', '').lower() != app.name.lower():
                continue
            app.config[PARAMETERS_KEY] += manifest.get('spec', {}).get(
                'contextParameters', []
            )
        app.config[PARAMETERS_KEY] += [
            {
                'name': 'watchdog_polling_delay_seconds',
                'descriptiveName': 'polling delay in seconds',
                'default': 30,
                'type': 'int',
            }
        ]
        app.logger.info('Configuration:')
    parameters = app.config[PARAMETERS_KEY]
    try:
        spec = get_named(name, parameters)
    except ValueError:
        spec = None
    return spec


########################################################################


def list_accessible_namespaces(
    resource: Optional[str] = None, verb: Optional[str] = None
) -> List[str]:
    """Get the accessible namespaces.

    If called outside of a request context, returns `['*']`.

    # Optional parameters

    - resource: a string or None (None by default)
    - verb: a string or None (None by default)

    # Returned value

    A list of _namespaces_ (strings) or `['*']` if all namespaces are
    accessible.
    """
    if not g or g.get('insecure_login'):
        return ['*']
    if 'namespaces' in g:
        return list(g.namespaces)
    if 'payload' in g:
        return get_user_accessible_namespaces(
            g.payload['sub'], current_app.config['CONTEXT'], resource, verb
        )
    return []


def can_use_namespace(
    namespace: str, resource: Optional[str] = None, verb: Optional[str] = None
) -> bool:
    """Check if namespace is accessible for current request.

    If called outside of a request context, returns True.

    # Required parameters

    - namespace: a string

    # Optional parameters

    - resource: a string or None (None by default)
    - verb: a string or None (None by default)

    # Returned value

    A boolean.
    """
    namespaces = list_accessible_namespaces(resource, verb)
    return namespace in namespaces or '*' in namespaces


def authorizer(resource: str, verb: str):
    """Decorate a function by adding an access control verifier.

    # Required parameters

    - resource: a string
    - verb: a string

    # Returned value

    The decorated function, unchanged if no authorizer required.

    The decorated function, which is expected to be a endpoint, will
    reject incoming requests if access control is enabled and the
    requester does not have the necessary rights.
    """

    def inner(function):
        """Ensure the incoming request has the required authorization"""

        @wraps(function)
        def wrapper(*args, **kwargs):
            if not _is_authorizer_required() or not g or g.get('insecure_login'):
                return function(*args, **kwargs)
            payload = g.get('payload')
            if not payload:
                return make_status_response('Unauthorized', 'No JWT payload.')
            user = payload['sub']
            if 'namespaces' not in g and not is_user_authorized(
                user, resource, verb, current_app.config['CONTEXT']
            ):
                return make_status_response(
                    'Forbidden',
                    f'User {user} is not authorized to {verb} {resource}.',
                )
            return function(*args, **kwargs)

        return wrapper

    return inner


def _make_authenticator(context: Dict[str, Any]):
    """Make an authenticator function tied to context."""

    def inner():
        """Ensure the incoming request is authenticated.

        If from localhost, allow.

        If from somewhere else, ensure there is a valid token attached.
        """
        if context.get('enable_insecure_login') and request.remote_addr == context.get(
            'insecure_bind_address'
        ):
            g.insecure_login = True
            return None
        authz = request.headers.get('Authorization')
        if authz is None:
            return make_status_response('Unauthorized', 'No Bearer token')
        return _check_token(authz, context)

    return inner


def get_actor() -> Optional[str]:
    """Get actor.

    # Returned value

    The subject (user), if authenticated.  None otherwise.
    """
    if g and 'payload' in g:
        return g.payload.get('sub')
    return None


class EventbusLogger(logging.Handler):
    """A Notification logger.

    A logging handler that posts Notifications if the workflow is
    known.

    Does nothing if the log event is not patched to a workflow.

    If `silent` is set to False, will print on stdout whenever it fails
    to send notifications.
    """

    def __init__(self, silent: bool = True):
        self.silent = silent
        super().__init__()

    def emit(self, record):
        if request and 'workflow_id' in g:
            try:
                publish(
                    make_event(
                        NOTIFICATION,
                        metadata={
                            'name': 'log notification',
                            'workflow_id': g.workflow_id,
                        },
                        spec={'logs': [self.format(record)]},
                    ),
                    current_app.config['CONTEXT'],
                )
            except Exception:
                if not self.silent:
                    print(
                        f'{record.name}: Could not send notification to workflow {g.workflow_id}.'
                    )


def make_app(
    name: str,
    description: str,
    configfile: Optional[str] = None,
    schema: Optional[str] = None,
    defaultcontext: Optional[Dict[str, Any]] = None,
    descriptor: Optional[Union[str, Dict[str, Any], List[Dict[str, Any]]]] = None,
) -> Flask:
    """Create a new app.

    # Required parameters

    - name: a string
    - description: a string

    # Optional parameters

    - configfile: a string or None (None by default)
    - schema: a string or None (None by default)
    - defaultcontext: a dictionary or None (None by default)
    - descriptor: a filename, a dictionary, a list of dictionaries, or
      None (None by default)

    # Returned value

    A new flask app (not started).  Three entries are added to
    `app.config`: `CONFIG`, `CONTEXT`, and `DESCRIPTOR`.

    `CONFIG` is a dictionary, the complete config file.  `CONTEXT` is a
    subset of `CONFIG`, the current entry in `CONFIG['context']`.  It is
    also a dictionary.  `DESCRIPTOR` is the service descriptor.

    # Raised Exception

    Exits with code error 2 if the context is not found or if the config
    file is invalid.
    """
    configfile = configfile or f'conf/{name}.yaml'
    args = make_argparser(description, configfile).parse_args()

    configure_logging(name, get_debug_level(name))
    app = Flask(name)
    try:
        context, config = read_config(
            args.config, args.context, configfile, defaultcontext, schema
        )

        if args.descriptor or descriptor is None or isinstance(descriptor, str):
            _, descriptor = read_descriptor(args.descriptor, descriptor)

        if args.host:
            context['host'] = args.host
        if args.port:
            context['port'] = args.port
        if args.ssl_context:
            context['ssl_context'] = args.ssl_context

        initialize_authn_authz(args, context)
    except ConfigError as err:
        app.logger.error(err)
        sys.exit(2)

    app.config['CONTEXT'] = context
    app.config['CONFIG'] = config
    app.config['DESCRIPTOR'] = (
        descriptor if isinstance(descriptor, list) else [descriptor]
    )
    app.before_request(_make_authenticator(context))
    app.after_request(_add_securityheaders)
    return app


def get_context_parameter(
    app: Flask,
    name: str,
    validator: Optional[Any] = None,
    default: Optional[Any] = None,
) -> Any:
    """Get an integer parameter from configuration context.

    Exits with an error code of 2 if the parameter is not properly
    valued or is not defined.

    Resolution order:

    - `{app.name.upper()}_{name.upper()}` environment variable
    - `{name.upper()}` environment variable (if spec is shared)
    - `name` in configuration context
    - `spec['default']` if spec defines a default value
    - `default` if not None

    # Required parameters

    - app: a Flask object
    - name: a string

    # Optional parameters

    - validator: a function of two arguments or None (None by default)
    - default: any value or None (None by default)

    # Returned value

    An integer if the parameter has a specification and is expected to
    be of type int.  The actual parameter type otherwise.
    """

    def _maybe_validate(v) -> int:
        newv, reason = validator(name, v) if validator else (v, None)
        lhs = f'  {spec["descriptiveName"]} ({name}):' if spec else f'  {name}:'
        if newv != v:
            app.logger.info(f'{lhs} {newv} (was defined as {v}, but {reason})')
        else:
            app.logger.info(f'{lhs} {newv}')
        return newv

    def _fatal(*msg) -> NoReturn:
        app.logger.error(*msg)
        sys.exit(2)

    spec = _get_contextparameter_spec(app, name)
    val = os.environ.get(name.upper()) if spec and spec.get('shared') else None
    val = os.environ.get(f'{app.name.upper()}_{name.upper()}', val)
    if val is None and name not in app.config['CONTEXT']:
        if spec and 'default' in spec:
            return _maybe_validate(spec['default'])
        if default is not None:
            return _maybe_validate(default)
        _fatal(
            'Context parameter %s not in current context and no default value specified.',
            name,
        )

    val = val if val is not None else app.config['CONTEXT'][name]
    if not spec:
        return _maybe_validate(val)
    if spec.get('type') == 'int':
        try:
            val = int(val)
        except ValueError as err:
            _fatal('Context parameter %s not an integer: %s.', name, str(err))
    desc = spec['descriptiveName'][0].upper() + spec['descriptiveName'][1:]
    if 'minValue' in spec and val < spec['minValue']:
        _fatal(f'{desc} must be greater than {spec["minValue"]-1}.')
    if 'maxValue' in spec and val > spec['maxValue']:
        _fatal(f'{desc} must be less that {spec["maxValue"]+1}.')
    return _maybe_validate(val)


def get_context_service(app: Flask, service: str) -> Dict[str, Any]:
    """Get service specification from configuration context.

    Exits with an error code of 2 if the service is missing.

    # Required parameters

    - app: a Flask object
    - service: a string

    # Returned value

    A dictionary.
    """
    if definition := app.config['CONTEXT'].get('services', {}).get(service):
        return definition
    app.logger.error(
        '.services.%s specification missing in configuration context.',
        service,
    )
    sys.exit(2)


def run_app(app: Flask) -> None:
    """Start the app.

    Using waitress as the wsgi server.  The logging service is
    configured to only show waitress errors and up messages.

    Access logs are only displayed when in DEBUG mode.
    """
    context = app.config['CONTEXT']

    from waitress import serve

    if get_debug_level(app.name) == 'DEBUG':
        from paste.translogger import TransLogger

        _app = TransLogger(app, format=ACCESSLOG_FORMAT, setup_console_handler=False)
    else:
        logging.getLogger('waitress').setLevel('ERROR')
        app.logger.info(f'Serving on http://{context["host"]}:{context["port"]}')
        _app = app

    serve(
        _app,
        host=context['host'],
        port=context['port'],
        server_name=app.name,
        threads=get_context_parameter(app, 'waitress_threads_count', default=4),
    )


########################################################################
## Misc. helpers


def make_uuid() -> str:
    """Generate a new uuid as a string."""
    return str(uuid4())


def is_uuid(uuid: str) -> bool:
    """Check if a string is a uuid.

    # Required parameters

    - uuid: a string

    # Returned value

    A boolean.
    """
    try:
        UUID(uuid)
        return True
    except ValueError:
        return False


########################################################################
# API Server Helpers


def make_status_response(
    reason: str,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    silent: bool = False,
) -> Response:
    """Return a new status response object.

    # Required parameters

    - reason: a non-empty string (must exist in `REASON_STATUS`)
    - message: a string

    # Optional parameters:

    - details: a dictionary or None (None by default)
    - silent: a boolean (False by default)

    # Returned value

    A _flask.Response_.  Its body is a _status_ JSON object.  It has
    the following entries:

    - kind: a string (`'Status'`)
    - apiVersion: a string (`'v1'`)
    - metadata: an empty dictionary
    - status: a string (either `'Success'` or `'Failure'`)
    - message: a string (`message`)
    - reason: a string (`reason`)
    - details: a dictionary or None (`details`)
    - code: an integer (derived from `reason`)
    """
    code = REASON_STATUS[reason]
    if not silent:
        if code // 100 == 4:
            logging.warning(message)
        elif code // 100 == 5:
            logging.error(message)
    return make_response(
        {
            'kind': 'Status',
            'apiVersion': 'v1',
            'metadata': {},
            'status': 'Success' if code // 100 == 2 else 'Failure',
            'message': message,
            'reason': reason,
            'details': details,
            'code': code,
        },
        code,
    )


def annotate_response(
    response: Response,
    links: Optional[List[str]] = None,
    processed: Optional[List[str]] = None,
) -> Response:
    """Annotate response with headers if appropriate.

    Handles 'Link' header (for RFC8288) and and `X-Processed-Query`
    header (specific, a comma-separated list of query parameter names)

    # Required parameters

    - response: a Flask Response object

    # Optional parameters

    - links: a list of strings or None
    - processed: a list of strings or None

    # Returned value

    `response`
    """
    if links:
        response.headers['Link'] = ','.join(links)
    if processed:
        if seen := {k for k in processed if request.args.get(k) is not None}:
            response.headers['X-Processed-Query'] = ','.join(seen)
    return response


########################################################################
# Pipelines Helpers


def validate_pipeline(
    workflow: Dict[str, Any]
) -> Tuple[bool, Union[str, List[List[str]]]]:
    """Validate workflow jobs, looking for circular dependencies.

    # Required parameters

    - workflow: a dictionary

    # Returned value

    A (`bool`, extra) pair.

    If there is a dependency on an non-existing job, returns
    `(False, description (a string))`.

    If there are circular dependencies in the workflow jobs, returns
    `(False, description (a string))`.

    If there are no circular dependencies, returns `(True, jobs)` where
    `jobs` is an ordered list of job names lists.  Each item in the
    returned list is a set of jobs that can run in parallel.
    """
    try:
        jobs = {}
        for job_name, job_definition in workflow['jobs'].items():
            if needs := job_definition.get('needs'):
                if isinstance(needs, list):
                    jobs[job_name] = set(needs)
                else:
                    jobs[job_name] = {needs}
            else:
                jobs[job_name] = set()
        for src, dependencies in jobs.items():
            for dep in dependencies:
                if dep not in jobs:
                    return (
                        False,
                        f"Job '{src}' has a dependency on job '{dep}' which does not exist.",
                    )

        return True, [list(items) for items in toposort(jobs)]
    except CircularDependencyError as err:
        return False, str(err)
