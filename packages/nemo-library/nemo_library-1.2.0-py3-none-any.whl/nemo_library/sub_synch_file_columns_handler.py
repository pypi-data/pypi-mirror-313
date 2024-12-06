import requests
import pandas as pd
import json
import re

from nemo_library.sub_config_handler import ConfigHandler
from nemo_library.sub_connection_handler import connection_get_headers
from nemo_library.sub_project_handler import getProjectID
from nemo_library.sub_symbols import (
    ENDPOINT_URL_PERSISTENCE_METADATA_CREATE_IMPORTED_COLUMN,
    ENDPOINT_URL_PERSISTENCE_METADATA_IMPORTED_COLUMNS,
    RESERVED_KEYWORDS,
)


def synchronizeCsvColsAndImportedColumns(
    config: ConfigHandler,
    projectname: str,
    filename: str,
) -> None:
    """
    Synchronizes the columns in a CSV file with the imported columns in the project.

    This function reads the column names from the first line of a specified CSV file and compares
    them with the imported columns for a given project. If a column from the CSV is not found in 
    the list of imported columns, it creates a new record for that column in the system.

    Args:
        config (ConfigHandler): A configuration handler that provides tenant and project information.
        projectname (str): The name of the project for which the columns are being synchronized.
        filename (str): The path to the CSV file whose columns need to be synchronized.

    Returns:
        None: The function performs its operation without returning a value.

    Steps:
        1. Retrieves the project ID based on the given project name.
        2. Reads the first line of the CSV file to get the column names.
        3. Cleans the column names using a `clean_column_name` function.
        4. For each CSV column, checks if an entry exists in the imported columns DataFrame.
        5. If no record is found for a column, a new record is created and added to the system.
    """
    
    project_id = getProjectID(config, projectname)
    importedColumns = getImportedColumns(config,project_id)

    # Read the first line of the CSV file to get column names
    with open(filename, "r") as file:
        first_line = file.readline().strip()

    # Split the first line into a list of column names
    csv_column_names = first_line.split(";")

    # Check if a record exists in the DataFrame for each column
    for column_name in csv_column_names:
        displayName = column_name
        column_name = clean_column_name(
            column_name, RESERVED_KEYWORDS
        )  # Assuming you have the clean_column_name function from the previous script

        # Check if the record with internal_name equal to the column name exists
        if not importedColumns[importedColumns["internalName"] == column_name].empty:
            print(f"Record found for column '{column_name}' in the DataFrame.")
        else:
            print(
                f"******************************No record found for column '{column_name}' in the DataFrame."
            )
            new_importedColumn = {
                "id": "",
                "internalName": column_name,
                "displayName": displayName,
                "importName": displayName,
                "description": "",
                "dataType": "string",
                "categorialType": False,
                "businessEvent": False,
                "unit": "",
                "columnType": "ExportedColumn",
                "tenant": config.config_get_tenant(),
                "projectId": project_id,
            }

            createImportedColumn(
                config=config,
                importedColumn=new_importedColumn,
            )


def getImportedColumns(config: ConfigHandler, project_id: str) -> pd.DataFrame:
    """
    Retrieves imported column metadata for a specified project from the persistence layer and
    returns it as a pandas DataFrame.

    Args:
        config (ConfigHandler): A configuration handler object used to fetch necessary API
                                connection details like the base URL.
        project_id (str): The unique identifier of the project whose imported column
                          metadata is to be retrieved.

    Returns:
        pd.DataFrame: A DataFrame containing the imported column metadata for the given project.

    Raises:
        Exception: If the HTTP request fails or the project_id is None.
                   It will raise an exception with an appropriate error message.

    Example:
        df = getImportedColumns(config, '12345')
    """
    try:

        # initialize reqeust
        headers = connection_get_headers(config)
        response = requests.get(
            config.config_get_nemo_url()
            + ENDPOINT_URL_PERSISTENCE_METADATA_IMPORTED_COLUMNS.format(
                projectId=project_id
            ),
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(
                f"request failed. Status: {response.status_code}, error: {response.text}"
            )
        resultjs = json.loads(response.text)
        df = pd.json_normalize(resultjs)
        return df

    except Exception as e:
        if project_id == None:
            raise Exception("process stopped, no project_id available")
        raise Exception("process aborted")


def clean_column_name(column_name: str, reserved_keywords: str) -> str:
    """
    Cleans and normalizes a given CSV column name.

    This function processes a given column name by removing special characters,
    converting it to lowercase, and ensuring it doesn't start with a numeric
    character. It also handles reserved keywords by appending an underscore
    to avoid conflicts.

    Args:
        column_name (str): The original CSV column name to be cleaned.
        reserved_keywords (str): A set of reserved keywords that should not
                                 conflict with the cleaned column name.

    Returns:
        str: The cleaned and normalized column name. If the column name is empty,
             it returns "undefined_name". If the column starts with a number,
             "numeric_" is prefixed to the name. For single-character names or
             reserved keywords, an underscore is appended to the end.
    """

    # If csv column name is empty, return "undefined_name"
    if not column_name:
        return "undefined_name"

    # Replace all chars not matching regex [^a-zA-Z0-9_] with empty char
    cleaned_name = re.sub(r"[^a-zA-Z0-9_]", "", column_name)

    # Convert to lowercase
    cleaned_name = cleaned_name.lower()

    # If starts with a number, concatenate "numeric_" to the beginning
    if cleaned_name[0].isdigit():
        cleaned_name = "numeric_" + cleaned_name

    # Replace all double "_" chars with one "_"
    cleaned_name = re.sub(r"_{2,}", "_", cleaned_name)

    # If length of csv column name equals 1 or is a reserved keyword, concatenate "_" to the end
    if len(cleaned_name) == 1 or cleaned_name in reserved_keywords:
        cleaned_name += "_"

    return cleaned_name


def createImportedColumn(
    config: ConfigHandler,
    importedColumn: json,
) -> pd.DataFrame:
    """
    Creates an imported column in a project by sending a POST request to a specified
    persistence metadata endpoint, and returns the result as a pandas DataFrame.

    Args:
        config (ConfigHandler): An object containing configuration data, including the base URL
            for making the request and necessary headers.
        importedColumn (json): A JSON object representing the column data to be imported.

    Returns:
        pd.DataFrame: A pandas DataFrame representing the imported column data from the API response.

    Raises:
        Exception: If the request fails (any status code other than 201), or if any other
        error occurs during the process.
    """
    try:

        # initialize reqeust
        headers = connection_get_headers(config)
        response = requests.post(
            config.config_get_nemo_url()
            + ENDPOINT_URL_PERSISTENCE_METADATA_CREATE_IMPORTED_COLUMN,
            headers=headers,
            json=importedColumn,
        )
        if response.status_code != 201:
            raise Exception(
                f"request failed. Status: {response.status_code}, error: {response.text}"
            )
        resultjs = json.loads(response.text)
        df = pd.json_normalize(resultjs)
        return df

    except Exception as e:
        raise Exception("process aborted")
