# -----------------------------------------------------------------------------

from unittest.mock import Mock

from conftest import run

from gitlabcis.benchmarks.source_code_1 import repository_management_1_2

# -----------------------------------------------------------------------------


def test_public_repos_have_security_file(glEntity, glObject, unauthorised):

    from gitlab.exceptions import GitlabGetError

    test = repository_management_1_2.public_repos_have_security_file

    unauthorised.visibility.side_effect \
        = GitlabGetError(response_code=401)
    unauthorised.repository_tree.side_effect \
        = GitlabGetError(response_code=401)
    run(unauthorised, glObject, test, None)

    del unauthorised.visibility
    run(unauthorised, glObject, test, None)

    unauthorised.visibility = 'private'
    unauthorised.repository_tree.side_effect = (
        GitlabGetError(response_code=401))
    run(unauthorised, glObject, test, None)

    visibility = Mock()
    visibility.visibility = 'private'
    run(visibility, glObject, test, None)

    visibility = Mock()
    del visibility.visibility
    run(visibility, glObject, test, None)

    files = [
        {'name': 'security.md'}
    ]
    glEntity.repository_tree.return_value = files
    run(glEntity, glObject, test, True)

    files = [
        {'name': 'not-security.md'}
    ]
    glEntity.repository_tree.return_value = files
    run(glEntity, glObject, test, False)

# -----------------------------------------------------------------------------


def test_limit_repo_creations(glEntity, glObject, unauthorised):

    from gitlab.exceptions import GitlabGetError

    test = repository_management_1_2.limit_repo_creations

    unauthorised.settings.get.side_effect \
        = GitlabGetError(response_code=401)
    run(unauthorised, unauthorised, test, None)

    settings = Mock()
    settings.signup_enabled = False
    glObject.settings.get.return_value = settings
    run(glEntity, glObject, test, True)

    settings.signup_enabled = True
    settings.require_admin_approval_after_user_signup = True
    settings.email_confirmation_setting = 'hard'
    run(glEntity, glObject, test, True)

    settings.require_admin_approval_after_user_signup = False
    settings.email_confirmation_setting = 'no'
    run(glEntity, glObject, test, False)

# -----------------------------------------------------------------------------


def test_limit_repo_deletions(glEntity, glObject, unauthorised):

    test = repository_management_1_2.limit_repo_deletions

    run(unauthorised, unauthorised, test, None)

    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


def test_limit_issue_deletions(glEntity, glObject, unauthorised):

    test = repository_management_1_2.limit_issue_deletions

    run(unauthorised, unauthorised, test, None)

    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


def test_track_forks(glEntity, glObject):

    test = repository_management_1_2.track_forks

    glEntity.forks.list.return_value = []
    run(glEntity, glObject, test, True)

    glEntity.forks.list.return_value = ['yes']
    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


def test_track_project_visibility_status(glEntity, glObject):

    test = repository_management_1_2.track_project_visibility_status

    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


def test_review_and_archive_stale_repos(glEntity, glObject):

    from datetime import datetime, timedelta, timezone

    from dateutil.parser import isoparse
    from dateutil.relativedelta import relativedelta

    test = repository_management_1_2.review_and_archive_stale_repos

    # UTC+00:00 and UTC+01:00
    zones = [timezone.utc, timezone(timedelta(hours=1))]

    for zone in zones:

        # 3 months ago:
        glEntity.last_activity_at = str(
            isoparse(
                str(datetime.now(zone) - relativedelta(months=3))
            )
        )
        run(glEntity, glObject, test, True)

        # 7 months ago:
        glEntity.last_activity_at = str(
            isoparse(
                str(datetime.now(zone) - relativedelta(months=7))
            )
        )
        run(glEntity, glObject, test, False)
