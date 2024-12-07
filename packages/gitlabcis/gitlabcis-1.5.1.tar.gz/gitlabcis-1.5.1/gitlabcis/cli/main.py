# -----------------------------------------------------------------------------

import logging
from argparse import ArgumentParser, FileType
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from os import environ
from sys import exit
from urllib.parse import urlparse

import gitlab
from tqdm import tqdm

from gitlabcis import (__version__, benchmarks, countRecommendations,
                       mapRecommendations, readRecommendations)
from gitlabcis.cli import log, output

# -----------------------------------------------------------------------------
# Load project & group benchmark functions:
# -----------------------------------------------------------------------------

# load all of the compliance check functions:

benchmarkFunctions = [
    getattr(getattr(getattr(benchmarks, catFile), subCatFile), func)
    for catFile in dir(benchmarks)
    if not catFile.startswith('__')
    for subCatFile in dir(getattr(benchmarks, catFile))
    if not subCatFile.startswith('__')
    for func in dir(getattr(getattr(benchmarks, catFile), subCatFile))
    if not func.startswith('__')
]

# -----------------------------------------------------------------------------

PROFILES = [1, 2]
IMPLEMENTATION_GROUPS = ['IG1', 'IG2', 'IG3']
OUTPUT_FORMATS = ['terminal', 'yaml', 'json', 'csv', 'xml', 'txt']
MAX_WORKERS = 15

# -----------------------------------------------------------------------------
# Main:
# -----------------------------------------------------------------------------


def main():

    # -------------------------------------------------------------------------
    # Obtain Input:
    # -------------------------------------------------------------------------

    parser = ArgumentParser(
        description=f'GitLab CIS Benchmark Scanner Version: {__version__}\n'
    )

    # Add arguments
    parser.add_argument(
        'url',
        metavar='URL',
        nargs='*',
        type=str,
        help='The URL to the project to audit'
    )

    parser.add_argument(
        '-t',
        '--token',
        dest='token',
        metavar='TOKEN',
        type=str,
        help='GitLab Personal Access Token'
    )

    parser.add_argument(
        '-ot',
        '--oauth-token',
        dest='oauth_token',
        metavar='OAUTH_TOKEN',
        type=str,
        help='GitLab OAUTH Token'
    )

    parser.add_argument(
        '-ci',
        '--cis-controls',
        dest='cis_controls',
        metavar='CIS_CONTROL_IDS',
        nargs='*',
        type=float,
        help='The IDs of the CIS Controls to audit (e.g. 18.1)'
    )

    parser.add_argument(
        '-ids',
        '--recommendation-ids',
        dest='recommendation_ids',
        metavar='RECOMMENDATION_IDS',
        nargs='*',
        type=str,
        help='The IDs of the recommedation controls to audit (e.g. 1.1.1)'
    )

    parser.add_argument(
        '-s',
        '--skip',
        dest='skip_recommendation_ids',
        metavar='RECOMMENDATION_IDS_TO_SKIP',
        nargs='*',
        type=str,
        help='The IDs of the recommedation controls to SKIP (e.g. 1.1.1)'
    )

    parser.add_argument(
        '-p',
        '--profile',
        dest='profile',
        metavar='PROFILE',
        type=int,
        choices=PROFILES,
        help='Which benchmark profile to use (default: both 1 & 2)'
    )

    parser.add_argument(
        '-r',
        '--remediations',
        dest='remediations',
        action='store_true',
        help='Include remediations in the results output'
    )

    parser.add_argument(
        '-o',
        '--output',
        dest='output_file',
        metavar='OUTPUT_FILE',
        type=FileType('w', encoding='utf-8'),
        help='The name of the file to output results to'
    )

    parser.add_argument(
        '-g',
        '--implementation-groups',
        dest='implementation_groups',
        metavar='IMPLEMENTATION_GROUPS',
        nargs='*',
        type=str,
        choices=IMPLEMENTATION_GROUPS,
        help=f'Which CIS Implementation Group to use {IMPLEMENTATION_GROUPS} '
             '(default: all)'
    )

    parser.add_argument(
        '-os',
        '--omit-skipped',
        dest='omit_skipped',
        action='store_true',
        help='Excludes SKIP results from the output'
    )

    parser.add_argument(
        '-f',
        '--format',
        dest='output_format',
        default='terminal',
        type=str,
        choices=OUTPUT_FORMATS,
        help='Output format (default: terminal)'
    )

    parser.add_argument(
        '-mw',
        '--max-workers',
        dest='max_workers',
        default=15,
        type=int,
        help='Maximum number of Worker threads (default: 15)'
    )

    parser.add_argument(
        '-d',
        '--debug',
        dest='debug',
        action='store_true',
        help='Enable debugging mode'
    )

    parser.add_argument(
        '-v',
        '--version',
        dest='version',
        action='store_true',
        help='Print the currently installed version of gitlabcis'
    )

    # Parse arguments
    args = parser.parse_args()

    if args.version:
        print(f'GitLabCIS {__version__}')
        exit(0)

    if not args.url:
        parser.print_usage()
        exit(2)

    # -------------------------------------------------------------------------
    # bools to determine what entity to run checks against:
    # -------------------------------------------------------------------------

    isProject = False
    isGroup = False
    isDotCom = False

    # -------------------------------------------------------------------------
    # Token heirachy:
    # -------------------------------------------------------------------------

    # If a user provided a token, that should take highest priority, next
    # is a GITLAB_TOKEN environment variable:

    token = None
    token_var = None

    _availableTokens = {
        '-t': args.token,
        '--token': args.token,
        'GITLAB_TOKEN': environ.get('GITLAB_TOKEN'),
        '-ot': args.oauth_token,
        '--oauth-token': args.oauth_token,
        'GITLAB_OAUTH_TOKEN': environ.get('GITLAB_OAUTH_TOKEN')
    }

    for _type, token in _availableTokens.items():
        if token is not None:
            token_var = _type
            break

    if token is None:
        print(
            'Error: No access token found, you must either have the '
            'environment variables: "GITLAB_TOKEN" / "GITLAB_OAUTH_TOKEN" or '
            'provide a token via the command line (--token/--oauth-token).'
        )
        exit(1)

    oauth = False
    if token_var in ['-ot', '--oauth-token', 'GITLAB_OAUTH_TOKEN']:
        oauth = True

    # -------------------------------------------------------------------------
    # Input sanity:
    # -------------------------------------------------------------------------

    if args.output_format.lower() != 'terminal' and args.output_file is None:
        print(
            'Error: Output format provided but no output file provided'
        )
        exit(1)

    if len(args.url) > 1:
        print('Error: Only one URL is currently supported')
        exit(1)
    else:
        args.url = args.url[0]

    # -------------------------------------------------------------------------
    # Logging:
    # -------------------------------------------------------------------------

    if args.debug is False:
        logLevel = 'INFO'
        logging.getLogger('gql.transport.requests').setLevel(logging.ERROR)
    else:
        logLevel = 'DEBUG'

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=getattr(logging, logLevel.upper())
    )

    # Suppress tokens in logs & max pool size:
    logFilter = log.CustomLogFilter(token)
    logging.getLogger('urllib3.connectionpool').addFilter(logFilter)
    logging.getLogger().addFilter(logFilter)

    logging.debug(f'args: {args}')

    # -------------------------------------------------------------------------
    # Auth to GitLab:
    # -------------------------------------------------------------------------

    urlParsedInput = urlparse(args.url)
    userInputPath = urlParsedInput.path.strip('/')
    userInputHost = f'{urlParsedInput.scheme}://{urlParsedInput.netloc}'  # noqa: E231, E501

    if urlParsedInput.netloc == 'gitlab.com':
        isDotCom = True

    logging.debug(f'{isDotCom=}')

    # instantiate the gl obj:
    gl = gitlab.Gitlab(
        userInputHost,
        private_token=token if not oauth else None,
        oauth_token=token if oauth else None
    )

    # attempt a dry-run auth to make sure the token works:
    try:
        gl.auth()

    except gitlab.exceptions.GitlabAuthenticationError as e:
        print(
            f'Error: The token provided failed to authenticate to: {args.url}'
        )
        logging.debug(f'Auth Error: {e}')
        exit(1)

    except (
        gitlab.exceptions.GitlabHttpError,
        gitlab.exceptions.GitlabGetError
            ) as e:

        logging.debug(f'Exception: {e}')

        if e.response_code == 403 and e.error_message == 'insufficient_scope':
            print(f'Error: The "{token_var}" token has an insufficient scope.')
            exit(1)

        print(
            f'Error: The host: {userInputHost} does not appear to be a '
            'GitLab instance. If this is erroneous, please raise a bug report.'
        )
        exit(1)

    except Exception as e:
        print(f'Error: Unable to connect to GitLab instance: {args.url}')
        logging.debug(f'Connection Error: {e}')
        exit(1)

    # add a warning for gitlab.com admins:
    try:
        if isDotCom is True and gl.user.is_admin:

            if input('\nWARNING: You are authenticated as a GitLab.com admin. '
                     'Running a "full scan" may create significant load.\n\n'
                     '  Do you wish to continue? (y/n): ').lower() == 'y':
                pass
            else:
                exit(0)

    # if CTRL-C was pressed, exit cleanly:
    except KeyboardInterrupt:
        exit(0)

    # if gl.user.is_admin does not return a bool:
    except AttributeError:
        pass

    # -------------------------------------------------------------------------
    # Check if we are dealing with a group or a project:
    # -------------------------------------------------------------------------

    try:
        entity = gl.projects.get(userInputPath)
        isProject = True

    except gitlab.exceptions.GitlabGetError as e:
        if '404 Project Not Found' in str(e):

            try:
                entity = gl.groups.get(userInputPath)
                isGroup = True

            except gitlab.exceptions.GitlabGetError as e:
                if '404 Project Not Found' in str(e):
                    print(
                        'Either you do not have access to the provided URL or '
                        'the URL is invalid. '
                        'Please provide a URL using the following '
                        'format: https://gitlab.com/path-to-group-or-project '
                        'e.g. https://gitlab.com/gitlab/gitlab-com'
                    )
                    exit(1)

    if isGroup is False and isProject is False:
        print(f'Error: Unable to find group/project: "{userInputPath}"')
        exit()

    # -------------------------------------------------------------------------

    # Load the filtered ones from user input:
    filteredRecommendations = readRecommendations(args)
    if len(filteredRecommendations) == 0:
        print('Error: No recommendations were found.')
        exit(1)

    # -------------------------------------------------------------------------

    # format the plan:
    _prof = args.profile if args.profile else ', '.join(
        str(p) for p in PROFILES)

    _ciCon = ', '.join(
        str(ci)
        for ci in args.cis_controls
        if args.cis_controls) if args.cis_controls else 'All applicable'

    _impl = ', '.join(
        args.implementation_groups
        if args.implementation_groups
        else IMPLEMENTATION_GROUPS)

    _start = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

    # -------------------------------------------------------------------------

    graphQLEndpoint = f'{userInputHost}/api/graphql'
    graphQLHeaders = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    workers = args.max_workers if args.max_workers else MAX_WORKERS

    # -------------------------------------------------------------------------

    # determine benchmarks to exec:
    _filteredRecs = len(filteredRecommendations)
    if _filteredRecs == countRecommendations():
        _recs = len(benchmarkFunctions)
    else:
        _recs = _filteredRecs

    # Print the plan to the user:
    print(
        f'\nRunning CIS benchmark scanner: \n\n'
        f' - Scan Started: {_start}\n'
        f' - Host: {userInputHost}\n'
        f' - {"Group" if isGroup else "Project"}: {userInputPath}\n'
        f' - Output Format: {args.output_format}\n'
        f' - Output File: {args.output_file.name if args.output_file else "stdout"}\n'  # noqa: E501
        f' - Profile(s) applied: {_prof}\n'
        f' - CIS Controls: {_ciCon}\n'
        f' - Implementation Group(s): {_impl}\n'
        f' - Benchmarks to check: {_recs}\n\n'
    )

    # -------------------------------------------------------------------------
    # Map the benchmarks:
    # -------------------------------------------------------------------------

    logging.debug(
        'Running CIS benchmark checks '
        f'against {"project" if isProject else "group"}: {userInputPath}'
    )

    results = []
    stats = {
        'PASSED': 0,
        'FAILED': 0,
        'SKIPPED': 0,
        'TOTAL': _recs
    }

    mappedFuncs = mapRecommendations(
        benchmarkFunctions, filteredRecommendations)

    # -------------------------------------------------------------------------
    # Setup kwargs that each benchmark function can have access to:
    # -------------------------------------------------------------------------

    kwargs = {'isDotCom': isDotCom, 'isProject': isProject,
              'isGroup': isGroup, 'graphQLEndpoint': graphQLEndpoint,
              'graphQLHeaders': graphQLHeaders}

    # -------------------------------------------------------------------------
    # Store benchmark results:
    # -------------------------------------------------------------------------

    Benchmark = namedtuple('Benchmark', ['projectCheck', 'result', 'func'])

    def executeBenchmark(_projectFunction, _projectCheck, entity, gl,
                         **kwargs):

        logging.debug(f'Executing benchmark: {_projectFunction.__name__}')
        return Benchmark(
            projectCheck=_projectCheck,
            result=_projectFunction(entity, gl, **kwargs),
            func=_projectFunction)

    # -------------------------------------------------------------------------
    # Projects:
    # -------------------------------------------------------------------------

    if isGroup:
        raise NotImplementedError('We do not support groups just yet...')

    try:

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(
                    executeBenchmark, _projectFunction, _projectCheck, entity,
                    gl, **kwargs)
                for _projectFunction, _projectCheck in mappedFuncs.items()
            ]

            for future in tqdm(
                as_completed(futures),
                total=len(mappedFuncs),
                colour='green',
                desc='Scanning',
                bar_format=(
                    '{l_bar}{bar}| {n_fmt}/{total_fmt} completed '
                    '[elapsed: {elapsed} remaining: {remaining}]')):
                _res = future.result()

                try:
                    if next(iter(_res.result)) is True:
                        _resStr = 'PASS'
                        stats['PASSED'] += 1
                    elif next(iter(_res.result)) is False:
                        _resStr = 'FAIL'
                        stats['FAILED'] += 1
                    elif next(iter(_res.result)) is None:
                        _resStr = 'SKIP'
                        stats['SKIPPED'] += 1
                except TypeError:
                    logging.error(f'Function: {_res.func.__name__} did '
                                  'not return a dict')
                    exit(1)

                result = {
                    'id': _res.projectCheck['id'],
                    'title': _res.projectCheck['title'],
                    'reason': list(_res.result.values())[0],
                    'result': _resStr
                }

                if args.remediations is True:
                    result['remediation'] = _res.projectCheck['remediation']

                if args.omit_skipped is True \
                        and result.get('result') == 'SKIP':
                    continue

                results.append(result)

        output.output(results, stats, args.output_format, args.output_file)

    except KeyboardInterrupt:
        exit(1)

# -----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
