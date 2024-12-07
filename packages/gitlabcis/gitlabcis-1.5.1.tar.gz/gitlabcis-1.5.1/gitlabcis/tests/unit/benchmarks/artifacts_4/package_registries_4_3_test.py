# -----------------------------------------------------------------------------

from unittest.mock import Mock

import pytest  # noqa: F401
from conftest import run
from gitlab.exceptions import GitlabHttpError

from gitlabcis.benchmarks.artifacts_4 import package_registries_4_3

# -----------------------------------------------------------------------------


def test_validate_signed_artifacts_on_upload(glEntity, glObject):

    test = package_registries_4_3.validate_signed_artifacts_on_upload

    glEntity.commits.list.return_value = [Mock(id='1'), Mock(id='2')]

    glEntity.commits.get.return_value = Mock(status='verified')
    run(glEntity, glObject, test, True)

    glEntity.commits.get.return_value = Mock(status=None)
    run(glEntity, glObject, test, False)

    glEntity.commits.get.side_effect = [
        Mock(status='verified'), Mock(status='unverified')]
    run(glEntity, glObject, test, False)

    glEntity.commits.list.side_effect = GitlabHttpError(response_code=403)
    run(glEntity, glObject, test, None)

    glEntity.commits.list.side_effect = GitlabHttpError(response_code=418)
    assert test(glEntity, glObject) is None

# -----------------------------------------------------------------------------


def test_all_artifact_versions_signed(glEntity, glObject):

    test = package_registries_4_3.all_artifact_versions_signed

    glEntity.commits.list.return_value = [Mock(id='1'), Mock(id='2')]

    glEntity.commits.get.return_value = Mock(status=None)
    run(glEntity, glObject, test, False)

    glEntity.commits.get.return_value = Mock(status='verified')
    run(glEntity, glObject, test, True)

    glEntity.commits.get.return_value = Mock(status='unverified')
    run(glEntity, glObject, test, False)

    glEntity.commits.list.side_effect = GitlabHttpError(response_code=403)
    run(glEntity, glObject, test, None)

    glEntity.commits.list.side_effect = GitlabHttpError(response_code=418)
    assert test(glEntity, glObject) is None

# -----------------------------------------------------------------------------


def test_audit_package_registry_config(glEntity, glObject):

    test = package_registries_4_3.audit_package_registry_config

    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


def test_secure_repo_webhooks(glEntity, glObject):

    test = package_registries_4_3.secure_repo_webhooks

    secHookSSLVerify = Mock(url='https://example.com',
                            enable_ssl_verification=True)
    secHookNoSSLVerify = Mock(url='https://example.com',
                              enable_ssl_verification=False)
    unsecureHook = Mock(url='http://example.com',
                        enable_ssl_verification=False)

    glEntity.hooks.list.return_value = []
    run(glEntity, glObject, test, True)

    glEntity.hooks.list.return_value = [
         secHookSSLVerify]
    run(glEntity, glObject, test, True)

    glEntity.hooks.list.return_value = [
         secHookNoSSLVerify]
    run(glEntity, glObject, test, False)

    glEntity.hooks.list.return_value = [
         unsecureHook]
    run(glEntity, glObject, test, False)

    glEntity.hooks.list.side_effect = GitlabHttpError(response_code=403)
    run(glEntity, glObject, test, None)

    glEntity.hooks.list.side_effect = GitlabHttpError(response_code=418)
    assert test(glEntity, glObject) is None
