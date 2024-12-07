import pytest

from nemo_library import NemoLibrary
from datetime import datetime

IC_PROJECT_NAME = "gs_unit_test_Intercompany"
MM_PROJECT_NAME = "Regions"
HS_PROJECT_NAME = "gs_unit_test_HubSpot"

def getNL():
    return NemoLibrary(
        config_file="tests/config.ini",
    )


def test_getProjectList():
    nl = getNL()
    df = nl.getProjectList()
    print(df)
    assert len(df) > 0
    first_row = df.iloc[0]
    assert first_row["id"] == "00000000-0000-0000-0000-000000000001"


def test_getProjectID():
    nl = getNL()
    assert (
        nl.getProjectID("Business Processes") == "00000000-0000-0000-0000-000000000001"
    )


def test_getProjectProperty():
    nl = getNL()
    val = nl.getProjectProperty(
        projectname="Business Processes", propertyname="ExpDateFrom"
    )

    assert val is not None, "API call did not return any value"

    try:
        date_val = datetime.strptime(val, "%Y-%m-%d")
    except ValueError:
        pytest.fail(f"Returned value ({val}) is not in the format YYYY-MM-DD")

    assert (
        2000 <= date_val.year <= 2100
    ), "Year is out of the acceptable range (2000-2100)"


def test_createProject():
    nl = getNL()

    # check if project exists (should not)
    projects = nl.getProjectList()["displayName"].to_list()
    if IC_PROJECT_NAME in projects:
        nl.deleteProject(IC_PROJECT_NAME)

    # now we can create the project
    nl.createProject(
        IC_PROJECT_NAME,
        "used for unit tests of nemo_library",
    )
    projects = nl.getProjectList()["displayName"].to_list()
    assert IC_PROJECT_NAME in projects


def test_createImportedColumn():
    nl = getNL()
    nl.createImportedColumn(
        projectname=IC_PROJECT_NAME,
        displayName="Rechnungsdatum",
        dataType="date",
        description="Rechnungsdatum",
    )
    importedColumns = nl.getImportedColumns(IC_PROJECT_NAME)
    assert "Rechnungsdatum" in importedColumns["displayName"].to_list()


def test_getImportedColumns():
    nl = getNL()
    df = nl.getImportedColumns(IC_PROJECT_NAME)
    assert (
        len(df) == 1
    )  # we have checked the behavior in test_createImportedColumn already...


def test_synchronizeCsvColsAndImportedColumns():
    nl = getNL()
    nl.synchronizeCsvColsAndImportedColumns(
        projectname=IC_PROJECT_NAME,
        filename="./tests/intercompany_NEMO.csv",
    )

    importedColumns = nl.getImportedColumns(IC_PROJECT_NAME)
    assert len(importedColumns) == 20


def test_setProjectMetaData():
    nl = getNL()
    nl.setProjectMetaData(
        IC_PROJECT_NAME,
        processid_column="seriennummer",
        processdate_column="rechnungsdatum",
        corpcurr_value="EUR",
    )
    assert True


def test_ReUploadFile():
    nl = getNL()

    nl.ReUploadFile(
        projectname=IC_PROJECT_NAME,
        filename="./tests/intercompany_NEMO.csv",
        update_project_settings=False,
    )

    assert True

def test_focusMoveAttributeBefore():
    nl = getNL()
    nl.focusMoveAttributeBefore(IC_PROJECT_NAME,"Mandant",None)
    assert True

def test_createOrUpdateReport():
    nl = getNL()
    # ml.createOrUpdateReport()


def test_createOrUpdateRule():
    nl = getNL()
    # ml.createOrUpdateRule()


def test_LoadReport():
    nl = getNL()
    return
    df = nl.LoadReport(
        projectname=IC_PROJECT_NAME,
        report_guid="2b02f610-c70e-489a-9895-2cab382ff911",
    )

    assert len(df) == 33


def test_deleteProject():
    nl = getNL()
    nl.deleteProject(IC_PROJECT_NAME)
    projects = nl.getProjectList()["displayName"].to_list()
    assert not IC_PROJECT_NAME in projects


def test_createProjectsForMigMan():
    nl = getNL()
    # check if project exists (should not)
    projects = nl.getProjectList()["displayName"].to_list()
    if MM_PROJECT_NAME in projects:
        nl.deleteProject(MM_PROJECT_NAME)

    # now we can create the project
    nl.createProjectsForMigMan([MM_PROJECT_NAME])
    projects = nl.getProjectList()["displayName"].to_list()
    assert MM_PROJECT_NAME in projects

    # check number of attributes
    importedColumns = nl.getImportedColumns(MM_PROJECT_NAME)
    assert len(importedColumns) == 2
    
    # delete the project for clean up
    nl.deleteProject(MM_PROJECT_NAME)

def test_FetchDealFromHubSpotAndUploadToNEMO():
    nl = getNL()
    nl.createProject(HS_PROJECT_NAME,"project for unit tests")
    nl.FetchDealFromHubSpotAndUploadToNEMO(HS_PROJECT_NAME)
    nl.deleteProject(HS_PROJECT_NAME)
    assert True
