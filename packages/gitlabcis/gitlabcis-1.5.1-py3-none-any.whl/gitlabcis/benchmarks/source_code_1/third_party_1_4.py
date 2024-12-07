# -------------------------------------------------------------------------


def admin_approval_for_app_installs(glEntity, glObject, **kwargs):
    """
    id: 1.4.1
    title: Ensure administrator approval is required for every installed
           application
    """

    return {True: 'You are compliant by default. Only maintainers and '
                  'owners can integrate with external applications'}

# -------------------------------------------------------------------------


def stale_app_reviews(glEntity, glObject, **kwargs):
    """
    id: 1.4.2
    title: Ensure stale applications are reviewed and inactive ones are
           removed
    """

    from gitlab.exceptions import (GitlabAuthenticationError, GitlabGetError,
                                   GitlabHttpError)
    from gql import Client, gql
    from gql.transport.exceptions import (TransportAlreadyConnected,
                                          TransportServerError)
    from gql.transport.requests import RequestsHTTPTransport
    from graphql import GraphQLError

    try:

        variables = {
            'fullPath': glEntity.path_with_namespace
        }

    except (GitlabHttpError, GitlabGetError, GitlabAuthenticationError) as e:
        if e.response_code in [401, 403]:
            return {None: 'Insufficient permissions'}

    client = Client(
        transport=RequestsHTTPTransport(
            url=kwargs.get('graphQLEndpoint'),
            headers=kwargs.get('graphQLHeaders'),
            use_json=True
        ),
        fetch_schema_from_transport=True
    )

    query = gql('''
    query GetSecurityScanners($fullPath: ID!) {
        project(fullPath: $fullPath) {
            securityScanners {
                enabled
            }
        }
    }
    ''')

    try:

        results = client.execute(query, variable_values=variables)

    except (GraphQLError, TransportServerError, TransportAlreadyConnected):
        return {None: 'Error: Issue with GraphQL Query'}

    # pytest no auth:
    except AttributeError:
        return {None: 'Insufficient permissions'}

    try:
        # dependency scanning alerts when there are stale applications present:
        if 'DEPENDENCY_SCANNING' in \
                results['project']['securityScanners']['enabled']:
            return {True: 'Dependency Scanning is enabled'}

        else:
            return {False: 'Dependency Scanning is not enabled'}

    except KeyError:
        return {False: 'Dependency Scanning is not enabled'}

# -------------------------------------------------------------------------


def least_privilge_app_permissions(glEntity, glObject, **kwargs):
    """
    id: 1.4.3
    title: Ensure the access granted to each installed application is
           limited to the least privilege needed
    """

    from gitlab.exceptions import (GitlabAuthenticationError, GitlabGetError,
                                   GitlabHttpError, GitlabListError)

    try:
        integrations = glEntity.integrations.list(get_all=False)

        if len(integrations) == 0:
            return {True: 'No integrations found'}

        return {None: 'This check requires validation'}

    except (GitlabHttpError, GitlabGetError, GitlabAuthenticationError,
            GitlabListError) as e:
        if e.response_code in [401, 403]:
            return {None: 'Insufficient permissions'}

# -------------------------------------------------------------------------


def secure_webhooks(glEntity, glObject, **kwargs):
    """
    id: 1.4.4
    title: Ensure only secured webhooks are used
    """

    from gitlab.exceptions import (GitlabAuthenticationError, GitlabGetError,
                                   GitlabHttpError, GitlabListError)

    try:
        webhooks = glEntity.hooks.list(get_all=True)

        if len(webhooks) == 0:
            return {None: 'No webhooks found'}

        for hook in webhooks:

            if hook.enable_ssl_verification is False or \
                    hook.url.startswith('http://'):
                return {False: 'Insecure webhook found'}

        return {True: 'All webhooks using HTTPS'}

    except (GitlabHttpError, GitlabGetError, GitlabAuthenticationError,
            GitlabListError) as e:
        if e.response_code in [401, 403]:
            return {None: 'Insufficient permissions'}
