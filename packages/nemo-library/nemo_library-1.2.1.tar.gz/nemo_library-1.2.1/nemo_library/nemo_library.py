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
    getImportedColumns,
    getProjectID,
    getProjectList,
    getProjectProperty,
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
        return getProjectList(self.config)

    def getProjectID(self, projectname: str) -> str:
        return getProjectID(self.config, projectname)

    def getProjectProperty(self, projectname: str, propertyname: str) -> str:
        return getProjectProperty(self.config, projectname, propertyname)

    def LoadReport(
        self,
        projectname: str,
        report_guid: str,
        max_pages=None,
    ) -> pd.DataFrame:
        return LoadReport(self.config,projectname,report_guid,max_pages)
        
    def createProject(self, projectname: str, description: str) -> None:
        return createProject(self.config, projectname, description)

    def createProjectsForMigMan(self, projects: list[str]) -> None:
        createProjectsForMigMan(self.config, projects=projects)

    def getImportedColumns(self, projectname: str) -> pd.DataFrame:
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
        createImportedColumn(self.config,projectname,displayName,dataType,importName,internalName,description)

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
        ReUploadFile(self.config,projectname,filename,update_project_settings,datasource_ids,global_fields_mapping,version,trigger_only)

    def createOrUpdateReport(
        self,
        projectname: str,
        displayName: str,
        querySyntax: str,
        internalName: str = None,
        description: str = None,
    ) -> None:
        createOrUpdateReport(self.config,projectname,displayName,querySyntax,internalName,description)

    def createOrUpdateRule(
        self,
        projectname: str,
        displayName: str,
        ruleSourceInternalName: str,
        internalName: str = None,
        ruleGroup: str = None,
        description: str = None,
    ) -> None:
        createOrUpdateRule(self.config,projectname,displayName,ruleSourceInternalName,internalName,ruleGroup,description)

    def synchronizeCsvColsAndImportedColumns(
        self,
        projectname: str,
        filename: str,
    ) -> None:
        synchronizeCsvColsAndImportedColumns(self.config,projectname,filename)

    def focusMoveAttributeBefore(
        self,
        projectname: str,
        sourceDisplayName: str,
        targetDisplayName: str = None,
    ) -> None:
        focusMoveAttributeBefore(self.config,projectname,sourceDisplayName,targetDisplayName)
        
    def FetchDealFromHubSpotAndUploadToNEMO(self, projectname: str) -> None:
        FetchDealFromHubSpotAndUploadToNEMO(self.config,projectname)
