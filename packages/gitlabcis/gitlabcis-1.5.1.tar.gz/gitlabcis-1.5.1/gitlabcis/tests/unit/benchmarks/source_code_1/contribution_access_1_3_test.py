# -----------------------------------------------------------------------------

from unittest.mock import Mock

from gitlabcis.benchmarks.source_code_1 import contribution_access_1_3
from conftest import run

# -----------------------------------------------------------------------------


def test_review_and_remove_inactive_users(glEntity, glObject, unauthorised):
    from gitlab.exceptions import GitlabGetError

    from dateutil.relativedelta import relativedelta
    from datetime import datetime, timezone

    test = contribution_access_1_3.review_and_remove_inactive_users

    user = Mock()
    hundredDaysAgo = datetime.strftime(
        datetime.now(timezone.utc) - relativedelta(days=100),
        '%Y-%m-%d')
    yesterday = datetime.strftime(
        datetime.now(timezone.utc) - relativedelta(days=1),
        '%Y-%m-%d')

    unauthorised.users.list.side_effect = GitlabGetError(response_code=401)
    run(unauthorised, unauthorised, test, None)

    user.last_activity_on = None
    glObject.users.list.return_value = [user]
    run(glEntity, glObject, test, True)

    user.last_activity_on = yesterday
    glObject.users.list.return_value = [user]
    run(glEntity, glObject, test, False)

    user.last_activity_on = hundredDaysAgo
    glObject.users.list.return_value = [user]
    run(glEntity, glObject, test, True)

    del user.last_activity_on
    glObject.users.list.return_value = [user]
    run(glEntity, glObject, test, None)

# -----------------------------------------------------------------------------


def test_limit_top_level_group_creation(glEntity, glObject, unauthorised):
    from gitlab.exceptions import GitlabGetError

    test = contribution_access_1_3.limit_top_level_group_creation

    unauthorised.settings.get.side_effect = GitlabGetError(
        response_code=401)
    run(unauthorised, unauthorised, test, None)

    glObject.settings.get.return_value = Mock(can_create_group=False)
    run(glEntity, glObject, test, True)

    glObject.settings.get.return_value = Mock(can_create_group=True)
    run(glEntity, glObject, test, False)

# -------------------------------------------------------------------------


def test_minimum_number_of_admins(glEntity, glObject, unauthorised):

    from gitlab.exceptions import GitlabGetError

    test = contribution_access_1_3.minimum_number_of_admins

    unauthorised.members_all.list.side_effect = GitlabGetError(
        response_code=401)
    run(unauthorised, unauthorised, test, None)

    member = Mock(access_level=40)
    glEntity.members_all.list.return_value = [member]
    run(glEntity, glObject, test, None)

    member2 = Mock(access_level=10)
    member3 = Mock(access_level=10)
    glEntity.members_all.list.return_value = [member, member2, member3]
    run(glEntity, glObject, test, True)

    member2 = Mock(access_level=40)
    member3 = Mock(access_level=40)
    glEntity.members_all.list.return_value = [member, member2, member3]
    run(glEntity, glObject, test, False)

# -------------------------------------------------------------------------


def test_require_mfa_for_contributors(glEntity, glObject, unauthorised):

    from gitlab.exceptions import GitlabGetError

    test = contribution_access_1_3.require_mfa_for_contributors

    unauthorised.settings.get.side_effect = GitlabGetError(response_code=401)
    run(unauthorised, unauthorised, test, None)

    settings = Mock()

    settings.require_two_factor_authentication = True
    glObject.settings.get.return_value = settings
    run(glEntity, glObject, test, True)

    settings.require_two_factor_authentication = False
    glObject.settings.get.return_value = settings
    run(glEntity, glObject, test, False)

# -------------------------------------------------------------------------


def test_require_mfa_at_org_level(glEntity, glObject, unauthorised):

    from gitlab.exceptions import GitlabGetError

    test = contribution_access_1_3.require_mfa_at_org_level

    unauthorised.settings.get.side_effect = GitlabGetError(response_code=401)
    run(unauthorised, unauthorised, test, None)

    settings = Mock()

    settings.require_two_factor_authentication = True
    glObject.settings.get.return_value = settings
    run(glEntity, glObject, test, True)

    settings.require_two_factor_authentication = False
    settings.two_factor_grace_period = 1
    glObject.settings.get.return_value = settings
    run(glEntity, glObject, test, True)

    settings.require_two_factor_authentication = False
    settings.two_factor_grace_period = 0
    glObject.settings.get.return_value = settings
    run(glEntity, glObject, test, False)

# -------------------------------------------------------------------------


def test_limit_user_registration_domain(glEntity, glObject):

    test = contribution_access_1_3.limit_user_registration_domain

    run(glEntity, glObject, test, None)

# -------------------------------------------------------------------------


def test_ensure_2_admins_per_repo(glEntity, glObject, unauthorised):
    from gitlab.exceptions import GitlabGetError

    test = contribution_access_1_3.ensure_2_admins_per_repo

    unauthorised.members_all.list.side_effect = GitlabGetError(
        response_code=401)
    run(unauthorised, unauthorised, test, None)

    del unauthorised.members_all
    run(unauthorised, unauthorised, test, None)

    member = Mock(access_level=50)
    member2 = Mock(access_level=50)
    glEntity.members_all.list.return_value = [member, member2]
    run(glEntity, glObject, test, True)

    member = Mock(access_level=10)
    glEntity.members_all.list.return_value = [member]
    run(glEntity, glObject, test, True)

    member = Mock(access_level=50)
    glEntity.members_all.list.return_value = [member]
    run(glEntity, glObject, test, True)

# -------------------------------------------------------------------------


def test_strict_permissions_for_repo(glEntity, glObject, unauthorised):
    from gitlab.exceptions import GitlabGetError

    test = contribution_access_1_3.strict_permissions_for_repo

    unauthorised.members_all.list.side_effect = GitlabGetError(
        response_code=401)
    run(unauthorised, unauthorised, test, None)

    member = Mock(access_level=40)
    glEntity.members_all.list.return_value = [member]
    run(glEntity, glObject, test, None)

    member = Mock(access_level=40)
    member2 = Mock(access_level=10)
    member3 = Mock(access_level=10)
    glEntity.members_all.list.return_value = [member, member2, member3]
    run(glEntity, glObject, test, True)

    member = Mock(access_level=40)
    member2 = Mock(access_level=40)
    glEntity.members_all.list.return_value = [member, member2]
    run(glEntity, glObject, test, False)

# -------------------------------------------------------------------------


def test_domain_verification(glEntity, glObject):

    test = contribution_access_1_3.domain_verification

    run(glEntity, glObject, test, None)

# -------------------------------------------------------------------------


def test_scm_notification_restriction(glEntity, glObject):

    test = contribution_access_1_3.scm_notification_restriction

    run(glEntity, glObject, test, None)

# -------------------------------------------------------------------------


def test_org_provided_ssh_certs(glEntity, glObject, unauthorised):

    from gitlab.exceptions import GitlabGetError

    test = contribution_access_1_3.org_provided_ssh_certs

    unauthorised.settings.get.side_effect = GitlabGetError(response_code=401)
    run(unauthorised, unauthorised, test, None)

    settings = Mock()
    settings.ed25519_key_restriction = 1
    glObject.settings.get.return_value = settings
    run(glEntity, glObject, test, True)

    settings.ed25519_key_restriction = 0
    settings.ecdsa_key_restriction = 0
    settings.dsa_key_restriction = 0
    settings.rsa_key_restriction = 0
    settings.ecdsa_sk_key_restriction = 0
    settings.ed25519_sk_key_restriction = 0
    glObject.settings.get.return_value = settings
    run(glEntity, glObject, test, False)

# -------------------------------------------------------------------------


def test_restrict_ip_addresses(glEntity, glObject):

    test = contribution_access_1_3.restrict_ip_addresses

    run(glEntity, glObject, test, None)

# -------------------------------------------------------------------------


def test_track_code_anomalies(glEntity, glObject):

    test = contribution_access_1_3.track_code_anomalies

    run(glEntity, glObject, test, None)
