#!/usr/bin/env python3
# Copyright 2021 The Pigweed Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Emulation of rm -rf out && cp -af in out."""

import logging
import os
import shutil
import sys

_LOG = logging.getLogger(__name__)

def remove_and_copy(src, dest):
    """Emulation of rm -rf out && cp -af in out."""
    if not os.path.exists(src):
        _LOG.error('No such file or directory.')
        return -1

    if os.path.exists(dest):
        if not os.access(dest, os.W_OK):
            # Attempt to make the file writable before deleting it.
            os.chmod(dest, stat.S_IWRITE)

        if os.path.isdir(dest):
            shutil.rmtree(dest, onerror=_on_error)
        else:
            os.unlink(dest)

    if os.path.isdir(src):
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest, follow_symlinks=False)
        if not os.path.exists(dest):
            _LOG.error('Error during copying procedure.')
            return -1

    return 0

def main():
    # Require exactly two arguments, source and destination.
    if (len(sys.argv) - 1) != 2:
        _LOG.error('Incorrect parameters provided.')
        return -1

    return remove_and_copy(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    sys.exit(main())
