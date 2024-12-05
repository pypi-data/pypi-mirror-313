# Copyright (c) 2024 Henix, Henix.fr
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

"""Datasources (testcases, tags and jobs) retrieval helpers"""

from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

from datetime import datetime


from flask import current_app

from opentf.commons.expressions import evaluate_bool
from opentf.commons.selectors import match_selectors


########################################################################
# Constants

SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'
ERROR = 'ERROR'
SKIPPED = 'SKIPPED'
TOTAL = 'total count'

DETAILS_KEYS = ('failureDetails', 'errorDetails', 'warningDetails')
STATUSES_ORDER = (SUCCESS, FAILURE, ERROR, SKIPPED)
FAILURE_STATUSES = (FAILURE, ERROR)

PROVIDERCOMMAND = 'ProviderCommand'
EXECUTIONCOMMAND = 'ExecutionCommand'
EXECUTIONRESULT = 'ExecutionResult'
WORKFLOW = 'Workflow'
GENERATORRESULT = 'GeneratorResult'
CREATION_TIMESTAMP = 'creationTimestamp'

########################################################################
## Helpers


class DataSourceScopeError(Exception):
    """DataSourceScopeError class"""

    def __init__(self, msg, details=None):
        self.msg = msg
        self.details = details


class DataSourceDataError(Exception):
    """DataSourceDataError class"""

    def __init__(self, msg, details=None):
        self.msg = msg
        self.details = details


def _merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    for k, v in dict1.items():
        if k in dict2:
            dict2[k] = _merge_dicts(v.copy(), dict2[k])
    dict3 = dict1.copy()
    dict3.update(dict2)
    return dict3


def _as_list(what) -> List[str]:
    return [what] if isinstance(what, str) else what


def _get_metadata(
    filter_: Callable, events: Iterable[Dict[str, Any]], kind_: str
) -> Dict[str, Any]:
    """Get metadata of the first workflow event that satisfies filter.

    # Required parameters

    - filter_: a callable, filtering fuction
    - events: a list of events or iterator
    - kind_: a string, considered events kind

    # Returned value

    A possibly empty dictionary, the `.metadata` part of the
    first event that satisfies kind and filter conditions.
    """
    src = (event for event in events if event['kind'] == kind_)
    return next(filter(filter_, src), {}).get('metadata', {})


def parse_testcase_name(full_name: str) -> Tuple[str, str]:
    """Parse test case name from testResults notification.

    full_name is a string: classname#testcase name

    # Returned value

    A tuple of two strings: suite and test case name. If one
    of strings is empty, returns not empty element value instead.
    """
    suite, _, name = full_name.partition('#')
    return suite or name, name or suite


########################################################################
## Datasource: Testcases


def in_scope(expr: Union[str, bool], contexts: Dict[str, Any]) -> bool:
    """Safely evaluate datasource scope."""
    try:
        if isinstance(expr, bool):
            return expr
        return evaluate_bool(expr, contexts)
    except ValueError as err:
        raise ValueError(f'Invalid conditional {expr}: {err}.')
    except KeyError as err:
        raise ValueError(f'Nonexisting context entry in expression {expr}: {err}.')


def get_testresults(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return a possibly empty list of Notifications.

    Each notification in the list is guaranteed to have a
    `spec.testResults` entry.
    """
    return [item for item in events if _has_testresult(item)]


def _has_testresult(item: Dict[str, Any]) -> bool:
    """Determine if a workflow notification has a testResults element."""
    return item.get('kind') == 'Notification' and item.get('spec', {}).get(
        'testResults', False
    )


def _get_workflow_jobs(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Get workflow jobs that have steps.

    TOTO Will have to be reviewed when adding nested generators.

    # Required parameters

    - events: a list of events

    # Returned value

    A dictionary.  Keys are job names, values are a (dict, event) pair.

    - name: a string, the job's name and the generator's job_id, if any
    - job: a dictionary (its `runs-on` entry is a list of strings)
    - event: either a workflow or a generatorresult event.
    """

    def _clean(j):
        j['runs-on'] = _as_list(j.get('runs-on', []))
        return j

    jobs = {
        job_name + ' ' + event['metadata'].get('job_id', ''): (_clean(job), event)
        for event in filter(lambda x: x['kind'] in (WORKFLOW, GENERATORRESULT), events)
        for job_name, job in event.get('jobs', {}).items()
    }
    for job_name, (job, event) in jobs.items():
        if ' ' not in job_name.strip():
            # we do not have to patch top-level jobs
            continue
        if not event['metadata']['job_origin']:
            job['runs-on'] = list(
                set(
                    job['runs-on'] + jobs[event['metadata']['name'] + ' '][0]['runs-on']
                )
            )

    return {name: (job, event) for name, (job, event) in jobs.items() if 'steps' in job}


def _uses_inception(events: List[Dict[str, Any]]) -> bool:
    """Determine if a workflow is the inception workflow."""
    workflow_event = next(
        (event for event in events if event['kind'] == WORKFLOW), None
    )
    if not workflow_event:
        raise ValueError('No Workflow event in workflow events...')
    return any(
        'inception' in _as_list(job.get('runs-on', []))
        for job in workflow_event['jobs'].values()
    )


def _get_inception_testresults(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Get unique testResults notifications for inception workflow.

    Note: This is a kludge until we find a reliable way to map such results
    to the executed tests list.
    """
    unique_results = set()
    unique_events = []
    for event in get_testresults(events):
        event_results = []
        for result in event['spec']['testResults']:
            event_results.append(
                (
                    result['attachment_origin'],
                    result['name'],
                    result['duration'],
                    result['status'],
                )
            )
        if tuple(event_results) not in unique_results:
            unique_results.add(tuple(event_results))
            unique_events.append(event)
    return unique_events


def _get_testresult_params(param_step_id: str, job: Dict[str, Any]) -> Dict[str, Any]:
    """Get .with.data field of param_step_id.

    # Required parameters

    - param_step_id: a string
    - job: a dictionary

    # Returned value

    A dictionary, the `.with.data` part of the params step.

    # Raised exceptions

    An _IndexError_ exception is raised if no params step is found.
    """
    return [
        step['with']['data'] for step in job['steps'] if step.get('id') == param_step_id
    ].pop()


def _get_testcase_timestamps_and_job_id(step_origin: str, events: List[Dict[str, Any]]):
    def _is_origin_provider(event: Dict[str, Any]) -> bool:
        return event['metadata']['step_id'] == step_origin

    def _is_origin_execution(event: Dict[str, Any]) -> bool:
        return step_origin in event['metadata']['step_origin']

    creation = _get_metadata(_is_origin_provider, events, PROVIDERCOMMAND)
    start = _get_metadata(_is_origin_execution, events, EXECUTIONCOMMAND)
    end = _get_metadata(_is_origin_execution, reversed(events), EXECUTIONRESULT)

    return {
        CREATION_TIMESTAMP: creation.get(CREATION_TIMESTAMP, None),
        'startTime': start.get(CREATION_TIMESTAMP, None),
        'endTime': end.get(CREATION_TIMESTAMP, None),
        'job_id': creation.get('job_id', None),
    }


def _complete_labels(
    labels: Dict[str, Any],
    exec_step_id: str,
    managedtests: Dict[str, Any],
    job: Dict[str, Any],
) -> Dict[str, Any]:
    testcases = managedtests.get('testCases')
    if not testcases or exec_step_id not in testcases:
        if not testcases:
            current_app.logger.warning(
                f'Was expecting a "testCases" part in parent of step {exec_step_id}, ignoring.'
            )
        return labels

    labels['test']['managed'] = True
    testcase_metadata = testcases[exec_step_id]
    labels['test']['technology-name'] = testcase_metadata['technology']
    labels['test']['collection'] = managedtests.get('testPlan', {})
    labels['test'].update(
        {
            key: value
            for key, value in testcase_metadata.items()
            if key
            in (
                'name',
                'reference',
                'importance',
                'nature',
                'path',
                'type',
                'uuid',
            )
        }
    )
    try:
        params = _get_testresult_params(testcase_metadata['param_step_id'], job)
        labels['test']['global'] = params.get('global', {})
        labels['test']['data'] = params.get('test', {})
    except IndexError:
        current_app.logger.warning(
            f'Could not find "params" step associated to "execute" step {exec_step_id}, ignoring.'
        )
    return labels


def _create_testresult_labels(
    events: List[Dict[str, Any]],
    step_origin: str,
    exec_step: Dict[str, Any],
    job_name: str,
    job: Dict[str, Any],
    parent: Dict[str, Any],
) -> Dict[str, Any]:
    """Create labels for test result.

    # Required parameters

    - events: a list, workflow events
    - step_origin: a string, the 'execute' step uuid
    - exec_step: a dictionary, the 'execute' step
    - job_name: a string (the name of the job containing exec_step)
    - job: a dictionary, the job containing exec_step
    - parent: a dictionary, the event defining the job

    # Returned value

    A labels dictionary.
    """
    exec_step_id = exec_step['id']
    times_jobid = _get_testcase_timestamps_and_job_id(step_origin, events)
    labels = {
        'apiVersion': 'testing.opentestfactory.org/v1alpha1',
        'kind': 'TestCase',
        'metadata': {
            CREATION_TIMESTAMP: times_jobid[CREATION_TIMESTAMP],
            'execution_id': exec_step_id,
            'job_id': times_jobid['job_id'],
            'namespace': parent['metadata']['namespace'],
            'workflow_id': parent['metadata']['workflow_id'],
        },
        'test': {
            'job': job_name.split()[0],
            'managed': False,
            'runs-on': job['runs-on'],
            'technology': exec_step['uses'].partition('/')[0],
            'test': exec_step.get('with', {}).get('test'),
            'uses': exec_step['uses'],
        },
        'execution': {
            'startTime': times_jobid['startTime'],
            'endTime': times_jobid['endTime'],
        },
    }
    if not (managedtests := parent['metadata'].get('managedTests')):
        return labels
    return _complete_labels(labels, exec_step_id, managedtests, job)


def _get_testresult_steporigin(
    attachment_origin: str, events: List[Dict[str, Any]]
) -> Optional[str]:
    """Find the step that produced the attachment.

    # Required parameters

    - attachment_origin: a string (the attachment uuid)
    - events: a list of events

    # Returned value

    A step ID (a string) or None.
    """
    for event in events:
        if not (
            event['kind'] == EXECUTIONRESULT and event['metadata'].get('attachments')
        ):
            continue
        metadata = event['metadata']
        for value in metadata.get('attachments', {}).values():
            if value['uuid'] != attachment_origin:
                continue
            return (
                metadata['step_origin'][0]
                if metadata['step_origin']
                else metadata['step_id']
            )
    return None


def _get_testresult_labels(
    attachment_origin: str, events: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Get labels for test result.

    # Required parameters

    - attachment_origin: a string (the attachment uuid)
    - events: a list of events

    # Returned value

    A _labels_ dictionary or None.
    """
    if step_origin := _get_testresult_steporigin(attachment_origin, events):
        jobs_with_steps = _get_workflow_jobs(events)
        for job_name, (job, parent) in jobs_with_steps.items():
            for exec_step in job['steps']:
                if exec_step.get('id') == step_origin:
                    return _create_testresult_labels(
                        events, step_origin, exec_step, job_name, job, parent
                    )
    return None


def _make_testcase_from_testresult(
    item: Dict[str, Any], labels: Dict[str, Any], scope: Union[str, bool]
) -> Dict[str, Any]:
    suite_name, testcase_name = parse_testcase_name(item['name'])
    item_data = {
        'metadata': {
            'name': item['name'],
            'id': item['id'],
        },
        'test': {
            'outcome': item['status'].lower(),
            'suiteName': suite_name,
            'testCaseName': testcase_name,
        },
        'status': item['status'],
        'execution': {
            'duration': item.get('duration', 0),
        },
    }
    if item['status'] in FAILURE_STATUSES:
        for key in DETAILS_KEYS:
            if item.get(key):
                item_data['execution'][key] = item[key]
    if item.get('errorsList'):
        item_data['execution']['errorsList'] = item['errorsList']
    testcase = _merge_dicts(labels, item_data)
    try:
        if not in_scope(scope, testcase):
            return {}
    except ValueError as err:
        raise DataSourceScopeError(f'[SCOPE ERROR] {err}')
    return testcase


def _get_max_count(state: Dict[str, Any]) -> int:
    if state['reset']:
        return state['per_page'] * state['page']
    return state['per_page']


def _extract_testcases(
    testresults: List[Dict[str, Any]],
    state: Dict[str, Any],
    scope: Union[str, bool],
    events: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    testcases = {}
    items = 0
    testresults_part = testresults[state['last_notification_used'] :]
    if not testresults_part:
        return {}
    for i, testresult in enumerate(
        testresults_part,
        start=state['last_notification_used'],
    ):
        if i == state['last_notification_used']:
            last_testresult_used = state['last_testresult_used']
        else:
            last_testresult_used = 0
        execution_id = testresult['metadata']['attachment_origin'][0]
        labels = _get_testresult_labels(execution_id, events)
        if not labels:
            continue
        for j, item in enumerate(
            testresult['spec']['testResults'][last_testresult_used:],
            start=last_testresult_used,
        ):
            testcase = _make_testcase_from_testresult(item, labels, scope)
            if not testcase:
                continue
            if not match_selectors(testcase, state['fieldselector']):
                continue
            testcases[item['id']] = testcase
            items += 1
            if items > _get_max_count(state):
                state['last_notification_used'] = i
                state['last_testresult_used'] = j
                return testcases

    state['last_notification_used'] = i + 1
    state['last_testresult_used'] = 0
    return testcases


def get_testcases(
    events: List[Dict[str, Any]], scope: Union[str, bool] = True, state=None
) -> Dict[str, Dict[str, Any]]:
    """Extract metadata for each test result.

    Test results are Notification events with a `.spec.testResults`
    entry.

    # Required parameters

    - events: a list of events

    # Returned value

    A possibly empty dictionary.  Keys are the test result IDs, values
    are dictionaries with test case metadata, labels, status, and
    execution info.

    `testcases` is a dictionary of entries like:

    ```
    apiVersion: testing.opentestfactory.org/v1alpha1
    kind: TestCase
    metadata:
      name: <<<Test case full name>>>
      id: <<<Test case uuid>>>
      job_id: <<<Test case job uuid>>>
      execution_id: <<<Test case attachment origin uuid>>>
      workflow_id: <<<Test case workflow uuid>>>
      namespace: <<<Test case namespace>>>
      creationTimestamp: <<<Test case provider creation timestamp>>>
    test:
      runs-on: <<<Test case execution environment tags>>>
      uses: <<<Test case provider>>>
      technology: <<<Test case technology>>>
      managed: bool <<<True for test referential managed test cases>>>
      job: <<<Test case job name>>>
      test: <<<Test case test reference>>>
      suiteName: <<<Test case suite>>>
      testCaseName: <<<Test case short name>>>
      outcome: <<<success|failure|skipped|error>>>
    status: <<<SUCCESS|FAILURE|SKIPPED|ERROR>>>
    execution:
      startTime: <<<Test case execution start time>>>
      endTime: <<<Test case execution end time>>>
      duration: <<<Test case execution duration (from result notification)>>>
      errorsList: [<<<Test case general execution errors>>>]
      (failure|warning|error)Details: {<<<Test case failure details>>>}
    ```

    # Raised exceptions

    A _ValueError_ exception is raised if there were no test results in
    `events` or some scope errors occured retrieving test results.
    """
    if not state:
        raise ValueError('No workflow cache state received from observer.')

    if _uses_inception(events):
        testresults = _get_inception_testresults(events)
    else:
        testresults = get_testresults(events)

    if not testresults:
        return {}
    try:
        testcases = _extract_testcases(testresults, state, scope, events)
        if not testcases:
            raise DataSourceScopeError(f'No test cases matching scope `{scope}`.')
    except DataSourceScopeError:
        raise
    return testcases


########################################################################
## Datasource: Tags


def _make_tag_datasource(tag: str, parent: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'apiVersion': 'opentestfactory.org/v1alpha1',
        'kind': 'Tag',
        'metadata': {
            'name': tag,
            'workflow_id': parent['metadata']['workflow_id'],
            'namespace': parent['metadata']['namespace'],
        },
        'status': {
            'jobCount': 0,
            'testCaseCount': 0,
            'testCaseStatusSummary': {
                'success': 0,
                'failure': 0,
                'error': 0,
                'skipped': 0,
                'cancelled': 0,
            },
        },
    }


def get_tags(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract metadata for each execution environment tag.

    # Required parameters:

    - events: a list of events

    # Returned value:

    A dictionary. Keys are tags names, values are dictionaries with tag metadata and status.

    `tags` is a dictionary of entries like:

    ```
    apiVersion: opentestfactory.org/v1alpha1
    kind: Tag
    metadata:
      name: <<<Tag name>>>
      workflow_id: <<<Tag workflow id>>>
      namespace: <<<Tag namespace>>>
    status:
      jobCount: <<<Tag related jobs count>>>
      testCaseCount: <<<Tag related test cases count>>>
      testCaseStatusSummary: <<<Tag test case count by status>>>
        success: N
        failure: N
        error: N
        skipped: N
        cancelled: N
    ```
    """
    if not (jobs := _get_workflow_jobs(events)):
        raise DataSourceDataError(
            'No job events found in workflow. Cannot extract data for tags.'
        )
    tags = {}
    for job, parent in jobs.values():
        for tag in job['runs-on']:
            tags.setdefault(tag, _make_tag_datasource(tag, parent))
            tags[tag]['status']['jobCount'] += 1

    return tags


########################################################################
## Datasource: Jobs


def _collect_job_times_and_id(
    events: List[Dict[str, Any]], request_metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """Collect job start and end time, if available.

    # Required parameters

    - events: a list of events
    - request_metadata: the channel request metadata for the job

    # Returned object

    A dictionary with the following entries:

    - job_id
    - requestTime

    If the job started, it contains the additional entries:

    - startTime
    - endTime
    - duration
    """
    job_id = request_metadata['job_id']
    request_time = request_metadata[CREATION_TIMESTAMP]

    start = end = None
    for event in events:
        metadata = event['metadata']
        kind_step_id = (event['kind'], metadata['step_sequence_id'], metadata['job_id'])
        if kind_step_id == (EXECUTIONCOMMAND, 0, job_id):
            start = metadata[CREATION_TIMESTAMP]
        elif kind_step_id == (EXECUTIONRESULT, -2, job_id):
            end = metadata[CREATION_TIMESTAMP]
        if start and end:
            break
    else:
        return {'job_id': job_id, 'requestTime': request_time}

    return {
        'requestTime': request_time,
        'startTime': start,
        'endTime': end,
        'duration': (
            datetime.fromisoformat(end) - datetime.fromisoformat(start)
        ).total_seconds()
        * 1000,
        'job_id': job_id,
    }


def _make_job_datasource(
    job_name: str,
    request_metadata: Dict[str, Any],
    job: Dict[str, Any],
    parent: Dict[str, Any],
    events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Make datasource object for job.

    # Required parameters

    - job_name: a string, the 'short' job name
    - request_metadata: the channel request metadata for the job or {}
    - job: a dictionary, the job definition
    - parent: a workflow or a generatorresult event
    - events: a list of events

    # Returned value

    A 'Job' datasource object.
    """
    if request_metadata:
        job_times_id = _collect_job_times_and_id(events, request_metadata)
    else:
        job_times_id = {}

    return {
        'apiVersion': 'opentestfactory.org/v1alpha1',
        'kind': 'Job',
        'metadata': {
            'name': job_name,
            'id': job_times_id.get('job_id'),
            'namespace': parent['metadata']['namespace'],
            'workflow_id': parent['metadata']['workflow_id'],
            CREATION_TIMESTAMP: parent['metadata'].get(CREATION_TIMESTAMP),
        },
        'spec': {
            'runs-on': job['runs-on'],
            'variables': {
                **parent.get('variables', {}),
                **job.get('variables', {}),
            },
        },
        'status': {
            'phase': 'SUCCEEDED',
            'requestTime': job_times_id.get('requestTime'),
            'startTime': job_times_id.get('startTime'),
            'endTime': job_times_id.get('endTime'),
            'duration': job_times_id.get('duration'),
            'testCaseCount': 0,
            'testCaseStatusSummary': {
                'success': 0,
                'failure': 0,
                'error': 0,
                'skipped': 0,
                'cancelled': 0,
            },
        },
    }


def get_jobs(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract metadata for each job.

    # Required parameters:

    - events: a list of events

    # Returned value:

    A dictionary. Keys are job names, values are dictionaries with
    job metadata, spec, and status.

    `jobs_testcases` is a dictionary of entries like:

    ```
    apiVersion: opentestfactory.org/v1alpha1
    kind: Job
    metadata:
      name: <<<Job name>>
      id: <<<Job uuid>>>
      namespace: <<<Job namespace>>>
      workflow_id: <<<Job workflow id>>>
      creationTimestamp: <<<Job creation timestamp>>>
    spec:
      runs-on: <<<Job execution environment tags>>>
      variables: <<<Workflow and job specific environment variables>>>
    status:
      phase: <<<Job phase>>>
      requestTime: <<<Job execution environment request time>>>
      startTime: <<<Job start time>>>
      endTime: <<<Job end time>>>
      duration: <<<Job duration (endTime - startTime)>>>
      testCaseCount: <<<Job test case count>>>
      testCaseStatusSummary: <<<Job test case count by status>>>
        success: N
        failure: N
        error: N
        skipped: N
        cancelled: N
    ```
    """

    def _matches(item, items):
        if item and items:
            return items[-1] == item
        return not item and not items

    if not (workflow_jobs := _get_workflow_jobs(events)):
        raise DataSourceDataError(
            'No job events found in workflow. Cannot extract data for jobs.'
        )

    jobs_events = list(
        filter(
            lambda event: event['kind'] in (EXECUTIONCOMMAND, EXECUTIONRESULT)
            and event['metadata']['step_sequence_id'] in (0, -1, -2),
            events,
        )
    )
    jobs = {}
    for job_name, (job, parent) in workflow_jobs.items():
        name, _, uuid = job_name.partition(' ')
        channel_request_metadata = next(
            (
                event
                for event in jobs_events
                if event['kind'] == EXECUTIONCOMMAND
                and event['metadata']['step_sequence_id'] == -1
                and event['metadata']['name'] == name
                and _matches(uuid, event['metadata']['job_origin'])
            ),
            {'metadata': {}},
        )['metadata']

        data = _make_job_datasource(
            name, channel_request_metadata, job, parent, jobs_events
        )
        jobs[data['metadata']['id']] = data

    return jobs
