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
  cd sr-train && poetry install

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

# SR-data pipeline for the experiments.
pipeline steps pipes out representation="resources/pipeline.json":
  cd sr-data && poetry poe pipeline --representation {{representation}} \
   --steps {{steps}} --pipes "{{pipes}}" --out "{{out}}"

# Clean up experiment.
clean:
  echo "Cleaning up sr-data/experiment..."
  rm sr-data/experiment/* && rmdir sr-data/experiment

# Collect repositories.
collect dir query start end out:
  mkdir -p {{dir}}
  ghminer --query "{{query}}" --start "{{start}}" --end "{{end}}" \
   --tokens "$PATS" --filename "{{out}}"

# Fetch pulls count for collected repos.
pulls repos token out="experiment/with-pulls.csv":
  cd sr-data && poetry poe pulls --repos "{{repos}}" --token "{{token}}" \
    --out "{{out}}"

# Collect maven pom.xml files.
maven repos token out="experiment/with-maven.csv":
  cd sr-data && poetry poe maven --repos "{{repos}}" --out "{{out}}" \
    --token "{{token}}"

# Count of JUnit tests.
junit repos token out="experiment/after-junit.csv":
  cd sr-data && poetry poe junit --repos "{{repos}}" --out "{{out}}" \
   --token "{{token}}"

# Collect test repositories.
test-collect:
  mkdir -p sr-data/tmp
  cd sr-data && ghminer --query "stars:>10 language:java size:>=20 mirror:false template:false" \
    --start "2024-05-01" --end "2024-05-01" --tokens "$PATS" \
    --filename "tmp/test-repos"

# License filter.
license_filter repos out="experiment/after-license-filter.csv":
  cd sr-data && poetry poe license_filter --repos "{{repos}}" --out "{{out}}"

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

# Count snippets.
snippets repos out="experiment/after-snippets.csv":
  cd sr-data && poetry poe snippets --repos {{repos}} --out {{out}}

# Count links.
links repos out="experiment/after-links.csv":
  cd sr-data && poetry poe links --repos {{repos}} --out {{out}}

# GitHub pull requests and issues mentions
ghmentions repos out="experiment/after-ghmentions.csv":
  cd sr-data && poetry poe ghmentions --repos {{repos}} --out {{out}}

# Run sentiment analysis on READMEs
sentiments repos out="experiment/after-sentiments.csv":
  cd sr-data && poetry poe sentiments --repos {{repos}} --out {{out}}

# GitHub workflows info.
workflows repos out="experiment/after-workflows.csv":
  cd sr-data && poetry poe workflows --repos {{repos}} --out {{out}}

# Compose all found metadata into final CSV.
final latest out="experiment/final.csv":
  cd sr-data && poetry poe final --latest {{latest}} --out {{out}}

# Create embeddings.
embed repos prefix="experiment/embeddings":
  cd sr-data && poetry poe embed --repos "{{repos}}" --prefix {{prefix}} \
    --hf "$HF_TOKEN" --cohere "$COHERE_TOKEN"

# Create datasets.
# @todo #134:35min: Remove run ad-hoc solution for just command resolution.
#  Now, we passing run parameter from recipe to nested just invocations in
#  order to resolve just command. We should refine our usage of full path in
#  the entire justfile.
# @todo #134:45min: Refactor recipes to be more optimally granular.
#  We should create more major recipes in order to reuse across the project.
#  The example of such step is `@experiment`. Let's do similar to the script
#  inside `data.sh`, so it can be invoked from just using datasets step.
datasets embeddings run dir="experiment" numbase="after-extract.csv":
  "{{run}}"/just numerical "{{dir}}/{{numbase}}" "{{dir}}/numerical.csv"
  "{{run}}"/just scores "{{dir}}/{{numbase}}" "{{dir}}/scores.csv"
  "{{run}}"/just combine "{{run}}" "{{embeddings}}" "{{dir}}"

# Combine datasets with embeddings.
combine run embeddings dir:
  if "{{embeddings}}"; then \
    "{{run}}"/just combination "{{dir}}" 5 "{{dir}}/sbert.csv" "{{dir}}/scores.csv" \
    "{{run}}"/just combination "{{dir}}" 6 "{{dir}}/e5.csv" "{{dir}}/scores.csv" \
    "{{run}}"/just combination "{{dir}}" 7 "{{dir}}/embedv3.csv" "{{dir}}/scores.csv" \
  fi

# Create scores dataset.
scores repos out="experiment/scores.csv":
  cd sr-data && poetry poe scores --repos "{{repos}}" --out "{{out}}"

# Create all numerical dataset.
numerical repos out="experiment/numerical.csv":
  cd sr-data && poetry poe numerical --repos "{{repos}}" --out "{{out}}"

# Create dataset from combination.
combination dir identifier embeddings scores="experiment/scores.csv":
  cd sr-data && poetry poe combination --scores "{{scores}}" \
    --embeddings "{{embeddings}}" --dir "{{dir}}" --identifier "{{identifier}}"

# Merge dataset folders into one.
merge datasets out branch:
  cd sr-data && poetry poe merge --datasets "{{datasets}}" --out "{{out}}" \
   --branch "{{branch}}"

# Download datasets.
dataset folder out:
  cd sr-train && poetry poe dataset --folder "{{folder}}" --out "{{out}}"

# Cluster repositories.
cluster dir out:
  cd sr-train && poetry poe cluster --dataset "{{dir}}/d1-scores.csv" --dir {{out}}
  cd sr-train && poetry poe cluster --dataset "{{dir}}/d2-sbert.csv" --dir {{out}}
  cd sr-train && poetry poe cluster --dataset "{{dir}}/d3-e5.csv" --dir {{out}}
  cd sr-train && poetry poe cluster --dataset "{{dir}}/d4-embedv3.csv" --dir {{out}}
  cd sr-train && poetry poe cluster --dataset "{{dir}}/d5-scores+sbert.csv" --dir {{out}}
  cd sr-train && poetry poe cluster --dataset "{{dir}}/d6-scores+e5.csv" --dir {{out}}
  cd sr-train && poetry poe cluster --dataset "{{dir}}/d7-scores+embedv3.csv" --dir {{out}}

# Statistics about generated clusters.
clusterstat out dir="experiment":
  cd sr-train && poetry poe clusterstat --dir {{dir}} --out {{out}}

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

# Remove readme from CSV file.
# Can be useful for inspecting large files.
noreadme repos out="experiment/no-readme.csv":
  cd sr-data && poetry poe no_readme --repos {{repos}} --out {{out}}

# Build paper with LaTeX.
paper:
  latexmk --version
  cd sr-paper && latexmk paper.tex -pdf
