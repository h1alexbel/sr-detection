# sr-detection

[![build](https://github.com/h1alexbel/sr-detection/actions/workflows/build.yml/badge.svg)](https://github.com/h1alexbel/sr-detection/actions/workflows/build.yml)
[![Hits-of-Code](https://hitsofcode.com/github/h1alexbel/sr-detection)](https://hitsofcode.com/view/github/h1alexbel/sr-detection)
[![PDD status](http://www.0pdd.com/svg?name=h1alexbel/sr-detection)](http://www.0pdd.com/p?name=h1alexbel/sr-detection)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/h1alexbel/sr-detection/blob/master/LICENSE.txt)

The goal of the study is to create a model that, by looking at the README file
and meta-information, can identify GitHub "sample repositories" (SR), that
mostly contain educational or demonstration materials supposed to be copied
instead of reused as a dependency.

**Motivation**. During the work on [CaM] project, we were required to
[filter out repositories with samples][cam-227]. No readily available
technique or tool existed that could perform that function, so we conducted
research on this very subject.

The repository structured as follows:

* [sr-data](/sr-data), module that consists of a set of tasks that filters
collected metadata about GitHub repositories.
* [sr-train](/sr-train), module for training ML models.
* [sr-detector](sr-detector), trained and reusable model for SR detection.
* [sr-paper](/sr-paper), LaTeX source for a paper on SR detection.

## Experiment's steps

### Metadata collection

We collect two-fold metadata for each GitHub repository: numerical, and
textual. For numerical we collect:

* `releases`, the number of releases.
* `pulls`, the number of pull requests.
* `issues`, the total number of issues (opened + closed).
* `branches`, the number of branches.
* `actions`, the number of GitHub Actions workflow files.
For textual: `README.md` file.

To run this:

```bash
just collect
```

You should expect to have `sr-data/experiment/repos.csv` with collected
repositories and their metadata.

To capture smaller amount of repositories you can run this:

```bash
just test-collect
```

You should expect to have `sr-data/tmp/test-repos.csv`, with the same structure
as `repos.csv`, but smaller.

### Filter

We filter collected repositories. We remove repositories with empty README
file. Then, we convert README file to plain text and check in which languages
file is written. We remove repositories with README file that is not fully
written in English.

To run this:

```bash
just filter repos.csv
```

You should expect to have `sr-data/experiment/after-filter.csv`.

## How to contribute

Make sure that you have [Python 3.10+], [just], and [npm] installed on your
system, fork this repository, make changes, send us a [pull request][guidelines].
We will review your changes and apply them to the `master` branch shortly,
provided they don't violate our quality standards. To avoid frustration, before
sending us your pull request please run full build:

```bash
just full
```

[CaM]: https://github.com/yegor256/cam
[cam-227]: https://github.com/yegor256/cam/issues/227
[guidelines]: https://www.yegor256.com/2014/04/15/github-guidelines.html
[Python 3.10+]: https://www.python.org/downloads/release/python-3100
[npm]: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm
[just]: https://just.systems/man/en/chapter_4.html
