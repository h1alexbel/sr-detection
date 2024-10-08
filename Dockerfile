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

FROM python:3.13-slim

# Poetry environment variables.
ENV POETRY_VERSION=1.8.0 \
    POETRY_VIRTUALENVS_CREATE=false \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Python3.
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    rm -rf /var/lib/apt/lists/*

# PATH.
ENV PATH="/root/.local/bin:${HOME}/.cargo/bin:${PATH}"

# NodeJS
RUN rm -rf /usr/lib/node_modules \
  && curl -sL https://deb.nodesource.com/setup_18.x -o /tmp/nodesource_setup.sh \
  && bash /tmp/nodesource_setup.sh \
  && apt-get -y install nodejs --no-install-recommends \
  && bash -c 'node --version' \
  && bash -c 'npm --version'

# Rust, Cargo, Just.
ENV PATH="${PATH}:${HOME}/.cargo/bin"
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y \
  && echo 'export PATH=${PATH}:${HOME}/.cargo/bin' >> /root/.profile \
  && ${HOME}/.cargo/bin/rustup toolchain install stable \
  && bash -c '"${HOME}/.cargo/bin/cargo" --version' \
  && bash -c '"${HOME}/.cargo/bin/cargo" install just@1.30.1'

COPY sr-data ./sr-data
COPY pyproject.toml justfile ./
RUN bash -c '"${HOME}/.cargo/bin/just" install'
RUN poetry install --no-root
COPY . .
ENTRYPOINT ["/root/.cargo/bin/just"]
