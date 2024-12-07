### Description
<!-- What changes are being introduced? -->

## Requester
<!-- Please ensure the checklist items are complete before requesting a review of this MR-->

<details><summary>Requester Checklist</summary>

- If this change modifies [benchmark functions](https://gitlab.com/gitlab-org/govern/compliance/engineering/cis/gitlabcis/-/tree/main/gitlabcis/benchmarks?ref_type=heads):
  - The function:
    - [ ] Name matches the `name` of the yaml recommendation
    - [ ] Returns a `dict` containing:
      - `True` or `False` (if the check passed/failed)
      - `None` for skipped checks
      - a `str` with the reason why (e.g. `{None: 'This check requires validation'}`)
    - [ ] The `docstring` contains the id and title of the recommendation to check
  - Limitations:
    - [ ] Any limitations for the function are added to [docs/limitations.md](https://gitlab.com/gitlab-org/govern/compliance/engineering/cis/gitlabcis/-/tree/main/docs/limitations.md)
- If this change modifies [recommendations](https://gitlab.com/gitlab-org/govern/compliance/engineering/cis/gitlabcis/-/tree/main/gitlabcis/recommendations):
  - [ ] Ensure approval from `CODEOWNERS` is obtained
- [ ] All unit tests pass before requesting review
- [ ] This merge request's title matches the prefixes allowed in `.commitlintrc`
- [ ] Remove _Draft_ phase from the MR

</details>

## Reviewer(s)
<!-- Please ensure this MR meets the requirements before approving & merging -->

<details><summary>Reviewer Checklist</summary>

- If this change modifies [benchmark functions](https://gitlab.com/gitlab-org/govern/compliance/engineering/cis/gitlabcis/-/tree/main/gitlabcis/benchmarks?ref_type=heads):
  - [ ] The function(s) satisfy the recommendation _(see the `audit` section in the yaml file)_
    - i.e. does this function address the recommendation benchmark check
- [ ] This merge request's title matches the prefixes allowed in `.commitlintrc`
- [ ] All tests have passed successfully

</details>

### Local validation
<!-- You can validate benchmark functions by following the below steps -->

To validate changes to benchmark functions for this merge request, follow the below:

<details><summary>validation steps</summary>

Clone the repo:

```sh
git clone git@gitlab.com:gitlab-com/gl-security/security-operations/sirt/automation/cis-benchmark-scanner.git
cd cis-benchmark-scanner
```

Checkout into the merge request branch:

```sh
git checkout $branchRequestingToMerge
```

Install the version in the merge request:

```sh
make install
```

Validate the function(s) against a project:

```sh
gitlabcis https://gitlab.example.com/path/to/project
```

To test a single benchmark functon:

```sh
gitlabcis https://gitlab.example.com/path/to/project \
    -ids 1.1.1
```

</details>

<!-- Labels, assignee & tags -->

/assign me

/draft
