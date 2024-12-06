import os
import sys
import pytest
import requests

from nemo_library import NemoLibrary
from datetime import datetime
from nemo_library.sub_infozoom_handler import (
    getFOXMetaData,
    getNEMOMetaData_imported_columns,
)

IC_PROJECT_NAME = "gs_unit_test_Intercompany"


def getNL():
    """
    Initializes and returns an instance of the NemoLibrary class.

    This function reads the configuration settings from the specified
    configuration file and uses them to create and return a NemoLibrary
    object.

    Returns:
        NemoLibrary: An instance of the NemoLibrary class initialized
                     with settings from 'tests/config.ini'.

    Example:
        nl = getNL()
        print(nl)

    Note:
        The configuration file 'tests/config.ini' should be present in
        the specified path and contain the necessary configuration
        settings required for initializing the NemoLibrary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ConfigParserError: If there is an error parsing the configuration file.

    """
    return NemoLibrary(
        config_file="tests/config.ini",
    )


def test_getProjectList():
    """
    Test the getProjectList method of the NemoLibrary class.

    This test initializes the NemoLibrary, retrieves the project list,
    prints the DataFrame, and asserts that the DataFrame contains at
    least one row. It also checks that the 'id' of the first row matches
    the expected value.

    Raises:
        AssertionError: If the DataFrame is empty or the 'id' of the first row
                        does not match the expected value.
    """
    nl = getNL()
    df = nl.getProjectList()
    print(df)
    assert len(df) > 0
    first_row = df.iloc[0]
    assert first_row["id"] == "00000000-0000-0000-0000-000000000001"


def test_getProjectID():
    """
    Test the getProjectID method of the NemoLibrary class.

    This test initializes the NemoLibrary and asserts that the project ID
    returned for the project name "Business Processes" matches the expected value.

    Raises:
        AssertionError: If the returned project ID does not match the expected value.
    """
    nl = getNL()
    assert (
        nl.getProjectID("Business Processes") == "00000000-0000-0000-0000-000000000001"
    )


def test_getProjectProperty():
    """
    Test the getProjectProperty method of the NemoLibrary class.

    This test initializes the NemoLibrary, retrieves a project property value for
    the given project and property names, and asserts that the value is not None.
    It also checks if the returned value is in the format 'YYYY-MM-DD' and that the
    year is within the acceptable range (2000-2100).

    Raises:
        AssertionError: If the returned value is None, not in the format 'YYYY-MM-DD',
                        or the year is out of the acceptable range.
        pytest.fail: If the returned value is not in the format 'YYYY-MM-DD'.
    """
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


def test_ReUploadFile():
    """
    Test the ReUploadFile method of the NemoLibrary class.

    This test initializes the NemoLibrary, re-uploads a file for a given project,
    and asserts that the expected number of records matches the returned value.

    Raises:
        AssertionError: If the number of records does not match the expected value.
    """
    nl = getNL()

    nl.ReUploadFile(
        projectname=IC_PROJECT_NAME,
        filename="./tests/intercompany_NEMO.csv",
    )

    val = nl.getProjectProperty(
        projectname=IC_PROJECT_NAME, propertyname="ExpNumberOfRecords"
    )
    assert int(val) == 34960, "number of records do not match"


def test_SynchColumns():
    """
    Test the synchronizeCsvColsAndImportedColumns method of the NemoLibrary class.

    This test initializes the NemoLibrary, synchronize fields from a file for a given project,
    and asserts that the expected number of records matches the returned value.

    Raises:
        AssertionError: If the number of records does not match the expected value.
    """

    nl = getNL()
    nl.synchronizeCsvColsAndImportedColumns(
        projectname=IC_PROJECT_NAME,
        filename="./tests/intercompany_NEMO.csv",
    )

    val = nl.getProjectProperty(
        projectname=IC_PROJECT_NAME, propertyname="ExpNumberOfRecords"
    )
    assert int(val) == 34960, "number of records do not match"

@pytest.mark.skipif(sys.platform != "win32", reason="we can run InfoZoom on windows only")
def test_exportMetadata():
    test_file = "./tests/SNr.metadata.test.csv"
    reference_file = "./tests/SNr.metadata.csv"

    nl = getNL()
    nl.exportMetadata(
        infozoomexe="C:/Program Files (x86)/NEMO/InfoZoom 2025/InfoZoom.exe",
        infozoomfile="./tests/snr.fox",
        metadatafile=test_file,
    )

    # Ensure the test file has been created
    assert os.path.exists(test_file), f"{test_file} was not created."

    # Read the content of the test file
    with open(test_file, "r", encoding="utf-8") as test_f:
        test_content = test_f.read()

    # Read the content of the reference file
    with open(reference_file, "r", encoding="utf-8") as reference_f:
        reference_content = reference_f.read()

    # Check if the contents of the two files are identical
    assert test_content == reference_content, "The files are not identical."

def test_synchMetadataWithFocus():
    # test de-activated since we don't have the analyzer file in challenge and I was not able to reproduce the file with the same attributes like in prod
    """
    Test the synchronization of FOX metadata with a NEMO project.

    This function performs the following steps:
    1. Creates an instance of NemoLibrary.
    2. Retrieves the project ID for a specific NEMO project.
    3. Calls the synchronization method to sync metadata from a given file with the NEMO project.
    4. Validates the synchronization by comparing the number of 'Einfaches Attribut' attributes
       in the FOX metadata with the number of attributes in the NEMO metadata.

    Raises:
        AssertionError: If the number of 'Einfaches Attribut' attributes in FOX metadata does not
                        match the number of attributes in the NEMO metadata.
    """

    # call API to synchronize FOX Meta data with NEMO project
    nl = getNL()
    projectId = nl.getProjectID(projectname="VH0001_21_XVH001_SNrNemo")
    metadatafile = "./tests/SNr.metadata.csv"
    nl.synchMetadataWithFocus(metadatafile=metadatafile, projectId=projectId)

    # now validate number of attributes
    dfMetaFOX = getFOXMetaData(metadatafile=metadatafile)
    dfMetaNEMO = getNEMOMetaData_imported_columns(config=nl.config, projectId=projectId)

    dfMetaFOX_Attributes = dfMetaFOX[dfMetaFOX["Definition"] == "Einfaches Attribut"]

    assert (
        len(dfMetaFOX_Attributes) == len(dfMetaNEMO) + 2
    )  # there are some attributes twice and thus cannot be sorted


def test_LoadReport():
    """
    Test the LoadReport method of the NemoLibrary class.

    This test initializes the NemoLibrary, loads a report for a given project and
    report GUID, and asserts that the DataFrame contains the expected number of rows.

    Raises:
        AssertionError: If the DataFrame does not contain the expected number of rows.
    """
    nl = getNL()
    df = nl.LoadReport(
        projectname=IC_PROJECT_NAME,
        report_guid="2b02f610-c70e-489a-9895-2cab382ff911",
    )

    assert len(df) == 33
