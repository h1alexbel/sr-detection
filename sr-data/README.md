# sr-data

`sr-data` consists of a set of tasks that collects, preprocesses and vectorizes
data about GitHub repositories.

## How it works?

`sr-data` runs a task or a set of [tasks](#tasks) and produces some output.
To run all tasks:

```bash
poetry run sr-data
```

All tasks will be executed in order, with default arguments, and you should
expect to have these [CSVs][CSV]:

* `repos.csv`
* `filtered.csv`
* `embeddings.csv`
* `u.csv`
* `v.csv`
* `w.csv`

In order to run single task in isolation, then use it like that
(run it inside `/sr-data` dir!):

```bash
poetry poe <task id> # e.g. collect
```

Most tasks in isolation require some arguments to pass. To observe them run:

```bash
poetry poe <task id> --help
```

Make sure you have [poethepoet] installed.

## Tasks

* `collect`, collects data about public repositories through
[GitHub GraphQL API] and outputs `repos.csv` with gathered repositories
and their [metadata](#collected-metadata).
* `filter`, filters out repositories with non-English README and outputs
`filtered.csv`.
* `embed`, generates embeddings for README content, outputs `embeddings.csv`.
* `u`, constructs a set of vectors with numerical metadata, outputs `u.csv`.
* `v`, constructs a set of vectors with README, outputs `v.csv`.
* `w`, constructs a set of vectors with both: numerical metadata and README,
outputs `w.csv`.

## Collected metadata

We collect these metadata attributes for each repository:

* `repo`, full name of repository on GitHub, e.g. `apache/kafka`, used only for
identification purposes.
* `readme`, README.md file.
* `releases`, the number of releases.
* `pulls`, the number of pull requests.
* `issues`, the total number of issues (opened + closed).
* `branches`, the number of branches.
* `workflows`, the number of GitHub Actions workflow files.

[CSV]: https://en.wikipedia.org/wiki/Comma-separated_values
[poethepoet]: https://poethepoet.natn.io/poetry_plugin.html
[GitHub GraphQL API]: https://api.github.com/graphql
