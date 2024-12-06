from __future__ import annotations

import json
import tarfile
import typing
from base64 import b64decode
from datetime import datetime
from io import BytesIO
from typing import Any

from digitalhub.entities._commons.enums import State
from digitalhub.utils.logger import LOGGER

from digitalhub_runtime_kfp.dsl import LABEL_PREFIX

if typing.TYPE_CHECKING:
    from kfp import Client
    from kfp_server_api.models import ApiRunDetail


def map_state(state: str) -> str:
    """
    Map KFP state to digitalhub state.

    Parameters
    ----------
    state : str
        KFP state.

    Returns
    -------
    str
        Mapped digitalhub state.
    """
    kfp_states = {
        "Succeeded": State.COMPLETED.value,
        "Failed": State.ERROR.value,
        "Running": State.RUNNING.value,
        "Pending": State.PENDING.value,
        "Skipped": State.STOP.value,
        "Error": State.ERROR.value,
    }
    return kfp_states.get(state, State.ERROR.value)


def build_status(
    build: dict | None = None,
    execution_results: ApiRunDetail | None = None,
    client: Client | None = None,
) -> dict:
    """
    Collect outputs.

    Parameters
    ----------
    execution_results : ApiRun
        KFP Execution results.
    client: Client
        reference to the KFP API client

    """
    try:
        if build is not None:
            return {"results": build}
        return {
            "state": map_state(execution_results.run.status),
            "results": _convert_run(execution_results, client),
        }
    except Exception as e:
        msg = f"Something got wrong during run status building. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg) from e


def _convert_run(run_detail: ApiRunDetail, client: Client) -> dict:
    """
    Convert run to dict.

    Parameters
    ----------
    run : ApiRunDetail
        KFP run.
    client: Client
        reference to the KFP API client.

    Returns
    -------
    dict
        Run dict.
    """
    try:
        manifest_json = run_detail.pipeline_runtime.to_dict()["workflow_manifest"]
        manifest = json.loads(manifest_json)
        result = {}
        result["metadata"] = {
            "name": manifest["metadata"]["name"],
            "uid": manifest["metadata"]["uid"],
            "resourceVersion": manifest["metadata"]["resourceVersion"],
            "creationTimestamp": manifest["metadata"]["creationTimestamp"],
            "labels": manifest["metadata"]["labels"],
            "annotations": manifest["metadata"]["annotations"],
        }
        try:
            nodes = manifest["status"]["nodes"]
        except KeyError:
            nodes = {}
        graph_nodes = []
        for id, node in nodes.items():
            graph_nodes.append(_node_to_graph(id, run_detail, node, manifest["spec"]["templates"], client))
        result["status"] = {
            "start_time": manifest["status"].get("startedAt"),
            "end_time": manifest["status"].get("finishedAt"),
            "last_update": datetime.now().isoformat(),
            "progress": manifest["status"].get("progress"),
            "graph": graph_nodes,
        }
        return result
    except Exception as e:
        msg = f"Something got wrong during run conversion. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg) from e


def _node_to_graph(id: str, run_detail: ApiRunDetail, node: dict, templates: list, client: Client) -> dict:
    """
    Convert node to graph.

    Parameters
    ----------
    id : str
        Node id.
    run_detail : ApiRun
        KFP run.
    node : dict
        KFP node.
    templates : list
        KFP templates.
    client: Client
        reference to the KFP API client.

    Returns
    -------
    dict
        Graph dict.
    """
    res = {
        "id": id,
        "name": node["name"],
        "display_name": node["displayName"],
        "type": node["type"],
        "children": node["children"] if "children" in node else [],
    }
    if "phase" in node:
        res["state"] = node["phase"]
    if "startedAt" in node:
        res["start_time"] = node["startedAt"]
    if "finishedAt" in node:
        res["end_time"] = node["finishedAt"]
    if "exit_code" in node:
        res["exit_code"] = node["exit_code"]
    try:
        if "inputs" in node:
            res["inputs"] = _process_params(node["inputs"])
        if "outputs" in node:
            res["outputs"] = _process_params(node["outputs"])
    except Exception as e:
        LOGGER.warning("Could not process values: %s", e)
        pass

    for template in templates:
        if "container" in template and template["name"] == node["displayName"]:
            labels = template["metadata"]["labels"] if "labels" in template["metadata"] else {}
            if LABEL_PREFIX + "function" in labels:
                res["function"] = labels[LABEL_PREFIX + "function"]
            if LABEL_PREFIX + "function_id" in labels:
                res["function_id"] = labels[LABEL_PREFIX + "function_id"]
            if LABEL_PREFIX + "action" in labels:
                res["action"] = labels[LABEL_PREFIX + "action"]

    # run_id
    if node["type"] == "Pod" and "outputs" in node:
        try:
            run_id_artifact = client.runs.read_artifact(
                run_detail.run.id,
                node["id"],
                f"{node['displayName']}-run_id",
                async_req=False,
            )
            res["run_id"] = _get_artifact_value(run_id_artifact.data)
        except Exception as e:
            LOGGER.warning("Could not get run_id artifact: %s", e)
    return res


def _process_params(params: dict) -> list:
    """
    Process params.

    Parameters
    ----------
    params : dict
        KFP params.

    Returns
    -------
    list
        Processed params.
    """
    res = []
    for param in params.get("parameters", []):
        res.append({"name": param["name"], "value": param.get("value", "")})
    return res


def _get_artifact_value(indata: Any) -> dict | str:
    """
    Get artifact value.

    Parameters
    ----------
    indata : str
        Artifact data.

    Returns
    -------
    dict
        Artifact value.
    """
    # Artifacts are returned as base64-encoded .tar.gz strings
    data = b64decode(indata)
    io_buffer = BytesIO()
    io_buffer.write(data)
    io_buffer.seek(0)

    # Unpack the tarball
    with tarfile.open(fileobj=io_buffer) as tar:
        member_names = tar.getnames()
        if len(member_names) == 1:
            members = tar.extractfile(member_names[0]).read().decode("utf-8")
        else:
            members = {}
            for member_name in member_names:
                members[member_name] = tar.extractfile(member_name).read().decode("utf-8")
    return members
