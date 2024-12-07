# -----------------------------------------------------------------------------

import base64
from unittest.mock import Mock, patch

import pytest  # noqa: F401
import yaml
from conftest import run
from gitlab.exceptions import GitlabHttpError

from gitlabcis.benchmarks.build_pipelines_2 import pipeline_instructions_2_3

# -----------------------------------------------------------------------------


@patch('gitlabcis.utils.ci.getConfig')
def test_build_steps_as_code(mockGetConfig, glEntity, glObject):

    test = pipeline_instructions_2_3.build_steps_as_code

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


@patch('gitlabcis.utils.ci.getConfig')
def test_build_stage_io(mockGetConfig, glEntity, glObject):

    test = pipeline_instructions_2_3.build_stage_io

    def setup_ci_yaml(yaml_content):
        mock_file = Mock()
        mock_file.content = base64.b64encode(
            yaml.dump(
                yaml_content
            ).encode()).decode('utf-8')
        return {mock_file: 'reason'}

    mockGetConfig.return_value = {None: 'No CI file found'}
    run(glEntity, glObject, test, None)

    mockGetConfig.return_value = setup_ci_yaml({})
    run(glEntity, glObject, test, False)

    mockGetConfig.return_value = setup_ci_yaml({'stages': ['test']})
    run(glEntity, glObject, test, False)

    mockGetConfig.return_value = setup_ci_yaml({'stages': ['build', 'test']})
    run(glEntity, glObject, test, True)

    mockGetConfig.return_value = setup_ci_yaml({
        'stages': ['build', 'test'],
        'build_job': {'stage': 'build'}
    })
    run(glEntity, glObject, test, False)

    mockGetConfig.return_value = setup_ci_yaml({
        'stages': ['build', 'test'],
        'build_job': {'stage': 'build', 'script': ['echo "Building"']}
    })
    run(glEntity, glObject, test, False)

    mockGetConfig.return_value = setup_ci_yaml({
        'stages': ['build', 'test'],
        'build_job': {
            'stage': 'build',
            'script': ['echo "Building"'],
            'artifacts': {'paths': ['build/']}
        }
    })
    run(glEntity, glObject, test, True)

    refYml = Mock()
    refYml.content = base64.b64encode(b'''
test:
  script:
    - !reference [.setup, script]
    - echo running my own command
  after_script:
    - !reference [.teardown, after_script]
''').decode('utf-8')

    mockGetConfig.return_value = {refYml: 'reason'}

    run(glEntity, glObject, test, False)

    mockGetConfig.side_effect = GitlabHttpError(response_code=403)
    run(glEntity, glObject, test, None)

    mockGetConfig.side_effect = GitlabHttpError(response_code=418)
    assert test(glEntity, glObject) is None


# -----------------------------------------------------------------------------


def test_secure_pipeline_output(glEntity, glObject):

    test = pipeline_instructions_2_3.secure_pipeline_output

    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


@patch('gitlabcis.utils.ci.getConfig')
def test_track_pipeline_files(mockGetConfig, glEntity, glObject):

    test = pipeline_instructions_2_3.track_pipeline_files

    mockGetConfig.return_value = {None: 'No CI file found'}
    run(glEntity, glObject, test, None)

    mockGetConfig.return_value = {'real-fake-file': 'i promise'}
    run(glEntity, glObject, test, True)

    mockGetConfig.side_effect = GitlabHttpError(response_code=403)
    run(glEntity, glObject, test, None)

    mockGetConfig.side_effect = GitlabHttpError(response_code=418)
    assert test(glEntity, glObject) is None

# -----------------------------------------------------------------------------


def test_limit_pipeline_triggers(glEntity, glObject):

    test = pipeline_instructions_2_3.limit_pipeline_triggers

    glEntity.protected_environments.list.return_value = []
    run(glEntity, glObject, test, False)

    glEntity.protected_environments.list.return_value = [Mock()]
    run(glEntity, glObject, test, None)

    glEntity.protected_environments.list.side_effect = GitlabHttpError(
        response_code=403)
    run(glEntity, glObject, test, None)

    glEntity.protected_environments.list.side_effect = GitlabHttpError(
        response_code=418)
    assert test(glEntity, glObject) is None

# -----------------------------------------------------------------------------


def test_pipeline_misconfiguration_scanning(glEntity, glObject, gqlClient):

    test = pipeline_instructions_2_3.pipeline_misconfiguration_scanning

    kwargs = {
        'graphQLEndpoint': 'https://example.com/graphql',
        'graphQLHeaders': {'Authorization': 'Bearer token'}
    }
    run(glEntity, glObject, test, False, **kwargs)

    glEntity.path_with_namespace = 'test/project'
    gqlClient.return_value.execute.return_value = {
        'project': {
            'scanExecutionPolicies': {
                'nodes': [
                    {
                        'enabled': True,
                        'yaml': '''
                            actions:
                              - scan: sast
                              - scan: dast
                              - scan: secret_detection
                              - scan: cluster_image_scanning
                              - scan: container_scanning
                              - scan: sast_iac
                              - scan: dependency_scanning
                            rules:
                              - type: pipeline
                                branches: ['*']
                        '''
                    }
                ]
            }
        }
    }
    run(glEntity, glObject, test, True, **kwargs)

    glEntity.path_with_namespace = 'test/project'
    gqlClient.return_value.execute.return_value = {
        'project': {
            'scanExecutionPolicies': {
                'nodes': [
                    {
                        'enabled': True,
                        'yaml': '''
                            actions:
                              - scan: sast
                              - scan: dast
                            rules:
                              - type: pipeline
                                branches: ['*']
                        '''
                    }
                ]
            }
        }
    }
    run(glEntity, glObject, test, True, **kwargs)

    glEntity.path_with_namespace = 'test/project'
    gqlClient.return_value.execute.return_value = {
        'project': {
            'scanExecutionPolicies': {
                'nodes': [
                    {
                        'enabled': True,
                        'yaml': '''
                            actions:
                              - scan: secret_detection
                            rules:
                              - type: pipeline
                                branches: ['*']
                        '''
                    }
                ]
            }
        }
    }
    run(glEntity, glObject, test, False, **kwargs)

    glEntity.path_with_namespace = 'test/project'
    gqlClient.return_value.execute.return_value = {'project': {}}
    run(glEntity, glObject, test, False, **kwargs)

# -----------------------------------------------------------------------------


def test_pipeline_vuln_scanning(glEntity, glObject, gqlClient):

    test = pipeline_instructions_2_3.pipeline_vuln_scanning

    kwargs = {
        'graphQLEndpoint': 'https://example.com/graphql',
        'graphQLHeaders': {'Authorization': 'Bearer token'}
    }
    glEntity.path_with_namespace = 'test/project'

    gqlClient.return_value.execute.return_value = {
        'project': {
            'scanExecutionPolicies': {
                'nodes': [
                    {
                        'enabled': True,
                        'yaml': '''
                        actions:
                          - scan: sast
                          - scan: dast
                          - scan: secret_detection
                          - scan: cluster_image_scanning
                          - scan: container_scanning
                          - scan: sast_iac
                          - scan: dependency_scanning
                        rules:
                          - type: pipeline
                            branches: ['*']
                        '''
                    }
                ]
            }
        }
    }
    run(glEntity, glObject, test, True, **kwargs)

    gqlClient.return_value.execute.return_value = {
        'project': {
            'scanExecutionPolicies': {
                'nodes': [
                    {
                        'enabled': True,
                        'yaml': '''
                        actions:
                          - scan: sast
                          - scan: dast
                        rules:
                          - type: pipeline
                            branches: ['*']
                        '''
                    }
                ]
            }
        }
    }
    run(glEntity, glObject, test, True, **kwargs)

    gqlClient.return_value.execute.return_value = {
        'project': {
            'scanExecutionPolicies': {
                'nodes': [
                    {
                        'enabled': True,
                        'yaml': '''
                        actions:
                          - scan: secret_detection
                        rules:
                          - type: pipeline
                            branches: ['*']
                        '''
                    }
                ]
            }
        }
    }
    run(glEntity, glObject, test, False, **kwargs)

    gqlClient.return_value.execute.return_value = {
        'project': {
            'scanExecutionPolicies': {
                'nodes': []
            }
        }
    }
    run(glEntity, glObject, test, False, **kwargs)

    gqlClient.return_value.execute.return_value = {}
    run(glEntity, glObject, test, False, **kwargs)

# -----------------------------------------------------------------------------


@patch('gitlabcis.utils.ci.searchConfig')
def test_pipeline_secret_scanning(mockSearchConfig, glEntity, glObject):

    test = pipeline_instructions_2_3.pipeline_secret_scanning

    mockSearchConfig.return_value = {True: 'Secret-Detection found'}
    run(glEntity, glObject, test, True)

    mockSearchConfig.return_value = {False: 'Secret-Detection not found'}
    run(glEntity, glObject, test, False)

    mockSearchConfig.side_effect = GitlabHttpError(response_code=401)
    run(glEntity, glObject, test, None)

    mockSearchConfig.side_effect = GitlabHttpError(response_code=418)
    assert test(glEntity, glObject) is None
