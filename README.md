# sr-detection

[![build](https://github.com/h1alexbel/sr-detection/actions/workflows/build.yml/badge.svg)](https://github.com/h1alexbel/sr-detection/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/h1alexbel/sr-detection/graph/badge.svg?token=lY3BaDIccI)](https://codecov.io/gh/h1alexbel/sr-detection)
[![Docker Image Version](https://img.shields.io/docker/v/h1alexbel/sr-detection)](https://hub.docker.com/repository/docker/h1alexbel/sr-detection)
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

* [sr-data](/sr-data), module that consists of a set of tasks that aggregates
and filters [collected metadata] about GitHub repositories.
* [sr-train](/sr-train), module for training ML models to identify SRs.

## Hypotheses

Our research based on the following hypotheses:

* `SR`s usually don't have release pipeline inside `.github/workflows`
* `SR`s usually have less strict build pipeline inside `.github/workflows`
* `SR`s usually don't have releases
* `SR`s have less pull requests
* `SR`s don't have section about how to use it
* `SR`s have more disconnected directories/files

## Run experiments

First, prepare datasets:

```bash
docker run --rm -v "$(pwd)/output:/collection" -e START="<start date>" \
  -e END="<end date>" -e COLLECT_TOKEN="<GitHub PAT to collect repositories>" \
  -e COLLECT_TOKEN="<GitHub PAT to fetch metadata>" \
  -e HF_TOKEN="<Huggingface PAT>" -e COHERE_TOKEN="<Cohere API token>" \
  -e OUT="sr-data" h1alexbel/sr-detection
```

In the output directory you should have these datasets:

* `d1-scores.csv`
* `d2-sbert.csv`
* `d3-e5.csv`
* `d4-embedv3.csv`
* `d5-scores+sbert.csv`
* `d6-scores+e5.csv`
* `d7-scores+embedv3.csv`

Alternatively, you can download existing datasets from [gh-pages] branch.

Then, you should run models against collected datasets via [cluster.yml]. Models
will distribute repositories from each dataset into clusters. The clustering
results will be placed into [clusters] branch.

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
[gh-pages]: https://github.com/h1alexbel/sr-detection/tree/gh-pages
[collected metadata]: sr-data/README.md#collected-metadata
[cluster.yml]: https://github.com/h1alexbel/sr-detection/blob/master/.github/workflows/cluster.yml
[clusters]: https://github.com/h1alexbel/sr-detection/tree/clusters
