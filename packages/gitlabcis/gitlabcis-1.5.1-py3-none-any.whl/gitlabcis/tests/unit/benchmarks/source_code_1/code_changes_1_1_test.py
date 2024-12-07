# -----------------------------------------------------------------------------

from unittest.mock import Mock

from conftest import run

from gitlabcis.benchmarks.source_code_1 import code_changes_1_1

# -----------------------------------------------------------------------------


def test_version_control(glEntity, glObject):

    test = code_changes_1_1.version_control

    run(None, glObject, test, False)
    run(glEntity, glObject, test, True)

# -----------------------------------------------------------------------------


def test_code_tracing(glEntity, glObject):
    from gitlab.exceptions import GitlabHttpError

    test = code_changes_1_1.code_tracing

    glEntity.mergerequests.list.return_value = []
    glEntity.issues.list.return_value = []
    run(glEntity, glObject, test, False)

    glEntity.mergerequests.list.return_value = []
    glEntity.issues.list.return_value = [Mock()]
    run(glEntity, glObject, test, True)

    issue = Mock()
    glEntity.mergerequests.list.return_value = [Mock(related_issues=[issue])]
    glEntity.issues.list.return_value = []
    run(glEntity, glObject, test, True)

    issue = Mock()
    glEntity.mergerequests.list.return_value = [Mock(related_issues=[])]
    glEntity.issues.list.return_value = []
    run(glEntity, glObject, test, False)

    glEntity.mergerequests.list.side_effect = GitlabHttpError(
        response_code=401)
    run(glEntity, glObject, test, None)

    glEntity.mergerequests.list.side_effect = GitlabHttpError(
        'Error', response_code=418)
    assert test(glEntity, glObject) is None

# -----------------------------------------------------------------------------


def test_code_approvals(glEntity, glObject):
    from gitlab.exceptions import GitlabHttpError

    test = code_changes_1_1.code_approvals

    approvalRule = Mock()
    approvalRule.approvals_required = 2
    glEntity.approvalrules.list.return_value = [approvalRule]
    run(glEntity, glObject, test, True)

    approvalRule.approvals_required = 1
    glEntity.approvalrules.list.return_value = [approvalRule]
    run(glEntity, glObject, test, False)

    glEntity.approvalrules.list.side_effect = GitlabHttpError(
        response_code=401)
    run(glEntity, glObject, test, None)

    glEntity.approvalrules.list.side_effect = GitlabHttpError(
        'Error', response_code=418)
    assert test(glEntity, glObject) is None

# -----------------------------------------------------------------------------


def test_code_approval_dismissals(glEntity, glObject):
    from gitlab.exceptions import GitlabHttpError

    test = code_changes_1_1.code_approval_dismissals

    mrApprovalSettings = Mock()
    mrApprovalSettings.reset_approvals_on_push = True
    glEntity.approvals.get.return_value = mrApprovalSettings
    run(glEntity, glObject, test, True)

    mrApprovalSettings.reset_approvals_on_push = False
    glEntity.approvals.get.return_value = mrApprovalSettings
    run(glEntity, glObject, test, False)

    glEntity.approvals.get.side_effect = GitlabHttpError(
        response_code=401)
    run(glEntity, glObject, test, None)

    glEntity.approvals.get.side_effect = GitlabHttpError(
        'Error', response_code=418)
    assert test(glEntity, glObject) is None

# -----------------------------------------------------------------------------


def test_code_dismissal_restrictions(glEntity, glObject):
    from gitlab.exceptions import GitlabHttpError

    test = code_changes_1_1.code_dismissal_restrictions

    protectedBranches = Mock()

    branch = Mock()
    branch.merge_access_levels = [
        {"access_level_description": "Maintainers"},
        {"access_level_description": "Developers"}
    ]
    branch.push_access_levels = [
        {"access_level_description": "Maintainers"}
    ]

    protectedBranches.list.return_value = [branch]
    glEntity.protectedbranches = protectedBranches
    run(glEntity, glObject, test, True)

    branch.merge_access_levels = [
        {"access_level_description": "Maintainers"},
        # {"access_level_description": "Developers"}
    ]
    branch.push_access_levels = [
        {"access_level_description": "Maintainers"}
    ]

    protectedBranches.list.return_value = [branch]
    glEntity.protectedbranches = protectedBranches
    run(glEntity, glObject, test, False)

    branch.merge_access_levels = []
    branch.push_access_levels = []

    protectedBranches.list.return_value = [branch]
    glEntity.protectedbranches = protectedBranches
    run(glEntity, glObject, test, False)

    protectedBranches.list.return_value = []
    glEntity.protectedbranches.list.side_effect = GitlabHttpError(
        response_code=401)
    run(glEntity, glObject, test, None)

    glEntity.protectedbranches.list.side_effect = GitlabHttpError(
        'Error', response_code=418)
    assert test(glEntity, glObject) is None

# -----------------------------------------------------------------------------


def test_code_owners(glEntity, glObject):
    from gitlab.exceptions import GitlabGetError, GitlabHttpError

    test = code_changes_1_1.code_owners

    _files = Mock()
    _files = [{
        'name': 'CODEOWNERS'
    }]
    glEntity.repository_tree.return_value = _files
    run(glEntity, glObject, test, True)

    _files = [{
        'name': 'notfound'
    }]
    glEntity.repository_tree.return_value = _files
    run(glEntity, glObject, test, False)

    glEntity.repository_tree.side_effect = GitlabHttpError(
        response_code=401)
    run(glEntity, glObject, test, None)

    glEntity.repository_tree.side_effect = GitlabGetError(
        response_code=404)
    run(glEntity, glObject, test, False)

    glEntity.repository_tree.side_effect = GitlabGetError(
        response_code=418)
    run(glEntity, glObject, test, None)

    glEntity.repository_tree.side_effect = GitlabHttpError(
        'Error', response_code=418)
    assert test(glEntity, glObject) == {None: 'Unknown error'}

# -----------------------------------------------------------------------------


def test_code_changes_require_code_owners(glEntity, glObject):
    from gitlab.exceptions import GitlabHttpError

    test = code_changes_1_1.code_changes_require_code_owners

    defaultBranch = Mock()
    defaultBranch.code_owner_approval_required = True
    glEntity.default_branch = defaultBranch
    glEntity.protectedbranches.get.return_value = defaultBranch
    run(glEntity, glObject, test, True)

    glEntity.protectedbranches.get.return_value = None
    run(glEntity, glObject, test, False)

    defaultBranch.code_owner_approval_required = False
    glEntity.default_branch = defaultBranch
    glEntity.protectedbranches.get.return_value = defaultBranch
    run(glEntity, glObject, test, False)

    glEntity.protectedbranches.get.side_effect = GitlabHttpError(
        response_code=403, error_message='403 Forbidden')
    run(glEntity, glObject, test, None)

    glEntity.protectedbranches.get.side_effect = GitlabHttpError(
        response_code=404)
    run(glEntity, glObject, test, False)

    glEntity.protectedbranches.get.side_effect = GitlabHttpError(
        'Error', response_code=418)
    assert test(glEntity, glObject) is None

# -----------------------------------------------------------------------------


def test_stale_branch_reviews(glEntity, glObject):
    from datetime import datetime, timezone

    from dateutil.relativedelta import relativedelta
    from gitlab.exceptions import GitlabHttpError

    test = code_changes_1_1.stale_branch_reviews

    branch = Mock()
    now = datetime.now(timezone.utc)
    nowts = f"{now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')}"
    branch.commit = {"committed_date": nowts}
    branch.name = 'not-stale'
    glEntity.branches.list.return_value = [branch]
    run(glEntity, glObject, test, True)

    thendt = now - relativedelta(months=5)
    branch.commit = {
        'committed_date': thendt.strftime('%Y-%m-%dT%H:%M:%S.%f%z')}
    branch.name = 'stale'
    glEntity.branches.list.return_value = [branch]
    run(glEntity, glObject, test, False)

    glEntity.branches.list.side_effect = GitlabHttpError(
        response_code=401)
    run(glEntity, glObject, test, None)

    glEntity.branches.list.side_effect = GitlabHttpError(
        'Error', response_code=418)
    assert test(glEntity, glObject) is None

# -----------------------------------------------------------------------------


def test_checks_pass_before_merging(glEntity, glObject):
    # from gitlab.exceptions import GitlabGetError

    test = code_changes_1_1.checks_pass_before_merging

    glEntity.only_allow_merge_if_all_status_checks_passed = True
    run(glEntity, glObject, test, True)

    glEntity.only_allow_merge_if_all_status_checks_passed = False
    run(glEntity, glObject, test, False)

# -----------------------------------------------------------------------------


def test_branches_updated_before_merging(glEntity, glObject):
    # from gitlab.exceptions import GitlabGetError

    test = code_changes_1_1.branches_updated_before_merging

    # unauthorised.merge_method.side_effect = GitlabGetError(response_code=401)
    # run(unauthorised, glObject, test, None)

    del glEntity.merge_method
    run(glEntity, glObject, test, None)

    glEntity.merge_method = 'ff'
    run(glEntity, glObject, test, True)

    glEntity.merge_method = 'no'
    run(glEntity, glObject, test, False)

# -----------------------------------------------------------------------------


def test_comments_resolved_before_merging(glEntity, glObject):

    test = code_changes_1_1.comments_resolved_before_merging

    del glEntity.only_allow_merge_if_all_discussions_are_resolved
    run(glEntity, glObject, test, None)

    glEntity.only_allow_merge_if_all_discussions_are_resolved = True
    run(glEntity, glObject, test, True)

    glEntity.only_allow_merge_if_all_discussions_are_resolved = False
    run(glEntity, glObject, test, False)

# -----------------------------------------------------------------------------


def test_commits_must_be_signed_before_merging(glEntity, glObject):

    test = code_changes_1_1.commits_must_be_signed_before_merging

    push = Mock()
    push.reject_unsigned_commits = True
    glEntity.pushrules.get.return_value = push
    run(glEntity, glObject, test, True)

    push.reject_unsigned_commits = False
    glEntity.pushrules.get.return_value = push
    run(glEntity, glObject, test, False)

# -----------------------------------------------------------------------------


def test_linear_history_required(glEntity, glObject):
    from gitlab.exceptions import GitlabGetError

    test = code_changes_1_1.linear_history_required

    glEntity.merge_method = 'dont-merge'
    run(glEntity, glObject, test, True)

    glEntity.merge_method = 'merge'
    run(glEntity, glObject, test, False)

    mergeFail = Mock()
    del mergeFail.merge_method
    mergeFail.side_effect = GitlabGetError(
        response_code=401)
    run(mergeFail, glObject, test, None)

    mergeNone = Mock()
    del mergeNone.merge_method
    mergeNone.side_effect = AttributeError()
    run(mergeNone, glObject, test, None)

# -----------------------------------------------------------------------------


def test_branch_protections_for_admins(glEntity, glObject, unauthorised):
    from gitlab.exceptions import GitlabGetError

    test = code_changes_1_1.branch_protections_for_admins

    settings = Mock()
    settings.group_owners_can_manage_default_branch_protection = False
    glObject.settings.get.return_value = settings
    run(glEntity, glObject, test, True)

    settings.group_owners_can_manage_default_branch_protection = True
    glObject.settings.get.return_value = settings
    run(glEntity, glObject, test, False)

    unauthorised.group_owners_can_manage_default_branch_protection.side_effect\
        = GitlabGetError(response_code=401)
    unauthorised.settings.get.side_effect = GitlabGetError(response_code=401)
    run(glEntity, unauthorised, test, None)

    unauthorised.group_owners_can_manage_default_branch_protection.side_effect\
        = GitlabGetError(response_code=418)
    unauthorised.settings.get.side_effect = GitlabGetError(response_code=418)
    assert test(glEntity, unauthorised) is None

# -----------------------------------------------------------------------------


def test_merging_restrictions(glEntity, glObject, unauthorised):
    from gitlab.exceptions import GitlabGetError

    test = code_changes_1_1.merging_restrictions

    glEntity.protectedbranches.list.return_value = []
    run(glEntity, glObject, test, False)

    branch = Mock()
    branch.allow_force_push = True
    protectedBranches = [branch]
    glEntity.protectedbranches.list.return_value = protectedBranches
    run(glEntity, glObject, test, False)

    branch.allow_force_push = False
    protectedBranches = [branch]
    glEntity.protectedbranches.list.return_value = protectedBranches
    run(glEntity, glObject, test, True)

    unauthorised.protectedbranches.list.side_effect \
        = GitlabGetError(response_code=401)
    run(unauthorised, glObject, test, None)

# -----------------------------------------------------------------------------


def test_ensure_force_push_is_denied(glEntity, glObject, unauthorised):
    from gitlab.exceptions import GitlabGetError

    test = code_changes_1_1.ensure_force_push_is_denied

    glEntity.protectedbranches.get.return_value = None
    run(glEntity, glObject, test, False)

    branch = Mock()
    branch.allow_force_push = False
    glEntity.protectedbranches.get.return_value = branch
    run(glEntity, glObject, test, True)

    branch.side_effect = GitlabGetError(response_code=401)
    glEntity.protectedbranches.get.return_value = branch
    unauthorised.protectedbranches.get.side_effect \
        = GitlabGetError(response_code=401)
    run(unauthorised, glObject, test, None)

# -----------------------------------------------------------------------------


def test_deny_branch_deletions(glEntity, glObject, unauthorised):
    from gitlab.exceptions import GitlabGetError

    test = code_changes_1_1.deny_branch_deletions

    glEntity.protectedbranches.list.return_value = []
    run(glEntity, glObject, test, False)

    glEntity.protectedbranches.list.return_value = ['main']
    run(glEntity, glObject, test, True)

    unauthorised.protectedbranches.list.side_effect \
        = GitlabGetError(response_code=401)
    run(unauthorised, glObject, test, None)

# -----------------------------------------------------------------------------


def test_auto_risk_scan_merges(glEntity, glObject, gqlClient):

    from gql.transport.exceptions import TransportServerError

    glEntity.path_with_namespace = 'test/project'

    kwargs = {
        'graphQLEndpoint': 'https://gitlab.com/api/graphql',
        'graphQLHeaders': {'Authorization': 'Bearer token'}
    }

    test = code_changes_1_1.auto_risk_scan_merges

    gqlClient.return_value.execute.return_value = {'project': {}}
    run(glEntity, glObject, test, False, **kwargs)

    mock_result = {
        'project': {
            'scanExecutionPolicies': {
                'nodes': [
                    {
                        'enabled': True,
                        'yaml': '''
                            actions:
                              - scan: secret_detection
                              - scan: dast
                              - scan: cluster_image_scanning
                              - scan: container_scanning
                              - scan: sast
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
    gqlClient.return_value.execute.return_value = mock_result
    run(glEntity, glObject, test, True, **kwargs)

    mock_result = {
        'project': {
            'scanExecutionPolicies': {
                'nodes': [
                    {
                        'enabled': True,
                        'yaml': '''
                            actions:
                              - scan: secret_detection
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

    gqlClient.return_value.execute.return_value = mock_result
    run(glEntity, glObject, test, True, **kwargs)

    mock_result = {
        'project': {
            'scanExecutionPolicies': {
                'nodes': [
                    {
                        'enabled': True,
                        'yaml': '''
                            actions:
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
    gqlClient.return_value.execute.return_value = mock_result
    run(glEntity, glObject, test, False, **kwargs)

    gqlClient.return_value.execute.side_effect = \
        TransportServerError("Error")
    run(glEntity, glObject, test, None, **kwargs)

# -----------------------------------------------------------------------------


def test_audit_branch_protections(glEntity, glObject, unauthorised):
    from gitlab.exceptions import GitlabAuthenticationError, GitlabGetError

    test = code_changes_1_1.audit_branch_protections

    unauthorised.get_license.side_effect = GitlabGetError(
        response_code=403, error_message='403 Forbidden')
    run(glEntity, unauthorised, test, None)

    glObject.get_license.return_value = {'plan': 'premium'}
    run(glEntity, glObject, test, True)

    glObject.get_license.return_value = {'plan': 'free'}
    run(glEntity, glObject, test, False)

    unauthorised.get_license.side_effect = GitlabAuthenticationError()
    run(glEntity, unauthorised, test, None)

# -----------------------------------------------------------------------------


def test_default_branch_protected(glEntity, glObject, unauthorised):
    from gitlab.exceptions import GitlabGetError

    test = code_changes_1_1.default_branch_protected

    branch = Mock()
    branch.protected = False
    glEntity.branches.get.return_value = branch
    run(glEntity, glObject, test, False)

    branch.protected = True
    glEntity.branches.get.return_value = branch
    run(glEntity, glObject, test, True)

    unauthorised.branches.get.side_effect \
        = GitlabGetError(response_code=401)
    run(unauthorised, glObject, test, None)
