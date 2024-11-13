#!/bin/bash
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
echo "$COLLECT_TOKEN" >> "$PATS"
{
  "$RUN"/just install
  poetry install
  "$RUN"/just collect "collection/$OUT" "$START" "$END" "repos"
  "$RUN"/just pulls "../repos.csv" "$GH_TOKEN" "../repos-with-pulls.csv"
  "$RUN"/just filter "../repos-with-pulls.csv" "../after-filter.csv"
  "$RUN"/just extract "../after-filter.csv" "../after-extract.csv"
  "$RUN"/just embed "../after-extract.csv" "../embeddings"
  cp "embeddings-s-bert-384.csv" "sbert.csv"
  cp "embeddings-e5-1024.csv" "e5.csv"
  cp "embeddings-embedv3-1024.csv" "embedv3.csv"
  "$RUN"/just datasets "$RUN" "../" "after-extract.csv"
} 2>&1 | tee -a collect.log
sed -i "s|$GH_TOKEN|REDACTED|g" collect.log
sed -i "s|$HF_TOKEN|REDACTED|g" collect.log
sed -i "s|$COHERE_TOKEN|REDACTED|g" collect.log
mkdir -p "collection/$OUT/steps"
files=(
  "repos.csv"
  "repos-with-pulls.csv"
  "after-filter.csv"
  "after-extract.csv"
  "embeddings-s-bert-384.csv"
  "embeddings-e5-1024.csv"
  "embeddings-embedv3-1024.csv"
)
id=1
for file in "${files[@]}"; do
  cp "$file" "collection/$OUT/steps/$(printf '%02d' "$id")-$file"
  id="$((id+1))"
done
cp "collect.log" "collection/$OUT"
cp "scores.csv" "collection/$OUT/d1-scores.csv"
cp "sbert.csv" "collection/$OUT/d2-sbert.csv"
cp "e5.csv" "collection/$OUT/d3-e5.csv"
cp "embedv3.csv" "collection/$OUT/d4-embedv3.csv"
cp "d5-scores+sbert.csv" "collection/$OUT"
cp "d6-scores+e5.csv" "collection/$OUT"
cp "d7-scores+embedv3.csv" "collection/$OUT"
