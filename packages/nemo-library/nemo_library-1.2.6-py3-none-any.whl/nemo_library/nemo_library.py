import pandas as pd

from nemo_library.features.config import Config
from nemo_library.features.fileingestion import ReUploadFile
from nemo_library.features.focus import focusMoveAttributeBefore
from nemo_library.features.hubspot import FetchDealFromHubSpotAndUploadToNEMO
from nemo_library.features.migman import createProjectsForMigMan
from nemo_library.features.projects import (
    LoadReport,
    createImportedColumn,
    createOrUpdateReport,
    createOrUpdateRule,
    createProject,
    deleteProject,
    getImportedColumns,
    getProjectID,
    getProjectList,
    getProjectProperty,
    setProjectMetaData,
    synchronizeCsvColsAndImportedColumns,
)


class NemoLibrary:

    def __init__(
        self,
        environment=None,
        tenant=None,
        userid=None,
        password=None,
        hubspot_api_token=None,
        config_file="config.ini",
    ):

        self.config = Config(
            environment=environment,
            tenant=tenant,
            userid=userid,
            password=password,
            hubspot_api_token=hubspot_api_token,
            config_file=config_file,
        )

        super().__init__()

    def getProjectList(
        self,
    ) -> pd.DataFrame:
        """
        Fetches the list of projects from the NEMO API and returns it as a pandas DataFrame.
        Logs an error message if the API request fails.

        Args:
            <None>
        Returns:
            pandas.DataFrame: A DataFrame containing the normalized project data.

        Logs:
            Error: If the API request fails (e.g., non-200 status code).
        """
        
        return getProjectList(self.config)

    def getProjectID(self, projectname: str) -> str:
        """
        Retrieves the unique project ID for a given project name.

        Args:
            projectname (str): The name of the project for which to retrieve the ID.

        Returns:
            str: The unique identifier (ID) of the specified project.

        Raises:
            ValueError: If the project name cannot be uniquely identified in the project list.

        Notes:
            - This function relies on the `getProjectList` function to fetch the full project list.
            - If multiple or no entries match the given project name, an error is logged, and the first matching ID is returned.
        """
        return getProjectID(self.config, projectname)

    def getProjectProperty(self, projectname: str, propertyname: str) -> str:
        """
        Retrieves a specific property value of a given project from the server.

        Args:
            projectname (str): The name of the project for which the property is requested.
            propertyname (str): The name of the property to retrieve.

        Returns:
            str: The value of the specified property, with leading and trailing quotation marks removed.

        Raises:
            RuntimeError: If the request to fetch the project property fails (non-200 status code).

        Notes:
            - This function first fetches the project ID using the `getProjectID` function.
            - Constructs an endpoint URL using the project ID and property name.
            - Sends an HTTP GET request to fetch the property value.
            - Logs an error if the request fails and raises an exception.
        """
        return getProjectProperty(self.config, projectname, propertyname)

    def LoadReport(
        self,
        projectname: str,
        report_guid: str,
        max_pages=None,
    ) -> pd.DataFrame:
        """
        Loads a report from a specified project and returns the data as a Pandas DataFrame.

        Args:
            projectname (str): The name of the project from which to load the report.
            report_guid (str): The unique identifier (GUID) of the report to be loaded.
            max_pages (int, optional): Reserved for future use to limit the number of pages in the report.

        Returns:
            pd.DataFrame: The report data as a Pandas DataFrame.

        Raises:
            RuntimeError: If the report initialization or data download fails.
            ValueError: If the downloaded data cannot be processed into a DataFrame.

        Notes:
            - Fetches the project ID using `getProjectID`.
            - Sends an HTTP POST request to initialize the report and retrieve a CSV download URL.
            - Downloads the CSV file and converts it into a Pandas DataFrame.
            - Removes the `_RECORD_COUNT` column if present in the dataset.
            - Logs errors and raises exceptions for failed requests or data processing issues.
        """
        return LoadReport(self.config, projectname, report_guid, max_pages)

    def createProject(self, projectname: str, description: str) -> None:
        """
        Creates a new project with the specified name and description in the NEMO system.

        Args:
            projectname (str): The display name for the new project.
            description (str): A brief description of the project.

        Returns:
            None

        Raises:
            RuntimeError: If the HTTP POST request to create the project fails (non-201 status code).

        Notes:
            - Generates a table name for the project by converting the project name to uppercase,
            replacing invalid characters with underscores, and ensuring it starts with "PROJECT_".
            - Sends a POST request to the project creation endpoint with the required metadata.
            - Logs an error if the request fails and raises an exception.
        """
        return createProject(
            config=self.config, projectname=projectname, description=description
        )

    def setProjectMetaData(
        self,
        projectname: str,
        processid_column: str = None,
        processdate_column: str = None,
        corpcurr_value: str = None,
    ) -> None:
        """
        Updates metadata for a specific project, including process ID, process date, and corporate currency value.

        Args:
            projectname (str): The name of the project to update metadata for.
            processid_column (str, optional): The column name representing the process ID.
            processdate_column (str, optional): The column name representing the process date.
            corpcurr_value (str, optional): The corporate currency value to set.

        Returns:
            None

        Raises:
            RuntimeError: If the HTTP PUT request to update the metadata fails (non-200 status code).

        Notes:
            - Fetches the project ID using `getProjectID`.
            - Constructs a metadata payload based on the provided parameters.
            - Sends an HTTP PUT request to update the project's business process metadata.
            - Logs an error if the request fails and raises an exception.
        """
        setProjectMetaData(
            self.config,
            projectname,
            processid_column,
            processdate_column,
            corpcurr_value,
        )

    def deleteProject(self, projectname: str) -> None:
        """
        Deletes a specified project from the NEMO system.

        Args:
            projectname (str): The name of the project to delete.

        Returns:
            None

        Raises:
            RuntimeError: If the HTTP DELETE request to delete the project fails (non-204 status code).

        Notes:
            - Fetches the project ID using `getProjectID`.
            - Sends an HTTP DELETE request to the endpoint associated with the project's metadata.
            - Logs an error if the request fails and raises an exception.
        """
        deleteProject(self.config, projectname)

    def createProjectsForMigMan(
        self, projects: list[str] = None, proALPHA_project_status_file: str = None
    ) -> None:
        """
        Creates projects for MigMan based on a provided project list or a proALPHA project status file.

        Args:
            projects (list[str], optional): A list of project names to create. Defaults to None.
            proALPHA_project_status_file (str, optional): Path to a proALPHA migration status file 
                                                        to generate the project list. Defaults to None.

        Returns:
            None

        Raises:
            ValueError: If no projects are provided or the project list is empty.
            RuntimeError: If no matching files are found for a given project.

        Notes:
            - If `proALPHA_project_status_file` is provided, the project list is generated from the file.
            - Each project is processed by:
                - Finding matching files.
                - Sorting the files.
                - Extracting a postfix and processing each file using `process_file`.
            - Logs errors and exceptions if files are missing or the project list is invalid.
        """
        createProjectsForMigMan(
            self.config,
            projects=projects,
            proALPHA_project_status_file=proALPHA_project_status_file,
        )

    def getImportedColumns(self, projectname: str) -> pd.DataFrame:
        """
        Retrieves the imported columns for a specified project and returns them as a Pandas DataFrame.

        Args:
            projectname (str): The name of the project for which to retrieve imported columns.

        Returns:
            pd.DataFrame: A DataFrame containing metadata about the imported columns.

        Raises:
            RuntimeError: If the HTTP GET request to fetch the columns fails (non-200 status code).

        Notes:
            - Fetches the project ID using `getProjectID`.
            - Sends an HTTP GET request to retrieve column metadata for the specified project.
            - Parses the JSON response and converts it into a normalized Pandas DataFrame.
            - Logs errors and raises exceptions for failed requests or invalid responses.
        """
        return getImportedColumns(self.config, projectname)

    def createImportedColumn(
        self,
        projectname: str,
        displayName: str,
        dataType: str,
        importName: str = None,
        internalName: str = None,
        description: str = None,
    ) -> None:
        """
        Creates a new imported column for a specified project in the NEMO system.

        Args:
            projectname (str): The name of the project to which the column will be added.
            displayName (str): The display name of the column.
            dataType (str): The data type of the column (e.g., "String", "Integer").
            importName (str, optional): The name used for importing data into the column. Defaults to a sanitized version of `displayName`.
            internalName (str, optional): The internal system name of the column. Defaults to a sanitized version of `displayName`.
            description (str, optional): A description of the column. Defaults to an empty string.

        Returns:
            None

        Raises:
            RuntimeError: If the HTTP POST request to create the column fails (non-201 status code).

        Notes:
            - Generates `importName` and `internalName` from `displayName` if not explicitly provided.
            - Sends an HTTP POST request to the appropriate endpoint with metadata for the new column.
            - Logs and raises an exception if the request fails.
        """
        createImportedColumn(
            self.config,
            projectname,
            displayName,
            dataType,
            importName,
            internalName,
            description,
        )

    def ReUploadFile(
        self,
        projectname: str,
        filename: str,
        update_project_settings: bool = True,
        datasource_ids: list[dict] = None,
        global_fields_mapping: list[dict] = None,
        version: int = 2,
        trigger_only: bool = False,
    ) -> None:
        """
        Re-uploads a file to a specified project in the NEMO system and triggers data ingestion.

        Args:
            projectname (str): The name of the project to which the file will be uploaded.
            filename (str): The path to the file to upload.
            update_project_settings (bool, optional): Whether to trigger the "analyze_table" task after ingestion (version 2 only). Defaults to True.
            datasource_ids (list[dict], optional): Data source identifiers for version 3 ingestion. Defaults to None.
            global_fields_mapping (list[dict], optional): Field mappings for version 3 ingestion. Defaults to None.
            version (int, optional): The ingestion version (2 or 3). Defaults to 2.
            trigger_only (bool, optional): If True, skips waiting for task completion. Defaults to False.

        Returns:
            None

        Raises:
            Exception: If any step of the file upload, data ingestion, or subsequent tasks fails.

        Notes:
            - Compresses the file into gzip format before uploading.
            - Retrieves temporary AWS S3 credentials from NEMO's Token Vendor and uploads the file to S3.
            - Sends a request to ingest the uploaded data and optionally waits for task completion.
            - Triggers "analyze_table" task if version 2 and `update_project_settings` is True.
            - Logs and raises exceptions for any errors encountered during the process.
        """
        ReUploadFile(
            self.config,
            projectname,
            filename,
            update_project_settings,
            datasource_ids,
            global_fields_mapping,
            version,
            trigger_only,
        )

    def createOrUpdateReport(
        self,
        projectname: str,
        displayName: str,
        querySyntax: str,
        internalName: str = None,
        description: str = None,
    ) -> None:
        """
        Creates or updates a report in the specified project within the NEMO system.

        Args:
            projectname (str): The name of the project where the report will be created or updated.
            displayName (str): The display name of the report.
            querySyntax (str): The query syntax that defines the report's data.
            internalName (str, optional): The internal system name of the report. Defaults to a sanitized version of `displayName`.
            description (str, optional): A description of the report. Defaults to an empty string.

        Returns:
            None

        Raises:
            RuntimeError: If any HTTP request fails (non-200/201 status code).

        Notes:
            - Fetches the project ID using `getProjectID`.
            - Retrieves the list of existing reports in the project to check if the report already exists.
            - If the report exists, updates it with the new data using a PUT request.
            - If the report does not exist, creates a new report using a POST request.
            - Logs errors and raises exceptions for failed requests.
        """
        createOrUpdateReport(
            self.config,
            projectname,
            displayName,
            querySyntax,
            internalName,
            description,
        )

    def createOrUpdateRule(
        self,
        projectname: str,
        displayName: str,
        ruleSourceInternalName: str,
        internalName: str = None,
        ruleGroup: str = None,
        description: str = None,
    ) -> None:
        """
        Creates or updates a rule in the specified project within the NEMO system.

        Args:
            projectname (str): The name of the project where the rule will be created or updated.
            displayName (str): The display name of the rule.
            ruleSourceInternalName (str): The internal name of the rule source that the rule depends on.
            internalName (str, optional): The internal system name of the rule. Defaults to a sanitized version of `displayName`.
            ruleGroup (str, optional): The group to which the rule belongs. Defaults to None.
            description (str, optional): A description of the rule. Defaults to an empty string.

        Returns:
            None

        Raises:
            RuntimeError: If any HTTP request fails (non-200/201 status code).

        Notes:
            - Fetches the project ID using `getProjectID`.
            - Retrieves the list of existing rules in the project to check if the rule already exists.
            - If the rule exists, updates it with the new data using a PUT request.
            - If the rule does not exist, creates a new rule using a POST request.
            - Logs errors and raises exceptions for failed requests.
        """
        createOrUpdateRule(
            self.config,
            projectname,
            displayName,
            ruleSourceInternalName,
            internalName,
            ruleGroup,
            description,
        )

    def synchronizeCsvColsAndImportedColumns(
        self,
        projectname: str,
        filename: str,
    ) -> None:
        """
        Synchronizes the columns from a CSV file with the imported columns in a specified project.

        Args:
            projectname (str): The name of the project where the synchronization will occur.
            filename (str): The path to the CSV file to synchronize.

        Returns:
            None

        Raises:
            RuntimeError: If there are issues retrieving imported columns or reading the CSV file.

        Notes:
            - Retrieves the existing imported columns in the project using `getImportedColumns`.
            - Reads the first line of the CSV file to get column names.
            - Compares the column names from the CSV file with the imported columns.
            - Creates new imported columns in the project for any CSV column names not already present.
            - Uses utility functions `display_name`, `internal_name`, and `import_name` to format column names.
        """
        synchronizeCsvColsAndImportedColumns(self.config, projectname, filename)

    def focusMoveAttributeBefore(
        self,
        projectname: str,
        sourceDisplayName: str,
        targetDisplayName: str = None,
        groupInternalName : str = None,
    ) -> None:
        """
        Moves an attribute in the focus tree of a specified project, positioning it before a target attribute.

        Args:
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

        focusMoveAttributeBefore(
            self.config, projectname, sourceDisplayName, targetDisplayName,groupInternalName
        )

    def FetchDealFromHubSpotAndUploadToNEMO(self, projectname: str) -> None:
        """
        Fetches deal data from HubSpot, processes it, and uploads the combined information to a specified NEMO project.

        Args:
            projectname (str): The name of the NEMO project where the deal data will be uploaded.

        Returns:
            None

        Raises:
            RuntimeError: If any step in the HubSpot data retrieval or NEMO upload process fails.

        Notes:
            - Authenticates with HubSpot using the provided configuration.
            - Retrieves deals, deal history, and deal activities from HubSpot.
            - Merges deal history and activities with deal details.
            - Resolves internal fields (e.g., `companyId`, `userId`) to human-readable information.
            - Processes the deal data to map deal stages and other fields.
            - Finally, uploads the processed deal data to the specified NEMO project using `upload_deals_to_NEMO`.
            - Includes optional debugging capability for saving/loading intermediate data as a pickle file.
        """
        FetchDealFromHubSpotAndUploadToNEMO(self.config, projectname)
