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

# Install dependencies.
install:
  ${RULTOR:+sudo} npm install -g ghminer@0.0.7
  poetry self add 'poethepoet[poetry_plugin]'
  cd sr-data && poetry install

# Full build.
full tests="fast":
  poetry install
  just test "{{tests}}"
  just check

# Run tests.
test which="fast":
  poetry run pytest -m "{{which}}"

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
  just embed experiment/after-extract.csv
  just datasets
  just cluster

# Clean up experiment.
clean:
  echo "Cleaning up sr-data/experiment..."
  rm sr-data/experiment/* && rmdir sr-data/experiment

# Collect repositories.
collect dir start end out:
  mkdir -p {{dir}}
  ghminer --query "stars:>10 language:java size:>=20 mirror:false template:false NOT android" \
    --start "{{start}}" --end "{{end}}" --tokens "$PATS" --filename "{{out}}"

# Fetch pulls count for collected repos.
pulls repos token out="experiment/with-pulls.csv":
  cd sr-data && poetry poe pulls --repos "{{repos}}" --token "{{token}}" \
    --out "{{out}}"

# Collect maven pom.xml files.
maven repos token out="experiment/with-maven.csv":
  cd sr-data && poetry poe maven --repos "{{repos}}" --token "{{token}}" \
    --out "{{out}}"

# Collect test repositories.
test-collect:
  mkdir -p sr-data/tmp
  cd sr-data && ghminer --query "stars:>10 language:java size:>=20 mirror:false template:false" \
    --start "2024-05-01" --end "2024-05-01" --tokens "$PATS" \
    --filename "tmp/test-repos"

# Filter collected repositories.
filter repos out="experiment/after-filter.csv":
  cd sr-data && poetry poe filter --repos "{{repos}}" --out "{{out}}"

# Extract headings from README files.
extract repos out="experiment/after-extract.csv":
  cd sr-data && poetry poe extract --repos "{{repos}}" --out "{{out}}"

# Collect most common words.
mcw repos out="experiment/after-mcw.csv":
  cd sr-data && poetry poe mcw --repos "{{repos}}" --out "{{out}}"

# Special words count.
swc repos out="experiment/after-swc.csv" config="resources/swc-words.txt":
  cd sr-data && poetry poe swc --repos "{{repos}}" --out "{{out}}" \
    --config "{{config}}"

# Calculate length metrics.
lens repos out="experiment/after-lens.csv":
  cd sr-data && poetry poe lens --repos {{repos}} --out {{out}}

# Compose all found metadata into final CSV.
final latest out="experiment/final.csv":
  cd sr-data && poetry poe final --latest {{latest}} --out {{out}}

# Create embeddings.
embed repos prefix="experiment/embeddings":
  cd sr-data && poetry poe embed --repos {{repos}} --prefix {{prefix}} \
    --hf "$HF_TOKEN" --cohere "$COHERE_TOKEN"

# Create datasets.
datasets dir="experiment":
  just numerical "{{dir}}/after-extract.csv"
  just scores "{{dir}}/after-extract.csv"
  cp "sr-data/{{dir}}/embeddings-s-bert-384.csv" "sr-data/{{dir}}/sbert.csv"
  cp "sr-data/{{dir}}/embeddings-e5-1024.csv" "sr-data/{{dir}}/e5.csv"
  cp "sr-data/{{dir}}/embeddings-embedv3-1024.csv" "sr-data/{{dir}}/embedv3.csv"
  just combination {{dir}} "{{dir}}/sbert.csv"
  just combination {{dir}} "{{dir}}/e5.csv"
  just combination {{dir}} "{{dir}}/embedv3.csv"

# Create scores dataset.
scores repos out="experiment/scores.csv":
  cd sr-data && poetry poe scores --repos {{repos}} --out {{out}}

# Create all numerical dataset.
numerical repos out="experiment/numerical.csv":
  cd sr-data && poetry poe numerical --repos {{repos}} --out {{out}}

# Create dataset from combination.
combination dir embeddings scores="experiment/scores.csv":
  cd sr-data && poetry poe combination --scores {{scores}} \
    --embeddings {{embeddings}} --dir {{dir}}

# Cluster repositories.
cluster dir="experiment":
  cd sr-data && poetry poe cluster --dataset "experiment/numerical.csv" --dir {{dir}}
  cd sr-data && poetry poe cluster --dataset "experiment/scores.csv" --dir {{dir}}
  cd sr-data && poetry poe cluster --dataset "experiment/sbert.csv" --dir {{dir}}
  cd sr-data && poetry poe cluster --dataset "experiment/e5.csv" --dir {{dir}}
  cd sr-data && poetry poe cluster --dataset "experiment/embedv3.csv" --dir {{dir}}
  cd sr-data && poetry poe cluster --dataset "experiment/scores+sbert.csv" --dir {{dir}}
  cd sr-data && poetry poe cluster --dataset "experiment/scores+e5.csv" --dir {{dir}}
  cd sr-data && poetry poe cluster --dataset "experiment/scores+embedv3.csv" --dir {{dir}}

# Fill in labels in repositories dataset.
labels dir="experiment":
  cd sr-data && poetry poe labels --repos "experiment/numerical.csv" --dir {{dir}}
  cd sr-data && poetry poe labels --repos "experiment/scores.csv" --dir {{dir}}
  cd sr-data && poetry poe labels --repos "experiment/sbert.csv" --dir {{dir}}
  cd sr-data && poetry poe labels --repos "experiment/e5.csv" --dir {{dir}}
  cd sr-data && poetry poe labels --repos "experiment/embedv3.csv" --dir {{dir}}
  cd sr-data && poetry poe labels --repos "experiment/scores+sbert.csv" --dir {{dir}}
  cd sr-data && poetry poe labels --repos "experiment/scores+e5.csv" --dir {{dir}}
  cd sr-data && poetry poe labels --repos "experiment/scores+embedv3.csv" --dir {{dir}}

# Label Propagation model training on repos `repos`, should be saved to `out`.
lpm repos out:
  cd sr-data && poetry poe lpm --repos {{repos}} --out {{out}}

# Build paper with LaTeX.
paper:
  latexmk --version
  cd sr-paper && latexmk paper.tex -pdf
