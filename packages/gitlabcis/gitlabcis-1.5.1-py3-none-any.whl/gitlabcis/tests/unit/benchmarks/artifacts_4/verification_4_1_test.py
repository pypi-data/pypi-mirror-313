# -----------------------------------------------------------------------------

from unittest.mock import Mock, patch

import pytest  # noqa: F401
from conftest import run

from gitlabcis.benchmarks.artifacts_4 import verification_4_1

# -----------------------------------------------------------------------------


@patch('zipfile.ZipFile')
def test_sign_artifacts_in_build_pipeline(mock_zipfile, glEntity, glObject):

    from gitlab.exceptions import GitlabHttpError
    test = verification_4_1.sign_artifacts_in_build_pipeline

    glEntity.pipelines.list.return_value = []
    run(glEntity, glObject, test, False)

    mockPipeline = Mock()
    mockJob = Mock()
    mockJob.stage = 'test'
    mockPipeline.jobs.list.return_value = [mockJob]
    glEntity.pipelines.list.return_value = [mockPipeline]
    run(glEntity, glObject, test, False)

    mockJob.stage = 'build'
    mockJob.id = 1
    mockPipeline.jobs.list.return_value = [mockJob]
    glEntity.pipelines.list.return_value = [mockPipeline]
    glEntity.jobs.get.return_value.artifacts.return_value = b'fake_artifact'

    mock_zipfile.return_value.__enter__.return_value.namelist.return_value \
        = ['file1.txt', 'file2.txt']

    run(glEntity, glObject, test, False)

    mockPipeline = Mock()
    mockJob = Mock()
    mockJob.stage = 'build'
    mockJob.id = 1
    mockPipeline.jobs.list.return_value = [mockJob]
    glEntity.pipelines.list.return_value = [mockPipeline]
    glEntity.jobs.get.return_value.artifacts.return_value = b'fake_artifact'

    mock_zipfile.return_value.__enter__.return_value.namelist.return_value \
        = ['file1.txt', 'file1.sig', 'file2.txt', 'file2.sig']

    run(glEntity, glObject, test, True)

    glEntity.pipelines.list.side_effect \
        = GitlabHttpError('', response_code=403)

    run(glEntity, glObject, test, None)

    glEntity.pipelines.list.side_effect = GitlabHttpError(response_code=418)
    assert test(glEntity, glObject) is None  # noqa: E501


# -----------------------------------------------------------------------------


def test_encrypt_artifacts_before_distribution(glEntity, glObject):

    test = verification_4_1.encrypt_artifacts_before_distribution

    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


def test_only_authorized_platforms_can_decrypt_artifacts(glEntity, glObject):

    test = verification_4_1.only_authorized_platforms_can_decrypt_artifacts

    run(glEntity, glObject, test, None)
