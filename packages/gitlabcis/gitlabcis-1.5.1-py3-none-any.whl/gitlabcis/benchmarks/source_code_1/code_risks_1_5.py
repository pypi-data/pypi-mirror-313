# -------------------------------------------------------------------------

def enable_secret_detection(glEntity, glObject, **kwargs):
    """
    id: 1.5.1
    title: Ensure scanners are in place to identify and prevent sensitive
           data in code
    """

    from gitlab.exceptions import GitlabGetError, GitlabHttpError
    from gitlab.exceptions import GitlabAuthenticationError
    from gql import gql
    from graphql import GraphQLError
    from gql.transport.exceptions import TransportServerError
    from gql.transport.exceptions import TransportAlreadyConnected
    from gql import Client
    from gql.transport.requests import RequestsHTTPTransport

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

        if 'SECRET_DETECTION' in \
                results['project']['securityScanners']['enabled']:
            return {True: 'Secret Detection is enabled'}

        else:
            return {False: 'Secret Detection is not enabled'}

    except KeyError:
        return {False: 'Secret Detection is not enabled'}

# -------------------------------------------------------------------------


def secure_pipeline_instructions(glEntity, glObject, **kwargs):
    """
    id: 1.5.2
    title: Detect and prevent misconfigurations and insecure instructions
           in CI pipelines
    """

    return {None: 'This check requires validation'}

# -------------------------------------------------------------------------


def secure_iac_instructions(glEntity, glObject, **kwargs):
    """
    id: 1.5.3
    title: Ensure scanners are in place to secure Infrastructure as Code
           (IaC) instructions
    """

    from gitlab.exceptions import GitlabGetError, GitlabHttpError
    from gitlab.exceptions import GitlabAuthenticationError
    from gql import gql
    from graphql import GraphQLError
    from gql.transport.exceptions import TransportServerError
    from gql.transport.exceptions import TransportAlreadyConnected
    from gql import Client
    from gql.transport.requests import RequestsHTTPTransport

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

        if 'SAST' in \
                results['project']['securityScanners']['enabled']:
            return {True: 'SAST Scanning is enabled'}

        else:
            return {False: 'SAST Scanning is not enabled'}

    except KeyError:
        return {False: 'SAST Scanning is not enabled'}

# -------------------------------------------------------------------------


def vulnerability_scanning(glEntity, glObject, **kwargs):
    """
    id: 1.5.4
    title: Ensure scanners are in place for code vulnerabilities
    """

    from gitlab.exceptions import GitlabGetError, GitlabHttpError
    from gitlab.exceptions import GitlabAuthenticationError
    from gql import gql
    from graphql import GraphQLError
    from gql.transport.exceptions import TransportServerError
    from gql.transport.exceptions import TransportAlreadyConnected
    from gql import Client
    from gql.transport.requests import RequestsHTTPTransport

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

        if 'SAST' in \
                results['project']['securityScanners']['enabled']:
            return {True: 'Vulnerability Scanning is enabled'}

        else:
            return {False: 'Vulnerability Scanning is not enabled'}

    except KeyError:
        return {False: 'Vulnerability Scanning is not enabled'}

# -------------------------------------------------------------------------


def dependency_scanning(glEntity, glObject, **kwargs):
    """
    id: 1.5.5
    title: Ensure scanners are in place for open-source vulnerabilities in
           used packages
    """

    from gitlab.exceptions import GitlabGetError, GitlabHttpError
    from gitlab.exceptions import GitlabAuthenticationError
    from gql import gql
    from graphql import GraphQLError
    from gql.transport.exceptions import TransportServerError
    from gql.transport.exceptions import TransportAlreadyConnected
    from gql import Client
    from gql.transport.requests import RequestsHTTPTransport

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

        if 'DEPENDENCY_SCANNING' in \
                results['project']['securityScanners']['enabled']:
            return {True: 'Dependency Scanning is enabled'}

        else:
            return {False: 'Dependency Scanning is not enabled'}

    except KeyError:
        return {False: 'Dependency Scanning is not enabled'}

# -------------------------------------------------------------------------


def license_scanning(glEntity, glObject, **kwargs):
    """
    id: 1.5.6
    title: Ensure scanners are in place for open-source license issues in
           used packages
    """

    from gitlab.exceptions import GitlabGetError, GitlabHttpError
    from gitlab.exceptions import GitlabAuthenticationError
    from gql import gql
    from graphql import GraphQLError
    from gql.transport.exceptions import TransportServerError
    from gql.transport.exceptions import TransportAlreadyConnected
    from gql import Client
    from gql.transport.requests import RequestsHTTPTransport

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

        # License scanning is covered under dependency scanning:
        if 'DEPENDENCY_SCANNING' in \
                results['project']['securityScanners']['enabled']:
            return {True: 'License Scanning is enabled'}

        else:
            return {False: 'License Scanning is not enabled'}

    except KeyError:
        return {False: 'License Scanning is not enabled'}

# -------------------------------------------------------------------------


def dast_web_scanning(glEntity, glObject, **kwargs):
    """
    id: 1.5.7
    title: Ensure scanners are in place for web application runtime
           security weaknesses
    """

    from gitlab.exceptions import GitlabGetError, GitlabHttpError
    from gitlab.exceptions import GitlabAuthenticationError
    from gql import gql
    from graphql import GraphQLError
    from gql.transport.exceptions import TransportServerError
    from gql.transport.exceptions import TransportAlreadyConnected
    from gql import Client
    from gql.transport.requests import RequestsHTTPTransport

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

        if 'DAST' in \
                results['project']['securityScanners']['enabled']:
            return {True: 'DAST Scanning is enabled'}

        else:
            return {False: 'DAST Scanning is not enabled'}

    except KeyError:
        return {False: 'DAST Scanning is not enabled'}

# -------------------------------------------------------------------------


def dast_api_scanning(glEntity, glObject, **kwargs):
    """
    id: 1.5.8
    title: Ensure scanners are in place for API runtime security weaknesses
    """

    from gitlab.exceptions import GitlabGetError, GitlabHttpError
    from gitlab.exceptions import GitlabAuthenticationError
    from gql import gql
    from graphql import GraphQLError
    from gql.transport.exceptions import TransportServerError
    from gql.transport.exceptions import TransportAlreadyConnected
    from gql import Client
    from gql.transport.requests import RequestsHTTPTransport

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

        if 'DAST' in \
                results['project']['securityScanners']['enabled']:
            return {True: 'DAST Scanning is enabled'}

        else:
            return {False: 'DAST Scanning is not enabled'}

    except KeyError:
        return {False: 'DAST Scanning is not enabled'}
