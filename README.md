# sr-detection

[![poetry](https://github.com/h1alexbel/sr-detection/actions/workflows/poetry.yml/badge.svg)](https://github.com/h1alexbel/sr-detection/actions/workflows/poetry.yml)
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

* [sr-data](/sr-data), module for collection, filtering, and preparing SR data
for models.
* [sr-train](/sr-train), module for training ML models.
* [sr-detector](sr-detector), trained and reusable model for SR detection.
* [sr-paper](/sr-paper), LaTeX source for a paper on SR detection.

## How to contribute

Make sure that you have [Python 3.10+], [npm], and [just] installed on your
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
