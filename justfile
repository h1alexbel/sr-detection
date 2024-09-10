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
  NOW=$(date +%F):$(TZ=UTC date +%T) && echo "$NOW" >> now.txt; \
    echo Experiment datetime is: "$NOW (UTC)"
  mkdir -p sr-data/experiment
  mv now.txt sr-data/experiment/now.txt
  just collect
  just filter experiment/repos.csv
  just extract experiment/after-filter.csv

# Clean up experiment.
clean:
  echo "Cleaning up sr-data/experiment..."
  rm sr-data/experiment/* && rmdir sr-data/experiment

# Collect repositories.
collect:
  mkdir -p sr-data/experiment
  ghminer --query "stars:>10 language:java size:>=20 mirror:false template:false" \
    --start "2019-01-01" --end "2024-05-01" --tokens "$PATS" \
    --filename "repos" && mv repos.csv sr-data/experiment/repos.csv

# Collect test repositories.
test-collect:
  mkdir -p sr-data/tmp
  cd sr-data && ghminer --query "stars:>10 language:java size:>=20 mirror:false template:false" \
    --start "2024-05-01" --end "2024-05-01" --tokens "$PATS" \
    --filename "tmp/test-repos"

# Filter collected repositories.
filter repos out="experiment/after-filter.csv":
  cd sr-data && poetry poe filter --repos {{repos}} --out {{out}}

# Extract headings from README files.
extract repos out="experiment/after-extract.csv":
  cd sr-data && poetry poe extract --repos {{repos}} --out {{out}}

# Create embeddings.
embed repos prefix="embeddings":
  cd sr-data && poetry poe embed --repos {{repos}} --prefix {{prefix}} \
    --hf "$HF_TOKEN" --cohere "$COHERE_TOKEN"

# Calculate TF-IDF for README files.
tfidf repos out="experiment/after-tfidf.csv":
  cd sr-data && poetry poe tfidf --repos {{repos}} --out {{out}}

# Build paper with LaTeX.
paper:
  latexmk --version
  cd sr-paper && latexmk paper.tex -pdf
