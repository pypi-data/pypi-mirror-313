# -----------------------------------------------------------------------------

from unittest.mock import Mock, patch

import pytest  # noqa: F401
from conftest import run
from gitlab.exceptions import GitlabHttpError

from gitlabcis.benchmarks.build_pipelines_2 import build_worker_2_2

# -----------------------------------------------------------------------------


def test_single_use_workers(glEntity, glObject):

    test = build_worker_2_2.single_use_workers

    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


def test_pass_worker_envs_and_commands(glEntity, glObject):

    test = build_worker_2_2.pass_worker_envs_and_commands

    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


def test_segregate_worker_duties(glEntity, glObject):

    test = build_worker_2_2.segregate_worker_duties

    glEntity.runners.list.return_value = [Mock(is_shared=False)]
    run(glEntity, glObject, test, True)

    glEntity.runners.list.return_value = [Mock(is_shared=True)]
    run(glEntity, glObject, test, False)

    glEntity.runners.list.side_effect = GitlabHttpError(response_code=401)
    run(glEntity, glObject, test, None)

    glEntity.runners.list.side_effect = GitlabHttpError(response_code=418)
    assert test(glEntity, glObject) is None

# -----------------------------------------------------------------------------


def test_restrict_worker_connectivity(glEntity, glObject):

    test = build_worker_2_2.restrict_worker_connectivity

    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


def test_worker_runtime_security(glEntity, glObject):

    test = build_worker_2_2.worker_runtime_security

    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


def test_build_worker_vuln_scanning(glEntity, glObject):

    test = build_worker_2_2.build_worker_vuln_scanning

    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


@patch('gitlabcis.utils.ci.getConfig')
def test_store_worker_config(mockGetConfig, glEntity, glObject):

    test = build_worker_2_2.store_worker_config

    mockGetConfig.return_value = {'gitlab-ci.yml': 'content'}
    run(glEntity, glObject, test, True)

    mockGetConfig.return_value = {None: 'No CI file found'}
    run(glEntity, glObject, test, None)

    mockGetConfig.return_value = {False: 'Invalid CI file'}
    run(glEntity, glObject, test, False)

    mockGetConfig.side_effect = GitlabHttpError('Error', response_code=401)
    run(glEntity, glObject, test, None)

    mockGetConfig.side_effect = GitlabHttpError('Error', response_code=418)
    assert test(glEntity, glObject) is None

# -----------------------------------------------------------------------------


def test_monitor_worker_resource_consumption(glEntity, glObject):

    test = build_worker_2_2.monitor_worker_resource_consumption

    run(glEntity, glObject, test, None)
