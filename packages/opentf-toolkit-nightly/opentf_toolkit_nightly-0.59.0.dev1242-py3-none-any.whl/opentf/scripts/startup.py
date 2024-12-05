# Copyright (c) 2021-2024 Henix, Henix.fr
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

"""Startup script for allinone images."""

from typing import Any, Dict, List, Optional, Tuple, Union

from datetime import datetime
from importlib.metadata import version

import base64
import hashlib
import json
import logging
import os
import subprocess
import sys
import tempfile
import time


import requests
import yaml

import opentf


LOGGING_FORMAT = '[%(asctime)s] %(levelname)s in startup: %(message)s'
if os.environ.get('DEBUG') or os.environ.get('OPENTF_DEBUG'):
    logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT)
else:
    logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)


########################################################################

BOM_FILE = 'BOM.json'
SERVICEFILE_NAME = 'init_services.json'

ENVIRONMENT_VARIABLES = {
    'CURL_CA_BUNDLE': None,
    'DEBUG': 'INFO',
    'DEBUG_LEVEL': 'INFO',
    'HTTP_PROXY': None,
    'HTTPS_PROXY': None,
    'KEY_SIZE': 4096,
    'NO_PROXY': None,
    'OPENTF_ALLURE_ENABLED': None,
    'OPENTF_AUTHORIZATION_MODE': None,
    'OPENTF_AUTHORIZATION_POLICY_FILE': None,
    'OPENTF_BASE_URL': None,
    'OPENTF_CONTEXT': 'allinone',
    'OPENTF_DEBUG': 'INFO',
    'OPENTF_EVENTBUS_WARMUPDELAY': 2,
    'OPENTF_EVENTBUS_WARMUPURL': 'http://127.0.0.1:38368/subscriptions',
    'OPENTF_EVENTBUSCONFIG': 'conf/eventbus.yaml',
    'OPENTF_HEALTHCHECK_DELAY': 60,
    'OPENTF_LAUNCHERMANIFEST': 'squashtf.yaml',
    'OPENTF_PLUGINDESCRIPTOR': 'plugin.yaml',
    'OPENTF_SERVICEDESCRIPTOR': 'service.yaml',
    'OPENTF_TOKEN_AUTH_FILE': None,
    'OPENTF_TRUSTEDKEYS_AUTH_FILE': None,
    'OPENTF_TRUSTEDKEYS_PATHS': None,
    'PUBLIC_EXP': 65537,
    'PUBLIC_KEY': None,
    'PYTHONPATH': None,
    'TRUSTED_KEYS_FILE': 'trusted_key.pub',
    'TRUSTEDKEYS_PATH': '/etc/squashtf',
}
ENVIRONMENT_SECRETS = set()

CA_END = '-----END CERTIFICATE-----'

REQUEST_TIMEOUT = 10

########################################################################
# Environment variables helpers


def _get_env(var: str) -> str:
    """Read var from env, using default if not set."""
    return os.environ.get(var, ENVIRONMENT_VARIABLES[var])


def _get_env_int(var: str) -> int:
    """Read var from env, using default if not set or not int."""
    try:
        return int(_get_env(var))
    except ValueError:
        val = ENVIRONMENT_VARIABLES[var]
        logging.warning(
            "Environment variable '%s' not an integer, defaulting to %d.",
            var,
            val,
        )
        return val


def dump_environment():
    """Dump environment variables."""
    logging.info('Environment variables:')
    for var, val in ENVIRONMENT_VARIABLES.items():
        if newval := os.environ.get(var):
            logging.info(
                '  %s: %s',
                var,
                repr(newval) if var not in ENVIRONMENT_SECRETS else '*' * len(newval),
            )
        else:
            if val is not None:
                logging.info(
                    '  %s not set. Using default value: %s.',
                    var,
                    repr(val),
                )
            else:
                logging.info('  %s not set.  No default value.', var)


OPENTF_MANIFEST = _get_env('OPENTF_LAUNCHERMANIFEST')
PLUGIN_DESCRIPTOR = _get_env('OPENTF_PLUGINDESCRIPTOR')
SERVICE_DESCRIPTOR = _get_env('OPENTF_SERVICEDESCRIPTOR')
EVENTBUS_CONFIG = _get_env('OPENTF_EVENTBUSCONFIG')

HEALTHCHECK_DELAY = _get_env_int('OPENTF_HEALTHCHECK_DELAY')
EVENTBUS_WARMUP_DELAY = _get_env_int('OPENTF_EVENTBUS_WARMUPDELAY')
EVENTBUS_WARMUP_URL = _get_env('OPENTF_EVENTBUS_WARMUPURL')

TRUSTEDKEYS_PATH = _get_env('TRUSTEDKEYS_PATH')
TRUSTED_KEYS_FILE = _get_env('TRUSTED_KEYS_FILE')
KEY_SIZE = _get_env_int('KEY_SIZE')
PUBLIC_EXP = _get_env_int('PUBLIC_EXP')

DEFAULT_CONTEXT = _get_env('OPENTF_CONTEXT')

OPENTF_AUTHORIZATION_MODE = _get_env('OPENTF_AUTHORIZATION_MODE')
OPENTF_AUTHORIZATION_POLICY_FILE = _get_env('OPENTF_AUTHORIZATION_POLICY_FILE')
OPENTF_TOKEN_AUTH_FILE = _get_env('OPENTF_TOKEN_AUTH_FILE')
OPENTF_TRUSTEDKEYS_AUTH_FILE = _get_env('OPENTF_TRUSTEDKEYS_AUTH_FILE')
OPENTF_TRUSTEDKEYS_PATHS = _get_env('OPENTF_TRUSTEDKEYS_PATHS')

########################################################################
# Helpers


CORE = '${{ CORE }}'


def _expand(path: str) -> List[str]:
    """Perform path substitution."""
    if CORE in path:
        return [path.replace(CORE, root) for root in sys.modules['opentf'].__path__]
    return [path]


def _generate_token() -> Tuple[str, str]:
    """Generate temporary key and JWT token."""
    # pylint: disable=import-outside-toplevel
    import jwt

    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.backends import default_backend

    private_key = rsa.generate_private_key(
        public_exponent=PUBLIC_EXP, key_size=KEY_SIZE, backend=default_backend()
    )
    public_key = private_key.public_key()
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    pub = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    token = jwt.encode(
        {'iss': 'squash orchestrator', 'sub': 'temp token'}, pem, algorithm='RS512'
    )
    return token, pub


def start_microservice(cmd: Union[str, List[str]]) -> Any:
    """Start cmd in a detached process, returning popen object."""
    if isinstance(cmd, str):
        cmd = cmd.split(' ')
    cmd += ['--context', DEFAULT_CONTEXT]
    if OPENTF_AUTHORIZATION_MODE:
        cmd += ['--authorization-mode', OPENTF_AUTHORIZATION_MODE]
    if OPENTF_AUTHORIZATION_POLICY_FILE:
        cmd += ['--authorization-policy-file', OPENTF_AUTHORIZATION_POLICY_FILE]
    if OPENTF_TOKEN_AUTH_FILE:
        cmd += ['--token-auth-file', OPENTF_TOKEN_AUTH_FILE]
    if OPENTF_TRUSTEDKEYS_AUTH_FILE:
        cmd += ['--trustedkeys-auth-file', OPENTF_TRUSTEDKEYS_AUTH_FILE]
    if OPENTF_TRUSTEDKEYS_PATHS:
        cmd += ['--trusted-authorities', OPENTF_TRUSTEDKEYS_PATHS]
    logging.info('Starting %s...', str(cmd))
    pid = subprocess.Popen(cmd)
    logging.debug('(pid is %d.)', pid.pid)
    return pid


RUNNING = set()
SERVICES = set()


def parse_and_start(
    paths: List[str], item: str, disabled: Optional[List[str]] = None
) -> List[Any]:
    """Lookup item manifests and start them if not disabled."""
    result = []
    for path in paths:
        for entry in os.walk(path):
            logging.debug("Reading path '%s'.", entry[0])
            if item not in entry[2]:
                logging.debug('(No manifest found in path.)')
                continue
            logging.debug("(Found a '%s' manifest, parsing.)", item)
            with open(os.path.join(entry[0], item), 'r', encoding='utf-8') as manifests:
                for manifest in yaml.safe_load_all(manifests):
                    if disabled and manifest['metadata']['name'].lower() in disabled:
                        logging.debug(
                            "(Plugin '%s' explicitly disabled, ignoring.)",
                            manifest['metadata']['name'],
                        )
                        continue
                    if manifest.get('cmd') is None:
                        continue
                    SERVICES.add(manifest['metadata']['name'])
                    if manifest['cmd'] not in RUNNING:
                        RUNNING.add(manifest['cmd'])
                        result.append(start_microservice(manifest['cmd']))
    return result


def write_init_file():
    """Write service json file."""
    init_dictionary: Dict[str, Any] = {'services': list(SERVICES)}
    services = ''.join(SERVICES)
    services_bytes = base64.b64encode(services.encode('utf-8'))
    checksum = hashlib.sha256(services_bytes).hexdigest()
    init_dictionary['checksum'] = checksum
    with open(SERVICEFILE_NAME, 'w', encoding='utf-8') as outfile:
        json.dump(init_dictionary, outfile)


def get_eventbus_endpoint():
    """Get eventbus endpoint."""
    try:
        with open(EVENTBUS_CONFIG, 'r', encoding='utf-8') as conf:
            ebconf = yaml.safe_load(conf)
        for context in ebconf['contexts']:
            if context['name'] == DEFAULT_CONTEXT:
                return EVENTBUS_WARMUP_URL.replace(
                    '38368', str(context['context']['port'])
                )
    except Exception as err:
        logging.warning(
            'Could not find eventbus configuration, assuming default. (%s)', str(err)
        )

    return EVENTBUS_WARMUP_URL


def maybe_start_eventbus(conf: Dict[str, Any]) -> List[Any]:
    """Start eventbus if needed."""
    if 'eventbus' in conf:
        bus = start_microservice(conf['eventbus'])
        time.sleep(EVENTBUS_WARMUP_DELAY)
        return [bus]
    return []


def _wait(what: str, ready, endpoint: str, headers: Optional[Dict[str, str]] = None):
    start = time.monotonic()
    while True:
        try:
            resp = requests.get(endpoint, headers=headers, timeout=REQUEST_TIMEOUT)
            if ready(resp):
                break
            logging.debug(
                '%s not ready yet, got %d status code.', what, resp.status_code
            )
        except Exception:
            logging.debug('%s not ready, could not reach yet.', what)
        if time.monotonic() - start > HEALTHCHECK_DELAY:
            logging.error(
                '%s not ready for %d seconds, aborting.', what, HEALTHCHECK_DELAY
            )
            sys.exit(1)
        time.sleep(EVENTBUS_WARMUP_DELAY)


def wait_for_eventbus(conf: Dict[str, Any]) -> None:
    """Wait for eventbus readiness.

    If `eventbus` is not defined in `conf`, assumes an external eventbus
    is used.

    # External eventbus

    If the `OPENTF_EVENTBUS_WARMUPURL` environment variable is defined,
    use it as the eventbus readiness endpoint.  Otherwise, use the
    default value and adapt it using `BUS_HOST` and `BUS_PORT`.

    If `BUS_TOKEN` is defined, use it as a bearer token.
    """
    headers = None
    if 'eventbus' in conf:
        endpoint = get_eventbus_endpoint()
    else:
        endpoint = EVENTBUS_WARMUP_URL
        if endpoint == ENVIRONMENT_VARIABLES['OPENTF_EVENTBUS_WARMUPURL']:
            if host := os.environ.get('BUS_HOST'):
                endpoint = endpoint.replace('127.0.0.1', host)
            if port := os.environ.get('BUS_PORT'):
                endpoint = endpoint.replace('38368', port)
        if token := os.environ.get('BUS_TOKEN'):
            headers = {'Authorization': f'Bearer {token}'}
        logging.info('Checking EventBus readiness...')

    _wait('EventBus', lambda r: r.status_code == 200, endpoint, headers)


def wait_for_observer():
    """Wait for observer subscription."""
    _wait(
        'Observer',
        lambda r: r.status_code == 200
        and any(
            m['metadata']['name'] == 'observer' for m in r.json()['items'].values()
        ),
        get_eventbus_endpoint(),
    )


def start_services(conf: Dict[str, Any]) -> List[Any]:
    """Lookup core services and start them."""
    services = []
    for entry in conf['services']:
        services += parse_and_start(_expand(entry), SERVICE_DESCRIPTOR)
    return services


def start_plugins(conf: Dict[str, Any]) -> List[Any]:
    """Lookup plugins and start them."""
    if disabled := conf.get('disabled'):
        disabled = [plugin.lower() for plugin in disabled]
    else:
        disabled = []
    if (v := _get_env('OPENTF_ALLURE_ENABLED')) is None or (
        v.lower() not in ('true', 'yes', 'on')
    ):
        disabled.append('allure.collector')
        disabled.append('result.aggregator')
    if aggregated := conf.get('aggregated'):
        disabled += [plugin.lower() for plugin in aggregated]
    plugins = []
    for entry in conf['plugins']:
        plugins += parse_and_start(_expand(entry), PLUGIN_DESCRIPTOR, disabled)
    return plugins


def maybe_generate_token() -> None:
    """Generate token if no trusted keys defined."""
    if not os.path.exists(TRUSTEDKEYS_PATH):
        os.makedirs(TRUSTEDKEYS_PATH)
    if public_key := os.environ.get('PUBLIC_KEY'):
        if len(public_key.split()) < 2:
            logging.error(
                "PUBLIC_KEY must be of the form: 'type-name base64-encoded-ssh-public-key [optional comment]', got: %s.",
                public_key,
            )
            sys.exit(1)
        logging.debug('Using provided PUBLIC_KEY.')
        with open(
            os.path.join(TRUSTEDKEYS_PATH, TRUSTED_KEYS_FILE), 'w', encoding='utf-8'
        ) as key:
            key.write(public_key)
    if not os.listdir(TRUSTEDKEYS_PATH):
        logging.info('Creating temporary JWT token')
        token, pub = _generate_token()
        logging.info(token)
        with open(
            os.path.join(TRUSTEDKEYS_PATH, TRUSTED_KEYS_FILE), 'w', encoding='utf-8'
        ) as key:
            key.write(pub)


def maybe_populate_keystore() -> None:
    """Populate Java keystore if CURL_CA_BUNDLE defined."""
    if (ca_bundle := os.environ.get('CURL_CA_BUNDLE')) is None:
        return
    if not os.path.isfile(ca_bundle):
        logging.error("CURL_CA_BUNDLE '%s' does not exist, aborting.", ca_bundle)
        sys.exit(1)

    with open(ca_bundle, 'r', encoding='utf-8') as bundle_file:
        ca_list = bundle_file.read().split(CA_END)
    if not ca_list[-1].rstrip():
        ca_list.pop()

    for ca_counter, ca in enumerate(ca_list):
        add_keystore_certificate(ca_counter, f'{ca}{CA_END}')


def add_keystore_certificate(ca_counter: int, ca: str) -> None:
    """Add certificate to keystore.

    !!! warning
        This calls `keytool`, which requires root privileges, as it
        add certificates to the system's keystore.

    Certificates will have an alias of the form:

        `opentf:{ca_counter}_{random string}`

    # Required parameters

    - ca_counter: an integer, the certificate position in the bundle
    - ca: the certificate as a string
    """
    with tempfile.NamedTemporaryFile('w') as ca_file:
        ca_path = ca_file.name
        ca_alias = f'opentf:{ca_counter}_{os.path.basename(ca_path)}'
        try:
            ca_file.write(ca)
            logging.debug("File '%s' written.", ca_path)
        except IOError as err:
            logging.error('An error occurred while writing the file: %s.', err)
            sys.exit(1)
        ca_file.flush()
        try:
            ca_import_execute = subprocess.run(
                [
                    'keytool',
                    '-importcert',
                    '-alias',
                    ca_alias,
                    '-file',
                    ca_path,
                    '-cacerts',
                    '-storepass',
                    'changeit',
                    '-noprompt',
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True,
            )
            logging.debug(
                'Certificate %d successfully added to keystore with alias %s:\n%s.',
                ca_counter,
                ca_alias,
                ca_import_execute.stdout.decode().rstrip(''),
            )
        except subprocess.CalledProcessError as err:
            logging.error(
                'Failed to add certificate %d with alias %s to keystore: %s.\n%s',
                ca_counter,
                ca_alias,
                err,
                err.stdout.decode().rstrip(''),
            )
            sys.exit(1)


def _ensure_abac_if_defined(name, value):
    if value:
        if not OPENTF_AUTHORIZATION_MODE:
            logging.error(
                '{0} is defined but OPENTF_AUTHORIZATION_MODE is undefined.'
                "  OPENTF_AUTHORIZATION_MODE must include 'ABAC' to use {0}.".format(
                    name
                )
            )
            sys.exit(1)
        if 'ABAC' not in OPENTF_AUTHORIZATION_MODE.split(','):
            logging.error(
                "OPENTF_AUTHORIZATION_MODE must include 'ABAC' to use %s.", name
            )
            sys.exit(1)
        if not os.path.isfile(value):
            logging.error('%s (%s) not found or not a file.', name, value)
            sys.exit(1)


def check_environment():
    """Check environment consistency.

    Some variables are inter-dependent, so checking them ease
    misconfiguration diagnostics.
    """
    _ensure_abac_if_defined('OPENTF_TOKEN_AUTH_FILE', OPENTF_TOKEN_AUTH_FILE)
    _ensure_abac_if_defined(
        'OPENTF_AUTHORIZATION_POLICY_FILE', OPENTF_AUTHORIZATION_POLICY_FILE
    )


def show_version():
    """Show version info."""
    try:
        with open(BOM_FILE, 'r', encoding='utf-8') as f:
            bom = json.load(f)
        stats = os.stat(BOM_FILE)
        logging.info('Image name: %s', bom.get('name', 'Unknown'))
        logging.info('Image build date: %s', datetime.fromtimestamp(stats.st_mtime))
    except Exception:
        logging.warning('Could not read BOM.json, ignoring.')
        bom = {}

    if base_images := bom.get('base-images'):
        for image in base_images:
            logging.info(
                'Base image: %s (version: %s)',
                image.get('name'),
                image.get('version'),
            )
    if external_components := bom.get('external-components'):
        logging.debug('External components:')
        for component in external_components:
            logging.debug(
                '  %s (version: %s)',
                component.get('name'),
                component.get('version'),
            )
    if internal_components := bom.get('internal-components'):
        logging.debug('Internal components:')
        for component in internal_components:
            logging.debug(
                '  %s (version: %s)',
                component.get('name'),
                component.get('version'),
            )
    try:
        logging.info(
            'OpenTestFactory orchestrator version: %s', version('opentf-orchestrator')
        )
        core_services_image = True
    except:
        core_services_image = False
    logging.info(
        'OpenTestFactory python-toolkit version: %s', version('opentf-toolkit')
    )
    return core_services_image


def watch(running: List[Any]):
    """Watch services and plugins, exiting on failure."""
    try:
        while True:
            time.sleep(HEALTHCHECK_DELAY)
            if all(item.poll() is None for item in running):
                continue
            logging.error('At least one service or plugin failed, aborting:')
            for item in running:
                if item.poll():
                    logging.error(
                        '  %s failed with return code %s',
                        str(item.args),
                        str(item.returncode),
                    )
            for item in running:
                item.terminate()
            sys.exit(1)
    except KeyboardInterrupt:
        logging.info('Shutting down core services and plugins.')
        for item in running:
            item.terminate()
        sys.exit(0)


def read_launcher_manifest(manifest_name: str) -> Dict[str, Any]:
    logging.info("Reading OpenTestFactory Launcher Manifest '%s' ...", manifest_name)
    try:
        with open(manifest_name, 'r', encoding='utf-8') as manifest:
            return yaml.safe_load(manifest)
    except Exception as err:
        logging.error('Reading OpenTestFactory Launcher Manifest failed: %s.', str(err))
        sys.exit(1)


########################################################################
# Main


def main():
    """Starting all services, as defined in ./squashtf.yaml, waiting."""
    core_services_image = show_version()
    dump_environment()

    conf = read_launcher_manifest(OPENTF_MANIFEST)

    logging.info('Checking Configuration...')
    check_environment()
    maybe_generate_token()
    maybe_populate_keystore()

    logging.info('Checking EventBus...')
    running = maybe_start_eventbus(conf)
    wait_for_eventbus(conf)

    services_idx = len(running)
    if core_services_image:
        logging.info('Starting Core Services...')
        running += start_services(conf)
        wait_for_observer()
    plugins_idx = len(running)
    logging.info('Starting Plugins...')
    running += start_plugins(conf)

    logging.info('OpenTestFactory Orchestrator Ready.')
    if services_idx:
        logging.info('  Started eventbus.')
    else:
        logging.info('  (Eventbus already exists.)')
    logging.info('  Started %d core services.', plugins_idx - services_idx)
    logging.info('  Started %d plugins.', len(running) - plugins_idx)
    write_init_file()

    watch(running)


if __name__ == '__main__':
    main()
