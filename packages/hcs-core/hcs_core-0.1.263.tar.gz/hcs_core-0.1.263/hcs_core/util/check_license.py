"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

#!/usr/bin/env -S python3 -W ignore

import os
import sys

license_header = """'''
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
""".splitlines()

_hint = sum(len(s) for s in license_header) + 7
_fix = len(sys.argv) == 2 and sys.argv[1] == "--fix"


def _process_file(file_path):
    compliant, fixable = _check_file_license(file_path)
    if compliant:
        return

    if not _fix or not fixable:
        print("ERROR", file_path)
        sys.exit(1)

    print("Updating file", file_path)
    with open(file_path, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        for line in license_header:
            f.write(line + "\n")
        f.write(content)


def _check_file_license(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines(_hint)
        if len(lines) == 0:
            return True, False

        fixable = lines[0][0] != "#"
        if len(lines) < len(license_header):
            return False, fixable

        for i in range(len(license_header)):
            if lines[i].strip() != license_header[i]:
                return False, fixable
    return True, False


if __name__ == "__main__":
    for root, subdirs, files in os.walk("."):
        for filename in files:
            if not filename.endswith(".py"):
                continue
            file_path = os.path.join(root, filename)
            _process_file(file_path)
