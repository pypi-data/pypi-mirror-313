import pandas as pd
import requests
import json
import re
import subprocess

from nemo_library.sub_connection_handler import connection_get_headers
from nemo_library.sub_config_handler import ConfigHandler
from nemo_library.sub_symbols import ENDPOINT_URL_PERSISTENCE_METADATA_ATTRIBUTE_GROUPS, ENDPOINT_URL_PERSISTENCE_METADATA_IMPORTED_COLUMNS, RESERVED_KEYWORDS


MINIMUM_INFOZOOM_VERSION = "9.80.0"


def synchMetadataWithFocus(config: ConfigHandler, metadatafile: str, projectId: str):
    """
    Synchronizes metadata from a given CSV file with the NEMO project metadata.

    This method reads metadata from a CSV file, processes it, and synchronizes it with
    the metadata of a specified NEMO project. It handles the creation of groups first
    and then processes individual attributes.

    Args:
        config (ConfigHandler): Configuration handler instance to retrieve configuration details.
        metadatafile (str): Path to the CSV file containing metadata.
        projectId (str): The ID of the NEMO project to synchronize with.

    Raises:
        Exception: If any request to the NEMO API fails or if an unexpected error occurs.
    """
    try:

        # headers for all requests
        headers = connection_get_headers(config)

        # read meta data from fox file
        foxmetadata = getFOXMetaData(metadatafile=metadatafile)

        # Filter rows where Definition is 'Gruppe' and create groups first
        foxmetadata_groups = foxmetadata[foxmetadata["Definition"] == "Gruppe"]
        process_groups(config, foxmetadata_groups, headers, projectId)


        # get meta data from NEMO project
        dfMetaNEMO_imported_columns = getNEMOMetaData_imported_columns(config=config, projectId=projectId)
        dfMetaNEMO_attribute_groups = getNEMOMetaData_attribute_groups(config=config, projectId=projectId)

        # process attributes
        previous_attr = None
        ignored_attributes = []
        
        for idx, row in foxmetadata.iterrows():

            print(
                "processing attibute",
                idx,
                row["Attributname"],
                "type:",
                row["Definition"],
            )

            # handle different row types
            match row["Definition"]:
                case 'Einfaches Attribut':
                    internal_name = convert_internal_name(name=row["Importname"])
                    meta = dfMetaNEMO_imported_columns[dfMetaNEMO_imported_columns["internalName"] == internal_name]
                case "Gruppe":
                    internal_name = convert_internal_name(name=row["Attributname"])
                    meta = dfMetaNEMO_attribute_groups[dfMetaNEMO_attribute_groups["internalName"] == internal_name]
                case _:
                    ignored_attributes.append((row["Attributname"], row["Definition"]))
                    internal_name = None
                    
            if internal_name:
                if len(meta) == 0:
                    print(
                        f"could not find attribute {internal_name}  in meta data!"
                    )
                else:
                    if len(meta) > 1:
                        print(
                            "multiple matches of attribute "
                            + internal_name
                            + " in meta data. Type : "
                            + row["Definition"]
                            + ". First one will be selected"
                        )
                    first_meta = meta.iloc[0]
                    source_id_meta = first_meta["id"]

                    if pd.isna(row["Enthalten in Gruppe"]):
                        group_name = None
                    else:
                        group_name = convert_internal_name(row["Enthalten in Gruppe"])

                    # lets move the attribute now
                    api_url = (
                        config.config_get_nemo_url()
                        + f"/api/nemo-persistence/metadata/AttributeTree/projects/{projectId}/attributes/move"
                    )
                    payload = {
                        "sourceAttributes": [source_id_meta],
                        "targetPreviousElementId": previous_attr,
                        "groupInternalName": group_name,
                    }

                    response = requests.put(api_url, headers=headers, json=payload)
                    if response.status_code != 204:
                        raise Exception(
                            f"request failed. Status: {response.status_code}, error: {response.text}"
                        )

                    previous_attr = source_id_meta

        if ignored_attributes:
            print("Ignored attributes due to unsupported types:")
            for attr, definition in ignored_attributes:
                print(
                    f" - attribute {attr} ignored, due to unsupported type {definition}"
                )

    except Exception as e:
        raise Exception(f"process aborted: {str(e)}")


def getFOXMetaData(metadatafile: str) -> pd.DataFrame:
    """
    Reads a CSV file containing FOX metadata and returns it as a pandas DataFrame.

    The CSV file should have the following columns:
    - Attribut
    - UUID
    - Attributname
    - Importname
    - Definition
    - Enthalten in Gruppe
    - Enthalten in Gruppe (mit UUID)

    The resulting DataFrame will have the "Attribut" column set as its index.

    Args:
        metadatafile (str): The path to the CSV file containing the FOX metadata.

    Returns:
        pd.DataFrame: A pandas DataFrame with the FOX metadata, indexed by the "Attribut" column.
    """
    foxmetadata = pd.read_csv(
        metadatafile,
        usecols=[
            "Attribut",
            "UUID",
            "Attributname",
            "Importname",
            "Definition",
            "Enthalten in Gruppe",
            "Enthalten in Gruppe (mit UUID)",
        ],
        delimiter=";",
        encoding="utf-8",
    )
    foxmetadata.set_index("Attribut", inplace=True)
    return foxmetadata


def getNEMOMetaData_imported_columns(config: ConfigHandler, projectId: str) -> pd.DataFrame:
    """
    Fetch metadata from a NEMO project and return it as a pandas DataFrame.

    Args:
        config (ConfigHandler): An instance of ConfigHandler containing configuration details.
        projectId (str): The ID of the project to fetch metadata for.

    Returns:
        pd.DataFrame: A DataFrame containing the normalized metadata.

    Raises:
        Exception: If the request to the NEMO API fails, an exception is raised with the status code and error message.

    """
    # headers for all requests
    headers = connection_get_headers(config)

    # read meta data from NEMO project
    response = requests.get(
        config.config_get_nemo_url()
        + ENDPOINT_URL_PERSISTENCE_METADATA_IMPORTED_COLUMNS.format(
            projectId=projectId
        ),
        headers=headers,
    )
    if response.status_code != 200:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )
    resultjs = json.loads(response.text)
    return pd.json_normalize(resultjs)


def getNEMOMetaData_attribute_groups(config: ConfigHandler, projectId: str) -> pd.DataFrame:
    """
    Fetch metadata from a NEMO project and return it as a pandas DataFrame.

    Args:
        config (ConfigHandler): An instance of ConfigHandler containing configuration details.
        projectId (str): The ID of the project to fetch metadata for.

    Returns:
        pd.DataFrame: A DataFrame containing the normalized metadata.

    Raises:
        Exception: If the request to the NEMO API fails, an exception is raised with the status code and error message.

    """
    # headers for all requests
    headers = connection_get_headers(config)

    # read meta data from NEMO project
    response = requests.get(
        config.config_get_nemo_url()
        + ENDPOINT_URL_PERSISTENCE_METADATA_ATTRIBUTE_GROUPS.format(
            projectId=projectId
        ),
        headers=headers,
    )
    if response.status_code != 200:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )
    resultjs = json.loads(response.text)
    return pd.json_normalize(resultjs)


def convert_internal_name(name: str) -> str:
    """
    Converts a given string into a valid internal name by removing special characters,
    converting camelCase to snake_case, and ensuring it doesn't start with an underscore
    or conflict with SQL reserved keywords.

    Args:
        name (str): The original string to be converted.

    Returns:
        str: The converted internal name that adheres to the specified rules.

    Example:
        >>> convert_internal_name("SomeNameExample")
        'some_name_example'
    """

    # map german umlauts
    umlaut_map = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "Ä": "Ae",
        "Ö": "Oe",
        "Ü": "Ue",
        "ß": "ss",
    }

    internal_name = name
    for umlaut, ascii_rep in umlaut_map.items():
        internal_name = internal_name.replace(umlaut, ascii_rep)

    # Remove special chars and replace with unterscores
    pattern = r"[^a-zA-Z0-9_]+"
    internal_name = re.sub(pattern, "_", internal_name)

    # Use a regular expression to find lowercase characters followed by uppercase characters
    pattern = re.compile(r"([a-z])([A-Z]+)")

    # Use re.sub to insert an underscore between the matched groups
    internal_name = re.sub(pattern, r"\1_\2", internal_name)

    internal_name = internal_name.lower()

    # multiple underscores to one underscore
    internal_name = re.sub("_{2,}", "_", internal_name)

    if internal_name.startswith("_"):
        internal_name = internal_name[1:]

    # column must not be an sql keyword
    if internal_name in RESERVED_KEYWORDS:
        internal_name = f"name_{internal_name}"

    return internal_name


def process_groups(
    config: ConfigHandler,
    df,
    headers,
    projectId,
    current_group=None,
    parent_group_internal_name=None,
):
    """
    Recursively process groups starting from the root level.

    :param df: DataFrame containing the group information.
    :param headers: The headers for the API call.
    :param project_id: The project ID for the API call.
    :param current_group: The UUID of the current group to process. None indicates root level.
    :param parent_group_uuid: UUID of the parent group, None indicates root level.
    :param level: The current level in the hierarchy.
    """
    if current_group is None:
        
        # remove existing groups first
        attributegroups = getNEMOMetaData_attribute_groups(config=config,projectId=projectId)
        for index, row in attributegroups.iterrows():
            print("delete attribute group", row["internalName"])
            api_url = (
                config.config_get_nemo_url()
                + "/api/nemo-persistence/metadata/AttributeGroup/"
                + row["id"]
            )
            response = requests.delete(api_url, headers=headers)
            if response.status_code != 204:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )

        # create groups from scratch starting with root level
        root_groups = df[df["Enthalten in Gruppe (mit UUID)"].isna()]
        for index, row in root_groups.iterrows():
            nemo_group_internal_name = create_attribute_group(
                config,
                headers,
                projectId,
                row["Attributname"],
                parent_group_internal_name,
            )
            process_groups(
                config,
                df,
                headers,
                projectId,
                current_group=row["UUID"],
                parent_group_internal_name=nemo_group_internal_name,
            )
    else:
        # Process sub-groups contained in the current group
        sub_groups = df[
            df["Enthalten in Gruppe (mit UUID)"].str.contains(current_group, na=False)
        ]
        for index, row in sub_groups.iterrows():
            nemo_group_internal_name = create_attribute_group(
                config,
                headers,
                projectId,
                row["Attributname"],
                parent_group_internal_name,
            )
            process_groups(
                config,
                df,
                headers,
                projectId,
                current_group=row["UUID"],
                parent_group_internal_name=nemo_group_internal_name,
            )


def create_attribute_group(
    config: ConfigHandler, headers, project_id, group_name, parent_group_internal_name
) -> str:
    """
    Perform the desired action for each group by making an API call.

    :param headers: The headers for the API call.
    :param project_id: The project ID for the API call.
    :param group_name: Name of the current group.
    :param parent_group_internal_name: Internal name of the parent group.
    """

    api_url = (
        config.config_get_nemo_url() + "/api/nemo-persistence/metadata/AttributeGroup"
    )
    group_internal_name = convert_internal_name(group_name)
    payload = {
        "displayName": group_name,
        "displayNameTranslations": {
            "de": group_name  # Assuming 'en' is the default language
        },
        "internalName": group_internal_name,
        "parentAttributeGroupInternalName": parent_group_internal_name,
        "projectId": project_id,
    }

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 201:
        print(
            f"Successfully created group: {group_name} as child of {parent_group_internal_name}"
        )
        return group_internal_name
    else:
        print(
            f"Failed to create group: {group_name}. Status code: {response.status_code}, Error: {response.text}"
        )


def extract_version(log_file_path: str) -> str:
    """
    Extracts the version number from a log file.

    Args:
        log_file_path (str): The path to the log file.

    Returns:
        str: The extracted version number in the format "x.y.z".

    Raises:
        Exception: If the version information is not found in the log file.
    """
    with open(log_file_path, "r") as file:
        log_contents = file.read()

    version_pattern = re.compile(r"Version (\d+\.\d+\.\d+)")
    match = version_pattern.search(log_contents)

    if match:
        return match.group(1)
    else:
        raise Exception(f"Version information not found")


def is_version_at_least(version: str, minimum_version: str) -> bool:
    """
    Checks if a version number is at least a specified minimum version.

    Args:
        version (str): The version number to check.
        minimum_version (str): The minimum version number to compare against.

    Returns:
        bool: True if the version is at least the minimum version, False otherwise.
    """
    version_parts = list(map(int, version.split(".")))
    minimum_version_parts = list(map(int, minimum_version.split(".")))

    return version_parts >= minimum_version_parts


def exportMetadata(
    config: ConfigHandler, infozoomexe: str, infozoomfile: str, metadatafile: str
) -> None:
    """
    Exports metadata from an InfoZoom file using the InfoZoom executable.

    Args:
        config (ConfigHandler): Configuration handler object.
        infozoomexe (str): Path to the InfoZoom executable.
        infozoomfile (str): Path to the InfoZoom file.
        metadatafile (str): Path to the metadata output file.

    Returns:
        None

    Prints:
        str: Output messages including the execution status and version information.

    Raises:
        subprocess.CalledProcessError: If the command execution fails.
    """
    full_command = [
        infozoomexe,
        infozoomfile,
        "-invisible",
        "-metadata",
        "-UTF8",
        "-saveObjectsAsCSV",
        ";",
        metadatafile,
        "-exit",
    ]
    result = subprocess.run(full_command, shell=True, check=True)
    print("Command executed with return code:", result.returncode)
    log_file_path = "Log.txt"
    version = extract_version(log_file_path)
    print(f"version number found in {log_file_path}: {version}")
    if is_version_at_least(version, MINIMUM_INFOZOOM_VERSION):
        print(
            f"Version number {version} matches minimum version {MINIMUM_INFOZOOM_VERSION}"
        )
    else:
        raise Exception(
            f"Version {version} lower than minimum version {MINIMUM_INFOZOOM_VERSION}"
        )
