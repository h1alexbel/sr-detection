"""
Compose all found metadata into final CSV.
"""
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
import pandas as pd


def main(latest, out):
    frame = pd.read_csv(latest)
    frame = frame[
        [
            "repo",
            "releases_count",
            "open_issues_count",
            "branches_count",
            "pulls_count",
            "readme_len",
            "readme_avg_slen",
            "readme_avg_wlen",
            "readme_hcount",
            "readme_snippets_count",
            "readme_mcw",
            "readme_example_count",
            "readme_sample_count",
            "readme_demonstration_count",
            "readme_links",
            "readme_links_count",
            "readme_pmentions",
            "readme_imentions",
            "maven_projects_count",
            "maven_plugins",
            "maven_wars_count",
            "maven_jars_count",
            "maven_poms_count",
            "junit_tests"
        ]
    ]
    frame.to_csv(out, index=False)
