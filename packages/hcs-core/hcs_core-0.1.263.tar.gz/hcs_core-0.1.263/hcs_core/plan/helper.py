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

import json
import yaml
from typing import Tuple
import os
from hcs_core.ctxp.data_util import load_data_file, process_variables


class PlanException(Exception):
    pass


class PluginException(Exception):
    pass


class Blueprint:
    var: dict
    default: dict
    provider: dict
    resource: dict

    def __init__(self):
        self.var = {}
        self.default = {}
        self.provider = {}
        self.resource = {}

    def __repr__(self):
        return "Blueprint"


def load_files(files: list[str]) -> dict:
    ret = {}
    for file in files:
        data = load_data_file(file)
        if data is None or isinstance(data, str):
            raise FileNotFoundError("Fail loading file: " + file)
        ret = _merge_dict_fail_on_dup(ret, _smart_load_file(file))
    return ret


def process_template(template, use_env: bool = True) -> Tuple[dict, dict]:
    # Ensure default sections are not None
    if "var" not in template:
        template["var"] = {}
    if "default" not in template:
        template["default"] = {}
    if "resource" not in template:
        template["resource"] = {}
    if "runtime" not in template:
        template["runtime"] = {}
    if "provider" not in template:
        template["provider"] = {}

    _validate_blueprint(template)

    deployment_id = template["deploymentId"]
    if isinstance(deployment_id, int):
        template["deploymentId"] = str(deployment_id)
    elif isinstance(deployment_id, str):
        pass
    else:
        raise PlanException("Invalid deploymentId type. Expect string, actual: " + type(deployment_id).__name__)
    bp, pending = _materialize_blueprint(template, use_env)
    return bp, pending


def _validate_blueprint(blueprint: dict):
    _validate_required_keys(blueprint)
    _validate_resource_schema(blueprint)
    _validate_resource_id_not_conflict_to_reserved_names(blueprint)
    _validate_no_conflict_resource_id_provider_types_runtime_id(blueprint)
    _validate_statement_after(blueprint)


def _validate_required_keys(blueprint: dict):
    required_keys = ["deploymentId", "resource"]
    for k in required_keys:
        if k not in blueprint:
            raise PlanException("Missing required property in blueprint: " + k)


def _validate_resource_schema(blueprint: dict):
    resource = blueprint["resource"]
    if not resource:
        return
    required_keys = set(["kind"])
    optional_keys = set(["eta", "data", "conditions", "for", "after"])
    for k, v in resource.items():

        def _raise(reason):
            raise PlanException(f"Invalid blueprint: {reason}. Resource: {k}")

        actual_keys = set(v.keys())
        missed_keys = required_keys - actual_keys
        if missed_keys:
            _raise(f"Missing required keys: {missed_keys}")
        extra_keys = actual_keys - required_keys - optional_keys
        if extra_keys:
            _raise(f"Unknown extra keys: {extra_keys}")


def _get_duplicates(lst):
    return [item for item in set(lst) if lst.count(item) > 1]


def _validate_statement_after(blueprint: dict):
    def _raise(owner, reason):
        raise PlanException(f"Invalid statement: after. Owner={owner}, reason={reason}.")

    items = {}
    items |= blueprint["resource"]
    items |= blueprint["runtime"]

    def _validate_after(target_name, owner_resource_name):
        if not isinstance(target_name, str):
            _raise(owner_resource_name, f"Invalid value type: {type(target_name).__name__}")

        if target_name not in items:
            _raise(owner_resource_name, "Target not found: " + target_name)

    for k, v in items.items():
        after = v.get("after")
        if after:
            if isinstance(after, list):
                for a in after:
                    _validate_after(a, k)

                dup = _get_duplicates(after)
                if dup:
                    _raise(k, "Duplicated keys: " + dup)
            elif isinstance(after, str):
                _validate_after(after, k)
            else:
                _raise(k, "Invalid type, expect str or list, got: " + type(after).__name__)


def _validate_no_conflict_resource_id_provider_types_runtime_id(blueprint: dict):
    provider_names = set()
    runtime_names = set(blueprint["runtime"].keys())
    for v in blueprint["resource"].values():
        name, _ = v["kind"].split("/")
        provider_names.add(name)

    declared_provider_names = set(blueprint["provider"].keys())
    excessive = declared_provider_names - provider_names
    if excessive:
        raise PlanException(f"Invalid blueprint. Unused provider definition: {excessive}.")
    resource_names = set(blueprint["resource"].keys())
    conflict = provider_names & resource_names
    if conflict:
        raise PlanException(f"Invalid blueprint. Provider ID and resource ID conflict: {conflict}.")
    conflict = runtime_names & resource_names
    if conflict:
        raise PlanException(f"Invalid blueprint. Runtime ID and resource ID conflict: {conflict}.")
    conflict = provider_names & runtime_names
    if conflict:
        raise PlanException(f"Invalid blueprint. Provider ID and runtime ID conflict: {conflict}.")


def _validate_resource_id_not_conflict_to_reserved_names(blueprint: dict):
    reserved_names_for_state = ["result", "pending", "log", "destroy_output"]
    reserved_names_for_blueprint = ["default", "var", "env", "provider", "resource", "runtime"]
    reserved_names_for_function = ["profile", "context"]
    existing_names_top_level = blueprint.keys()
    reserved_names = set(
        [
            *existing_names_top_level,
            *reserved_names_for_blueprint,
            *reserved_names_for_state,
            *reserved_names_for_function,
        ]
    )
    for name in blueprint["resource"]:
        if name in reserved_names:
            raise PlanException("Invalid blueprint. Resource name conflicts to a reserved name: " + name)
    for name in blueprint["runtime"]:
        if name in reserved_names:
            raise PlanException("Invalid blueprint. Runtime name conflicts to a reserved name: " + name)
    for name in blueprint["provider"]:
        if name in reserved_names:
            raise PlanException("Invalid blueprint. Provider name conflicts to a reserved name: " + name)


def _smart_load_file(file: str):
    if not os.path.exists(file):
        raise Exception("File not found: " + file)
    if not os.path.isfile(file):
        raise Exception("Not a file: " + file)
    if file.endswith(".json"):
        with open(file, "r") as f:
            return json.load(f)
    elif file.endswith(".yaml") or file.endswith(".yml"):
        with open(file, "r") as f:
            return yaml.safe_load(f)
    else:
        raise Exception("Unknown file extention: " + file)


def _merge_dict_fail_on_dup(o1: dict, o2: dict) -> dict:
    ret = dict(o1)
    for k, v in o2.items():
        if k in o1:
            raise Exception("Fail processing file. Duplicated key found: " + k)
        ret[k] = v
    return ret


def _materialize_blueprint(template: dict, use_env: bool) -> Tuple[dict, dict]:
    ret = process_variables(template, None, use_env)
    return template, ret["pending"]
