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

You can run this step in GitHub Actions: [collect.yml].
Aggregated collections located in [collect branch].

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

### Extract headings

From each README file we extract it's all headings (text after `#`).
We remove English stop words from each heading. Then, we apply
lemmatization for each word, filter words with `^[a-zA-Z]+$` regex,
and calculate up to 5 most common words across README headings.

For instance, this README:

```markdown
# Building web applications in Java with Spring Boot 3
...

## Agenda
...

## Who am I?
...

## Prerequisites
...

## Outcomes
...

## What is Spring?
...

## Resources
...

### Dan Vega
...

### Spring
... 

### Documentation
...

### Books
...

### Podcasts
...

### YouTube
...
```

Will be transformed to:

```text
['spring', 'build', 'web', 'application', 'java']
```

To run this:

```bash
just extract after-filter.csv
```

You should expect to have `sr-data/experiment/after-extract.csv`.

### Generate embeddings

For each repo, we aggregate all [top words](#extract-headings) from README file
headings into string. We convert each string to three variants of embeddings:
[S-BERT], [E5], [Embedv3].

To run this:

```bash
just embed after-extract.csv
```

You should expect to have three files:

* `sr-data/experiment/embeddings-s-bert-384.csv`
* `sr-data/experiment/embeddings-e5-1024.csv`
* `sr-data/experiment/embeddings-embedv3-1024.csv`

### Create datasets

We calculate SR-score from numerical metadata for each repository, and create
seven datasets from prepared data:

* `scores.csv`, dataset with SR-scores;
* `sbert.csv`, dataset from S-BERT-384 embeddings;
* `e5.csv`, dataset from E5-1024 embeddings;
* `embedv3.csv`, dataset from Embedv3 embeddings;
* `scores+sbert.csv`, combination of SR-score and S-BERT-384 embeddings;
* `scores+e5.csv`, combination of SR-score and E5-1024 embeddings;
* `scores+embedv3.csv`, combination of SR-score and Embedv3-1024 embeddings;

To run this:

```bash
just datasets
```

You should expect to have all seven files in `sr-data/experiment` directory.

### Cluster

We apply [clustering][Cluster analysis] on our previously
[created datasets](#create-datasets). We use the following algorithms:

* [KMeans]
* [Agglomerative clustering]
* [DBSCAN]
* [GMM]

Each algorithm generates set of clusters for each dataset.

To run this:

```bash
just cluster
```

You should expect to have the following directories inside `experiment`
directory:

* `kmeans`
* `agglomerative`
* `dbscan`
* `gmm`

Each directory have its subs named after dataset name: `e5`, `embedv3`,
`scores+sbert`, etc. In each subdirectory you should have `config.json|txt`
file with used model parameters, and `clusters` directory with files containing
clustered repositories. Each file, for instance `0.txt`, where `0` is cluster
identifier, hosts list of repositories in `OWNER/REPO` format, separated by new
line:

```text
Faceplugin-ltd/FaceRecognition-LivenessDetection-Android
LxxxSec/CTF-Java-Gadget
flutter-youni/flutter_youni_gromore
ax1sX/RouteCheck-Alpha
darksolopic/PasswordManagerGUI
borjavb/bq-lineage-tool
...
```

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
[S-BERT]: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
[E5]: https://huggingface.co/intfloat/e5-large
[Embedv3]: https://cohere.com/blog/introducing-embed-v3
[KMeans]: https://en.wikipedia.org/wiki/K-means_clustering
[Cluster analysis]: https://en.wikipedia.org/wiki/Cluster_analysis
[Agglomerative clustering]: https://en.wikipedia.org/wiki/Hierarchical_clustering
[DBSCAN]: https://en.wikipedia.org/wiki/DBSCAN
[GMM]: https://en.wikipedia.org/wiki/Mixture_model
[collect.yml]: https://github.com/h1alexbel/sr-detection/actions/workflows/collect.yml
[collect branch]: https://github.com/h1alexbel/sr-detection/tree/collect
