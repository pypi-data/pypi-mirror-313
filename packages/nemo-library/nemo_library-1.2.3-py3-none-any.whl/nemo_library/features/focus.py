import logging
import re
import pandas as pd
import requests
import json

from nemo_library.features.config import Config
from nemo_library.features.projects import getProjectID
from nemo_library.utils.utils import log_error


def focusMoveAttributeBefore(
    config: Config,
    projectname: str,
    sourceDisplayName: str,
    targetDisplayName: str = None,
    groupInternalName: str = None,
) -> None:
    """
    Moves an attribute in the focus tree of a specified project, positioning it before a target attribute.

    Args:
        config (Config): Configuration object containing connection details and headers.
        projectname (str): The name of the project where the attribute will be moved.
        sourceDisplayName (str): The display name of the attribute to move.
        targetDisplayName (str, optional): The display name of the attribute before which the source will be positioned. Defaults to None.
        groupInternalName (str, optional): The internal name of the attribute group for grouping purposes. Defaults to None.

    Returns:
        None

    Raises:
        RuntimeError: If any HTTP request fails (non-200/204 status code) or if the source/target attributes are not found.

    Notes:
        - Fetches the project ID using `getProjectID`.
        - Retrieves the attribute tree for the project to locate the source and target attributes.
        - If the target display name is not provided, the source attribute is moved to the top of the group or tree.
        - Sends a PUT request to update the position of the source attribute in the attribute tree.
        - Logs errors and raises exceptions for failed requests or missing attributes.
    """
    
    headers = config.connection_get_headers()
    project_id = getProjectID(config, projectname)

    # load attribute tree
    response = requests.get(
        config.config_get_nemo_url()
        + "/api/nemo-persistence/focus/AttributeTree/projects/{projectId}/attributes".format(
            projectId=project_id
        ),
        headers=headers,
    )
    if response.status_code != 200:
        raise Exception(
            f"Request failed. Status: {response.status_code}, error: {response.text}"
        )

    resultjs = json.loads(response.text)
    df = pd.json_normalize(resultjs)

    # locate source and target object
    filtereddf = df[df["label"] == sourceDisplayName]
    if filtereddf.empty:
        log_error(f"could not find source column '{sourceDisplayName}' to move in focus")
    sourceid = filtereddf.iloc[0]["id"]

    if targetDisplayName:
        filtereddf = df[df["label"] == targetDisplayName]
        if filtereddf.empty:
            log_error(
                f"could not find target column '{targetDisplayName}' to move in focus"
            )
        targetid = filtereddf.iloc[0]["id"]
    else:
        targetid = ""

    # now move the attribute
    data = {
        "sourceAttributes": [sourceid],
        "targetPreviousElementId": targetid,
        "groupInternalName": groupInternalName,
    }

    response = requests.put(
        config.config_get_nemo_url()
        + "/api/nemo-persistence/metadata/AttributeTree/projects/{projectId}/attributes/move".format(
            projectId=project_id
        ),
        headers=headers,
        json=data,
    )

    if response.status_code != 204:
        raise Exception(
            f"Request failed. Status: {response.status_code}, error: {response.text}"
        )

