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

from copy import deepcopy
import time
import threading
from graphlib import TopologicalSorter
from graphviz import Digraph
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable
from .helper import PlanException
from hcs_core.ctxp import data_util
from hcs_core.util import exit


class walker:
    next = "next"
    stop = "stop"


class _NodeType:
    var = "var"
    env = "env"
    const = "const"
    provider = "provider"
    resource = "resource"
    runtime = "runtime"


class DAG:
    graph: dict[str, set[str]]
    data: dict[str, Any]

    def __init__(self):
        self.graph = {}
        self.data = {}
        self.extra_source = []

    def add(self, id: str, type: str, data: Any, dependencies=None):
        if id in self.data:
            raise PlanException("Node already added to graph: " + id)
        self.data[id] = {"type": type, "data": data, "ghost": False}
        self.graph[id] = set(dependencies) if dependencies else set()

    def validate(self, extra):
        all_keys = self.data.keys()
        for k, v in self.graph.items():
            for d in v:
                if d in all_keys:
                    continue
                if d in extra:
                    continue
                raise PlanException(f"Blueprint error: target dpendency not found: from={k}, target={d}")


def process_blueprint(
    blueprint,
    fn_process_node: Callable,
    continue_on_error: bool = False,
    reverse: bool = False,
    concurrency: int = 3,
    target_node_name: str = None,
    include_dependencies: bool = True,
):
    dag = _build_graph(blueprint, reverse, target_node_name, include_dependencies)

    def fn_process_node_impl(name: str):
        if name.startswith("priority/"):
            actual_name = name[len("priority/") :]
            return fn_process_node(actual_name)
        if dag.data[name]["ghost"]:
            return walker.next
        return fn_process_node(name)

    return _walkthrough(dag, fn_process_node_impl, continue_on_error, concurrency)


def _filter_dag_by_target_node(dag: DAG, target_node_name, include_dependencies):
    if include_dependencies:
        # Remove all nodes that are not dependencies (both direct and indirect) of the target
        all_nodes = set(dag.graph.keys())
        dependencies = set()
        dependencies.add(target_node_name)
        open_nodes = set(dag.graph[target_node_name])
        while open_nodes:
            n = open_nodes.pop()
            if n in dependencies:
                continue
            dependencies.add(n)
            open_nodes |= dag.graph[n]

        to_delete = all_nodes - dependencies
        for n in to_delete:
            del dag.graph[n]
            del dag.data[n]
    else:
        # keep only the target node
        dag.data = {target_node_name: dag.data[target_node_name]}
        dag.graph = {target_node_name: set()}
    pass


def _build_graph(blueprint, reverse: bool, target_node_name: str, include_dependencies: bool):
    dag = DAG()
    extra = blueprint.keys()

    def add_node(name, type, obj):
        dependencies = set()

        # identify dependencies due to variables
        variables = data_util.deep_find_variables(obj)
        for v in variables:
            i = v.find(".")
            resource_name = v if i < 0 else v[:i]
            if resource_name == "var":
                continue  # ignore dependencies to var, which is a common thing.
            dependencies.add(resource_name)

        # identify dependencies due to explicit "after" statement
        after = obj.get("after")
        if after:

            def _add(t):
                if t in dependencies:
                    raise PlanException(
                        f"Invalid blueprint: statement after contains a dependency that is already implicitly created. This is not necessary. Resource: {name}, unexpected after-key: {t}"
                    )
                dependencies.add(t)

            if isinstance(after, str):
                _add(after)
            else:
                for v in after:
                    _add(v)

        # identify dependencies due to provider
        if type == _NodeType.resource:
            provider_type = _get_provider_id(obj)
            dependencies.add(provider_type)
        dag.add(name, type, obj, dependencies)

    required_providers = set()
    for k, v in blueprint["runtime"].items():
        add_node(k, _NodeType.runtime, v)
    for k, v in blueprint["resource"].items():
        required_providers.add(_get_provider_id(v))
        add_node(k, _NodeType.resource, v)
    default = blueprint["default"]
    if default:
        add_node("default", _NodeType.const, default)
    var = blueprint["var"]
    if var:
        add_node("var", _NodeType.var, var)
    providers = blueprint["provider"]
    if providers:
        for provider_id, data in providers.items():
            add_node(provider_id, _NodeType.provider, data)
    # Provider config is optional. Add place-holder nodes for all missing providers.
    for provider_id in required_providers:
        if provider_id not in dag.data:
            add_node(provider_id, _NodeType.provider, {})

    dag.validate(extra)

    if reverse:
        _reverse_dag(dag)
        _handle_priority_override(blueprint, dag)

    if target_node_name:
        _filter_dag_by_target_node(dag, target_node_name, include_dependencies)

    return dag


def _handle_priority_override(blueprint, dag):
    priority_list = []
    for k, v in blueprint["runtime"].items():
        p = v.get("destroyPriority")
        if p is not None:
            priority_list.append({"priority": p, "name": k, "data": v})

    if not priority_list:
        return

    list.sort(priority_list, key=lambda i: i["priority"])

    leaves = []
    for k, v in dag.graph.items():
        if not v:
            leaves.append(k)

    last_priority = None
    for i in priority_list:
        dependencies = [last_priority] if last_priority else []
        name = "priority/" + i["name"]
        dag.add(name, _NodeType.runtime, i["data"], dependencies)
        last_priority = name
        dag.data[i["name"]]["ghost"] = True

    for leaf in leaves:
        dag.graph[leaf].add(last_priority)


def _get_provider_id(node_data):
    kind = node_data["kind"]
    provider_type = kind[: kind.find("/")]
    if provider_type == "runtime":
        raise PlanException("This is a regression bug. Must not be runtime here")
    return provider_type


def _walkthrough(dag: DAG, fn_process_node: Callable, continue_on_error: bool, concurrency: int):
    topological_sorter = TopologicalSorter(dag.graph)
    topological_sorter.prepare()
    lock = threading.Lock()

    flag_stop = threading.Event()

    flags = {"err": None}

    def process_node(node_id):
        try:
            if flag_stop.is_set() or exit.is_set():
                return
            ret = fn_process_node(node_id)
            with lock:
                if ret == walker.stop:
                    flag_stop.set()
                topological_sorter.done(node_id)
        except KeyboardInterrupt as e:
            with lock:
                flags["err"] = e
            exit.set()
        except Exception as e:
            with lock:
                flags["err"] = e
                if continue_on_error:
                    topological_sorter.done(node_id)
                else:
                    flag_stop.set()
        except SystemExit as e:
            with lock:
                flags["err"] = e
            exit.set()

    # with ThreadPoolExecutor(max_workers=concurrency, thread_name_prefix="dag-walker") as executor:

    #     def close():
    #         flag_stop.set()
    #         executor.shutdown(wait=False, cancel_futures=True)

    #     atexit.register(close)

    #     while topological_sorter.is_active():
    #         if flag_stop.is_set():
    #             break
    #         with lock:
    #             if not continue_on_error and flags["err"]:
    #                 break
    #             read_nodes = topological_sorter.get_ready()
    #         if not len(read_nodes):
    #             time.sleep(0.1)
    #             continue
    #         for node in read_nodes:
    #             executor.submit(process_node, node)
    #     executor.shutdown(wait=True)
    #     if flags["err"]:
    #         raise flags["err"]

    #     atexit.unregister(close)

    try:
        executor = ThreadPoolExecutor(max_workers=concurrency, thread_name_prefix="dag-walker")

        while topological_sorter.is_active():
            if flag_stop.is_set():
                break
            with lock:
                if not continue_on_error and flags["err"]:
                    break
                read_nodes = topological_sorter.get_ready()
            if not len(read_nodes):
                time.sleep(0.1)
                continue
            for node in read_nodes:
                executor.submit(process_node, node)
    except KeyboardInterrupt as e:
        exit.set()
        raise e
    except Exception as e:
        flag_stop.set()
        raise e
    finally:
        executor.shutdown(wait=False)
        ex = flags["err"]
        if ex:
            raise ex  # pylint: disable=raising-bad-type


def _has_indirect_dependency(tree: dict, from_node: str, to_node: str):
    deps = list(tree[from_node])
    deps.remove(to_node)
    while deps:
        n = deps.pop()
        new_deps = tree[n]
        if to_node in new_deps:
            return True
        deps += new_deps
    return False


def graph(blueprint: dict, state: dict, reverse: bool, target_resource: str, include_dependencies: bool) -> Digraph:
    dag = _build_graph(blueprint, reverse, target_resource, include_dependencies)
    topological_sorter = TopologicalSorter(dag.graph)
    sorted_nodes = list(topological_sorter.static_order())
    graph = Digraph(name=f"Deployment {blueprint['deploymentId']}", comment="Simplified")

    class styles:
        deployed = {"style": "filled", "fillcolor": "lightgrey"}

    # https://graphviz.org/doc/info/shapes.html#:~:text=There%20are%20three%20main%20types,and%20an%20HTML%2Dlike%20label.
    node_type_style_map = {
        _NodeType.const: {"shape": "tab"},
        _NodeType.provider: {"shape": "component"},
        _NodeType.resource: {
            # empty
        },
        _NodeType.var: {"shape": "note"},
        _NodeType.runtime: {"shape": "hexagon"},
    }
    GHOST = {"style": "dashed"}

    def _is_deployed(node_name):
        data = state["output"].get(node_name)
        if isinstance(data, list):
            return any(d for d in data)
        return data

    def _get_node_style(node_name):
        n = dag.data[node_name]
        attr = {} | node_type_style_map[n["type"]]
        if n["ghost"]:
            attr |= GHOST

        if _is_deployed(node_name):
            attr |= styles.deployed
        return attr

    for node in sorted_nodes:
        attrs = _get_node_style(node)
        graph.node(node, **attrs)

    # Add the edges based on the dependencies
    for node, dependencies in dag.graph.items():
        for dependency in dependencies:
            if _has_indirect_dependency(dag.graph, from_node=node, to_node=dependency):
                continue  # simplify the diagram by removing ommitable
            graph.edge(dependency, node)

    return graph


def _reverse_dag(dag: DAG):
    old_dep = deepcopy(dag.graph)
    dag.graph = {}
    for k, h in old_dep.items():
        dag.graph[k] = set()

    def add_dep(from_node: str, to_node: str):
        holder = dag.graph[from_node]
        holder.add(to_node)

    for k, h in old_dep.items():
        for t in h:
            if t in old_dep:
                add_dep(t, k)
            else:
                # This is an external dependency and not part of our node
                pass


def _test(reverse):
    print("reverse=", reverse)
    dag = DAG()
    dag.add("a", "a", None)
    dag.add("b1", "b1", {"a"})
    dag.add("b2", "b2", {"a"})
    dag.add("c", "c", {"b1"})
    dag.add("d", "d", {"b2", "c"})

    if reverse:
        _reverse_dag(dag)

    def fn_proc(id):
        print("-> ", id)
        print("sleeping", id)
        time.sleep(2)
        print("<- ", id)

    _walkthrough(dag, fn_proc, False, 3)
    print("exit")


if __name__ == "__main__":
    _test(False)
    _test(True)
