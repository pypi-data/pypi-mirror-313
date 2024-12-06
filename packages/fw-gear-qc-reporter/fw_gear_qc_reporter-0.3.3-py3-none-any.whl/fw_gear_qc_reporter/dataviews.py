import copy
import itertools
import logging

import backoff
import pandas as pd
from fw_client import FWClient
from fw_utils import AttrDict

log = logging.getLogger(__name__)

AVAILABLE_LEVELS = ["subject", "session", "acquisition"]

COLUMNS = {
    "file.file_id": "file_id",
    "file.version": "version",
    "file.name": "filename",
    "subject.label": "subject_label",
    "session.label": "session_label",
    "acquisition.label": "acquisition_label",
    "analysis.label": "analysis_label",
    "session.url": "session_url",
    "file.info": "qc",
}

DATAVIEW_TEMPLATE = {
    "parent": "",
    "label": "",
    "description": "",
    "columns": [],
    "fileSpec": {
        "container": "",
        "filter": {"regex": False, "value": "*"},
        "match": "all",
        "processFiles": False,
        "analysisFilter": {
            "label": {"regex": False, "value": "*"},
        },
    },
    "filter": "",
    "includeIds": False,
    "includeLabels": False,
    "errorColumn": False,
    "missingDataStrategy": "none",
    "sort": False,
    "origin": {"type": "user", "id": ""},
}


async def launch_dataview(
    client: FWClient,
    container: str,
    top_level: str,
    analyses: bool = False,
    level: str = "acquisition",
) -> AttrDict:
    """Launch dataview on given container at given level.

    Args:
        client: API client
        container (str): Container ID.
        top_level: Top level namespace to look for QC info in.
        analyses (bool, optional): Include analyses. Defaults to False.
        level (str, optional): File level to gather. Defaults to "acquisition".

    Returns:
        AttrDict: Dataview Execution object.
    """
    if level not in AVAILABLE_LEVELS:
        raise RuntimeError()
    exclude = []
    if not analyses:
        exclude.append("analysis.label")
    if level == "subject":
        exclude.extend(["session.label", "acquisition.label", "session.url"])
    elif level == "session":
        exclude.append("acquisition.label")

    columns = []
    for k, v in COLUMNS.items():
        col = k
        if k == "file.info":
            col += f".{top_level}"
        if k not in exclude:
            columns.append({"src": col, "dst": v})

    user = client.get("/api/users/self")
    dataview = copy.deepcopy(DATAVIEW_TEMPLATE)
    dataview["columns"] = columns
    dataview["parent"] = container
    dataview["fileSpec"]["container"] = level
    if not analyses:
        del dataview["fileSpec"]["analysisFilter"]
    dataview["origin"]["id"] = user.user_id
    res = client.post(
        "/api/views/queue", params={"containerId": container}, json=dataview
    )
    return res


@backoff.on_predicate(
    backoff.fibo, lambda x: x.state not in ["completed", "failed"], max_time=200
)
async def poll_dataview(client, execution_id: str) -> AttrDict:
    """Poll a dataview until it finishes (either completed or failed)."""
    return client.get(f"/api/data_view_executions/{execution_id}")


async def get_dataview(
    client: FWClient, top_level: str, params: dict, dv_num: int
) -> pd.DataFrame:
    """Run a dataview and return data as a DataFrame.

    Args:
        client: Flywheel API client
        top_level: Top level namespace to look for QC info in.
        params: Dataview parameters
        dv_num: Dataview number for logging purposes.

    Raises:
        RuntimeError: If dataview execution fails

    Returns:
        pd.DataFrame: Dataview data as a pandas Dataframe
    """
    log.info(f"Dataview {dv_num} -- Launching.")
    dv = await launch_dataview(client, params.pop("container"), top_level, **params)
    res = await poll_dataview(client, dv._id)
    if res.state == "completed":
        log.info(f"Dataview {dv_num} -- done, downloading data.")
        data = client.get(f"/api/data_view_executions/{dv._id}/data")
        log.info(f"Dataview {dv_num} -- data downloaded.")
        df = pd.DataFrame(data=data["data"])
        return df
    else:
        raise RuntimeError("Dataview failed")


def generate_params(config: dict, destination: dict):
    if config["intermediates"]:
        dest = destination["type"]
        hierarchy = AVAILABLE_LEVELS.copy()
        if dest in AVAILABLE_LEVELS:
            hierarchy = AVAILABLE_LEVELS[AVAILABLE_LEVELS.index(dest) :]
        if config["include_analyses"]:
            hierarchy = itertools.product(hierarchy, [True, False])
        else:
            hierarchy = [(h, False) for h in hierarchy]
        return [
            {
                "container": destination["id"],
                "analyses": analyses,
                "level": level,
            }
            for level, analyses in hierarchy
        ]
    else:
        # Only do one dataview at acquisition level
        return [
            {
                "container": destination["id"],
                "analyses": False,
                "level": "acquisition",
            }
        ]
