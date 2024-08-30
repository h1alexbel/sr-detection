# The MIT License (MIT)
#
# Copyright (c) 2024 Aliaksei Bialiauski
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Verify versions.
versions:
  python3 --version
  poetry --version
  cargo --version
  npm --version

# Full build.
full:
  just install
  just test
  just check

# Install dependencies.
install:
  poetry install
  npm install -g ghminer@0.0.5

# Run tests.
test:
  poetry run pytest

# Check quality of source code.
check:
  git ls-files '*.py' | xargs -I {} sh -c \
    ' echo "Running Pylint for {}" poetry run pylint "$@" echo "Running Flake8 for {}" poetry run flake8 "$@" \
     ' _ {}

# Run experiment.
@experiment:
  EID=$(uuidgen); echo ID of experiment is: "$EID"
  NOW=$(date +%F):$(date +%T); echo Experiment date is: "$NOW"
  just collect
  just filter

# Collect repositories.
collect:

# Filter collected repositories.
filter:

# Build paper with LaTeX.
paper:
  latexmk --version
  cd sr-paper && latexmk paper.tex -pdf
