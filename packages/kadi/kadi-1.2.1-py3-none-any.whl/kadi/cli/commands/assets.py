# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import glob
import os
import re
import shutil
import sys

import click
from flask import current_app

from kadi.cli.main import kadi
from kadi.cli.utils import echo_danger
from kadi.cli.utils import echo_success
from kadi.cli.utils import run_command
from kadi.lib.security import hash_value
from kadi.lib.utils import compact_json


@kadi.group()
def assets():
    """Utility commands for asset management."""


prefix_option = click.option(
    "-p",
    "--prefix",
    type=click.Path(exists=True),
    help="The path that contains all configuration files needed by npm.",
)


@assets.command()
@prefix_option
def build(prefix):
    """Build and compile all static assets for use in production.

    This will install all missing frontend dependencies, run webpack to build all
    minified asset bundles and then tag all static files using their MD5 hash.
    Additionally, a manifest file "manifest.json" mapping the original files to their
    tagged counterparts will also be created.
    """
    _clean_assets()

    _run_npm(["install"], prefix=prefix)
    _run_npm(["run", "build"], prefix=prefix)

    _compile_assets()

    echo_success("Assets built successfully.")


@assets.command()
@prefix_option
def dev(prefix):
    """Build all static assets for use in development.

    This will install all missing frontend dependencies and then run webpack to build
    all asset bundles.
    """
    _clean_assets()

    _run_npm(["install"], prefix=prefix)
    _run_npm(["run", "dev"], prefix=prefix)

    echo_success("Assets built successfully.")


@assets.command()
@prefix_option
def watch(prefix):
    """Build and watch all static assets for use in development.

    This will install all missing frontend dependencies and then run webpack to build
    and watch all asset bundles.
    """
    _clean_assets()

    _run_npm(["install"], prefix=prefix)
    _run_npm(["run", "watch"], prefix=prefix)


def _run_npm(args, prefix):
    if not shutil.which("npm"):
        echo_danger("'npm' not found in PATH, maybe Node.js is not installed?")
        sys.exit(1)

    if prefix is not None:
        prefix = ["--prefix", prefix]
    else:
        prefix = []

    run_command(["npm"] + args + prefix)


# The following code is a slightly modified version of flask-static-digest's core
# functionality, which is licensed under the MIT license and available at:
#
# https://github.com/nickjj/flask-static-digest/tree/v0.4.1
#
# The MIT License (MIT)
#
# Copyright (c) 2019 Nick Janetakis
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# 'Software'), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# Also takes files into account that have already been hashed via webpack.
def _is_compiled_file(filepath):
    return re.search(r"-[a-f\d]{32}", os.path.basename(filepath))


def _skip_file(filepath):
    return (
        _is_compiled_file(filepath)
        or re.search(r"\.(ttf|woff2?)$", filepath)
        or filepath.endswith(".LICENSE.txt")
    )


def _compile_assets():
    static_path = current_app.static_folder
    search_path = os.path.join(static_path, "**", "*")

    # Collect all static files to "compile".
    files = []

    for item in glob.iglob(search_path, recursive=True):
        if os.path.isfile(item) and not _skip_file(item):
            files.append(item)

    # Generate the manifest, which maps the original files to their compiled
    # counterpart.
    manifest = {}

    for filepath in files:
        rel_filepath = os.path.relpath(filepath, static_path).replace("\\", "/")
        filename, file_extension = os.path.splitext(rel_filepath)

        with open(filepath, mode="rb") as f:
            digest = hash_value(f.read(), alg="md5")

        digested_filepath = f"{filename}-{digest}{file_extension}"
        manifest[rel_filepath] = digested_filepath

        # Copy the file while preserving permissions and metadata, if supported.
        full_digested_filepath = os.path.join(static_path, digested_filepath)
        shutil.copy2(filepath, full_digested_filepath)

    # Finally, save the manifest in a file.
    with open(current_app.config["MANIFEST_PATH"], mode="w", encoding="utf-8") as f:
        f.write(compact_json(manifest))


def _clean_assets():
    search_path = os.path.join(current_app.static_folder, "**", "*")

    for item in glob.iglob(search_path, recursive=True):
        if os.path.isfile(item) and _is_compiled_file(item):
            os.remove(item)

    try:
        os.remove(current_app.config["MANIFEST_PATH"])
    except FileNotFoundError:
        pass
