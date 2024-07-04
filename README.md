# sr-detection

The goal of the study is to create a model that, by looking at the README file
and meta-information, can identify GitHub ``sample repositories'' (SR), that
mostly contain educational or demonstration materials supposed to be copied
instead of reused as a dependency.

**Motivation**. During the work on [CaM] project, we were required to
[filter out repositories with samples][cam-issue]. No readily available
technique or tool existed that could perform that function, so we conducted
research on this very subject.

The repository structured as follows:

* [sr-data](/sr-data), module for collection, preprocessing and preparing the
SR data.
* [sr-train](/sr-train), module for training ML models.
* [sr-detector](sr-detector), trained and reusable model for SR detection.
* [sr-paper](/sr-paper), LaTeX source for a paper on SR detection.

## How to contribute

It's a Python project, so make sure that you have [Python 3.11+] on your
system, fork this repository, make changes, send us a [pull request][guidelines].
We will review your changes and apply them to the `master` branch shortly,
provided they don't violate our quality standards. To avoid frustration, before
sending us your pull request please run full build:

```bash
poetry build
```

[CaM]: https://github.com/yegor256/cam
[cam-issue]: https://github.com/yegor256/cam/issues/227
[guidelines]: https://www.yegor256.com/2014/04/15/github-guidelines.html
[Python 3.11+]: https://www.python.org/downloads/release/python-3110
