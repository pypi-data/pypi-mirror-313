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

import yaml
import os
from hcs_core.ctxp import profile, recent
from hcs_core.ctxp.jsondot import undot
from hcs_core.plan import PlanException


def load_plan(file):

    if not file:
        file = _try_locating_plan_file()
    else:
        if file.name:
            recent.set("plan-file", file.name)

    with file:
        payload = file.read()
    data = yaml.safe_load(payload)
    extra = {"profile": undot(profile.current(exclude_secret=True))}
    return data, extra


_valid_extensions = [".yml", ".yaml", ".json", ".plan.yml", ".plan.yaml", ".plan.json"]


def _is_valid_name(file_name: str) -> bool:
    file_name = file_name.lower()
    for ext in _valid_extensions:
        if file_name.endswith(ext):
            return True
    return False


def validate_plan_file(file: str):
    if not os.path.exists(file):
        raise PlanException("File not found: " + file)
    if not os.path.isfile(file):
        raise PlanException("Not a file: " + file)
    if not _is_valid_name(file):
        raise PlanException("Not a valid plan file name: " + file)


def _try_locating_plan_file():
    # first, if we have a file "used"
    file_name = recent.get("plan-file")
    if file_name:
        validate_plan_file(file_name)
    else:
        files = os.listdir()
        candidates = []
        for name in files:
            if _is_valid_name(name):
                if candidates:
                    raise PlanException(
                        "Multiple plan files exist. Use the --file parameter to specify a target plan file."
                    )
                candidates.append(name)
        if not candidates:
            raise PlanException("No plan yaml file found. Use the --file parameter to specify a target plan file.")
        file_name = candidates[0]
        recent.set("plan-file", file_name)
    return open(file_name, "rt")


def resource_output_to_display(item):
    if not item:
        return
    if isinstance(item, dict):
        _display = item.get("_display")
        if _display:
            return _display
        return f"{item.get('name')} ({item.get('id')})"
    if isinstance(item, list):
        return "[...]"
    return type(item).__name__
