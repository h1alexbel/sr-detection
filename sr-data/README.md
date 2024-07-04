# sr-data

`sr-data` consists of a set of tasks that collects, preprocesses and vectorizes
data about GitHub repositories.

## How it works?

`sr-data` runs a [task](#tasks) or a set of tasks and produces output.
To run all tasks:

```bash
poetry run sr-data
```

All tasks will be executed in order, and you should expect to have these
[CSVs][CSV]:

* `repos.csv`
* `filtered.csv`
* `preprocessed.csv`
* `text.csv`
* `highlighted.csv`
* `embeddings.csv`
* `u.csv`
* `v.csv`
* `w.csv`

In order to run single task in isolation, use it like that:

```bash
poetry run sr-data:collect
```

## Tasks

* `collect`, collects data about public repositories through
[GitHub GraphQL API] and outputs `repos.csv` CSV with gathered repositories
and their [metadata](#collected-metadata).
* `en-filter`, filters out repositories with non-English README file and
outputs `filtered.csv` CSV with English-only entries.
* `text`, converts README markdown content into plain text, outputs
`text.csv` CSV.
TBD..

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
[GitHub GraphQL API]: https://api.github.com/graphql
