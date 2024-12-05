# Copyright (c) 2023 Henix, Henix.fr
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

"""Helpers for the OpenTestFactory subscription and publication API."""

from typing import Any, Dict, List, Optional

import sys
import threading

from datetime import datetime, timezone
from queue import Queue
from time import sleep


from requests import delete, post, Response

from .schemas import SUBSCRIPTION, validate_schema


########################################################################
# Publishers & Subscribers Helpers

DEFAULT_TIMEOUT_SECONDS = 10


def make_event(schema: str, **kwargs) -> Dict[str, Any]:
    """Return a new event dictionary.

    # Required parameters

    - schema: a string

    # Optional parameters

    A series of key=values

    # Returned value

    A dictionary.
    """
    apiversion, kind = schema.rsplit('/', 1)
    return {'apiVersion': apiversion, 'kind': kind, **kwargs}


def make_subscription(
    name: str, selector: Optional[Dict[str, Any]], target: str, context: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate a subscription manifest.

    # Required parameter

    - name: a string
    - selector: a dictionary or None
    - target: a string
    - context: a dictionary

    # Returned value

    A validated _subscription manifest_.

    # Raised exceptions

    A _ValueError_ exception is raised if the `selector` is not a valid
    subscription selector.
    """
    protocol = 'http' if context.get('ssl_context') == 'disabled' else 'https'
    hostname = context['eventbus'].get('hostname', context['host'])
    port = context['port']
    spec = {
        'subscriber': {
            'endpoint': f'{protocol}://{hostname}:{port}/{target.lstrip("/")}'
        }
    }
    if selector is not None:
        spec['selector'] = selector

    subscription = make_event(
        SUBSCRIPTION,
        metadata={
            'name': name,
            'creationTimestamp': datetime.now(timezone.utc).isoformat(),
        },
        spec=spec,
    )

    valid, extra = validate_schema(SUBSCRIPTION, subscription)
    if not valid:
        raise ValueError(f'Invalid subscription: {extra}')
    return subscription


def _do(req, path: str, eventbus: Dict[str, Any], **kwargs) -> Response:
    return req(
        eventbus['endpoint'].rstrip('/') + path,
        headers={'Authorization': f'Bearer {eventbus["token"]}'},
        verify=not eventbus.get('insecure-skip-tls-verify', False),
        timeout=DEFAULT_TIMEOUT_SECONDS,
        **kwargs,
    )


def _dispatch_events(dispatch_queue: Queue, fn, app, strategy) -> None:
    """Async event dispatch thread handler."""
    delay = 0
    while True:
        try:
            publication = dispatch_queue.get()
            try:
                fn(publication, app.config['CONTEXT'])
                delay = 0
            except Exception:
                dispatch_queue.put(publication)
                delay = min(2 * delay + 1, 60)
                app.logger.debug(
                    'Failed to dispatch publication, retrying in %d seconds.', delay
                )
                sleep(delay)
        except Exception as err:
            app.logger.error('Internal error while dispatching publication: %s.', err)


def subscribe(
    kind: Optional[str],
    target: str,
    app,
    labels: Optional[Dict[str, str]] = None,
    fields: Optional[Dict[str, str]] = None,
    expressions: Optional[List[Dict[str, Any]]] = None,
    fieldexpressions: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """Subscribe on specified endpoint.

    `kind` is of form `[apiVersion/]kind` or None.

    # Required parameters

    - kind: a string or None
    - target: a string
    - app: a flask app

    # Optional parameters

    - labels: a dictionary
    - fields: a dictionary
    - expressions: a dictionary
    - fieldexpressions: a dictionary

    # Returned value

    A _uuid_ (a string).

    # Raised exceptions

    Raise a _SystemExit_ exception (with exit code 1) if the
    subscription fails.
    """
    selector: Dict[str, Any] = {}
    if kind is not None:
        if '/' in kind:
            apiversion, kind = kind.rsplit('/', 1)
            if fields is None:
                fields = {}
            fields['apiVersion'] = apiversion
        selector['matchKind'] = kind
    if labels:
        selector['matchLabels'] = labels
    if expressions:
        selector['matchExpressions'] = expressions
    if fields:
        selector['matchFields'] = fields
    if fieldexpressions:
        selector['matchFieldExpressions'] = fieldexpressions

    context = app.config['CONTEXT']
    try:
        json = make_subscription(
            app.name, selector=selector or None, target=target, context=context
        )

        response = _do(post, '/subscriptions', context['eventbus'], json=json)

        if response.status_code == 201:
            return response.json()['details']['uuid']

        app.logger.error(
            'Could not subscribe to eventbus: was expecting 201, got status %d: %s.',
            response.status_code,
            response.text,
        )
    except Exception as err:
        app.logger.error('Could not subscribe to eventbus: %s.', err)

    sys.exit(1)


def unsubscribe(subscription_id: str, app) -> Response:
    """Cancel specified subscription

    #  Required parameters

    - subscription_id: a string (an uuid)
    - app: a flask app

    # Returned value

    A `requests.Response` object.
    """
    eventbus = app.config['CONTEXT']['eventbus']
    return _do(delete, f'/subscriptions/{subscription_id}', eventbus)


def publish(publication: Any, context: Dict[str, Any]) -> Response:
    """Publish publication on specified endpoint.

    If `publication` is a dictionary, and if it has a `metadata` entry,
    a `creationTimestamp` sub-entry will be created (or overwritten if
    it already exists).

    # Required parameters

    - publication: an object
    - context: a dictionary

    # Returned value

    A `requests.Response` object.
    """
    if isinstance(publication, dict) and 'metadata' in publication:
        publication['metadata']['creationTimestamp'] = datetime.now(
            timezone.utc
        ).isoformat()
    return _do(post, '/publications', context['eventbus'], json=publication)


def make_dispatchqueue(app, fn=publish, strategy=None) -> Queue:
    """Make an asynchronous dispatch queue.

    Handles publication failures by waiting for an increasing delay and
    re-attempting publication.

    The delay is at most 60 seconds.

    # Required parameters

    - app: a flask app

    # Optional parameters

    - fn: a function (`publish` by default)
    - stragegy: a dictionary or None (None by default)

    # Returned value

    A _queue_.  Events pushed to this queue will be published.
    """
    queue = Queue()
    app.logger.debug('Starting events dispatch thread.')
    try:
        threading.Thread(
            target=_dispatch_events, args=[queue, fn, app, strategy], daemon=True
        ).start()
        return queue
    except Exception as err:
        app.logger.error('Cound not start events dispatch thread: %s.', str(err))
        sys.exit(2)
