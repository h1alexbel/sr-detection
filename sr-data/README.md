# SR Data

`sr-data` consists of a set of scripts that filter collected metadata about
GitHub repositories, and converts them into numerical vectors.

## Collected Metadata

<!-- metadata_begin -->
```text
repo
releases
pulls
open_issues
branches
has_workflows
has_release_workflow
w_simplicity
tests
```
<!-- metadata_end -->

## How to test?

Run this:

```bash
poetry run pytest sr-data
```
