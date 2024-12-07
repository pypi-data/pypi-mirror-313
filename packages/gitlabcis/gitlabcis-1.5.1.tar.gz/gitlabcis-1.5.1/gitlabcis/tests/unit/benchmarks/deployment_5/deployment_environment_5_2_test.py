# -----------------------------------------------------------------------------

from unittest.mock import Mock, patch

import pytest  # noqa: F401
from conftest import run
from gitlab.exceptions import GitlabHttpError

from gitlabcis.benchmarks.deployment_5 import deployment_environment_5_2

# -----------------------------------------------------------------------------


@patch('gitlabcis.utils.ci.getConfig')
def test_automate_deployment(mockGetConfig, glEntity, glObject):

    test = deployment_environment_5_2.automate_deployment

    mockGetConfig.return_value = {None: 'No CI file found'}
    run(glEntity, glObject, test, None)

    mockGetConfig.return_value = {False: 'Invalid CI file'}
    run(glEntity, glObject, test, False)

    mockGetConfig.return_value = {'gitlab-ci.yml': None}
    glEntity.approvalrules.list.return_value = [Mock(approvals_required=0)]
    run(glEntity, glObject, test, None)

    mockGetConfig.side_effect = GitlabHttpError('Error', response_code=401)
    run(glEntity, glObject, test, None)

    mockGetConfig.side_effect = GitlabHttpError('Error', response_code=418)
    assert test(glEntity, glObject) is None

# -----------------------------------------------------------------------------


def test_reproducible_deployment(glEntity, glObject):

    test = deployment_environment_5_2.reproducible_deployment

    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


def test_limit_prod_access(glEntity, glObject):

    test = deployment_environment_5_2.limit_prod_access

    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


def test_disable_default_passwords(glEntity, glObject):

    test = deployment_environment_5_2.disable_default_passwords

    run(glEntity, glObject, test, None)
