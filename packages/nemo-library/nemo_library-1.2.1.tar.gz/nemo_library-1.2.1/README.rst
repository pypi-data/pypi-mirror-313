NEMO Library
============

This library helps you with access to NEMO APIs

Installation
============

::

   pip install nemo_library

Sources
=======

please find all sources on github:
https://github.com/H3rm1nat0r/nemo_library

configuration
=============

please create a file “config.ini”. This is an example for the content:

::

   [nemo_library]
   nemo_url = https://enter.nemo-ai.com
   tenant = <your tenant>
   userid = <your userid>
   password = <your password>
   environment = [prod|dev|demo]
   hubspot_api_token = <your API token, if you are going to use the HubSpot adapter, blank if not used>

If you don’t want to pass userid/password in a file (which is readable
to everybody that has access to the file), you can use Windows
Credential Manager or MacOS key chain to store your password. Please use
“nemo_library” as “Program name”. As an alternative, you can
programmatically set your password by using this code

.. code:: python

   from nemo_library.sub_password_handler import *

   service_name = "nemo_library"
   username = "my_username"
   password = "my_password"

   pm = PasswordManager(service_name, username)

   # Set password
   pm.set_password(password)
   print(f"Password for user '{username}' in service '{service_name}' has been stored.")

   # Retrieve password
   retrieved_password = pm.get_password()
   if retrieved_password:
       print(f"The stored password for user '{username}' is: {retrieved_password}")
   else:
       print(f"No password found for user '{username}' in service '{service_name}'.")

Methods
=======

Projects
--------

getProjectList method
~~~~~~~~~~~~~~~~~~~~~

Return list of projects (as pandas Dataframe)

.. code:: python

   from nemo_library import NemoLibrary

   nl = NemoLibrary()
   df = nl.getProjectList()

getProjectID method
~~~~~~~~~~~~~~~~~~~

Return internal id of project identified by given project name as shown
in the NEMO UI

.. code:: python

   from nemo_library import NemoLibrary

   nl = NemoLibrary()
   print(nl.getProjectID(projectname="Business Processes"))

ReUploadFile method
~~~~~~~~~~~~~~~~~~~

ReUpload a CSV file into an existing project

.. code:: python

   from nemo_library import NemoLibrary

   nl = NemoLibrary()
   nl.ReUploadFile(projectname="21 CRM", filename="./csv/hubspot.csv")

Args: - projectname (str): Name of the project. - filename (str): Name
of the file to be uploaded. - update_project_settings (bool, optional):
Whether to update project settings after ingestion. Defaults to True. -
datasource_ids (list[dict], optional): List of datasource identifiers
for V3 ingestion. Defaults to None. - global_fields_mapping (list[dict],
optional): Global fields mapping for V3 ingestion. Defaults to None. -
version (int, optional): Version of the ingestion process (2 or 3).
Defaults to 2 - trigger_only (bool, optional): Whether to trigger only
without waiting for task completion. Applicable for V3. Defaults to
False.

V2 uploads a file plain into the project. V3 merges the data with the
Business Processes project (needs more parameters)

synchronizeCsvColsAndImportedColumns method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sychronize columns with CSV file and NEMO meta data. This method
compares the list of columns found in CSV with the list of columns
defined in meta data and adds or removes missing or not-any-longer-used
columns to and from meta data. For performance reasons, you should not
use it on a daily base, but after changes in the source, it makes sense
to call it before uploading a file.

Here’s some example code from Gunnar’s reporting

.. code:: python

   nl = NemoLibrary()
   if synch_columns:
       nl.synchronizeCsvColsAndImportedColumns(
           projectname=PROJECT_NAME_SNR0,
           filename=folder_reporting_input_pa() + "/snr0_NEMO.csv",
       )
       time.sleep(120)
   nl.ReUploadFile(
       projectname=PROJECT_NAME_SNR0,
       filename=folder_reporting_input_pa() + "/snr0_NEMO.csv",
   )

Reports
-------

LoadReport method
~~~~~~~~~~~~~~~~~

Load a report from NEMO and return this as pandas dataframe

.. code:: python

   from nemo_library import NemoLibrary

   nl = NemoLibrary()
   df = nl.LoadReport(report_guid="b82cfed8-81a7-44e0-b3da-c76454540697")

project_id
^^^^^^^^^^

Optional parameter. If you want to get reports for non-default ERP
projects. Please provide the project GUID (you can retrieve them by
running getProjectList)

report_guid
^^^^^^^^^^^

This methode takes 1 mandatory parameter, the report_guid. You can find
“your” guid in NEMO meta data. Just open the definition of the report in
meta data and copy the GUID from your browser URL.

The report “(SAMPLE) Replenishment Time Analysis Purchased Parts” for
example has this URL:
https://enter.nemo-ai.com/nemo/metadata/report/b82cfed8-81a7-44e0-b3da-c76454540697
and thus the GUID you need is then
“b82cfed8-81a7-44e0-b3da-c76454540697”

max_pages
^^^^^^^^^

By default all pages from the report are loaded. You can optionally
restrict the amount of data by providing max_pages parameter and you’ll
get not more than this number of pages (usually 1 page holds 20 records)

InfoZoom / NEMO synchronization
-------------------------------

There are two thinkable ways of synchronization between InfoZoom and
NEMO. At the moment, we support InfoZoom –> NEMO direction only. The
other way is on my wish list, but not implemented yet

InfoZoom –> NEMO
~~~~~~~~~~~~~~~~

When synchronizing an InfoZoom (FOX) file with NEMO, there are two
thinks to think about - data: data can easily uploaded using the above
mentioned “ReUploadFile” method (maybe you need to use InfoZoom batch
commands to extract the data first). But it’s on my list as well to make
this more automatic - meta data: this is the point, where this library
is the closest to a final solution

exportMetadata
^^^^^^^^^^^^^^

Exports metadata from an InfoZoom file using the InfoZoom executable.

.. code:: python

   from nemo_library import NemoLibrary

   nl = NemoLibrary()
   nl.exportMetadata(infozoomexe="C:\\Program Files (x86)\\NEMO\\InfoZoom 2025\\InfoZoom.exe",infozoomfile="D:\\temp\\SNr.fox",metadatafile="D:\\temp\\SNr.metadata.csv")

This code snipped calls exportMetadata method which itself opens
InfoZoom (identified by the given executable path), then opens the given
fox file, openes the metadata view and finally exports the metadata file
into the given CSV file (delimiter ;, UTF-8-Format).

This is the first step needed to synchronize the FOX meta data with
NEMO.

synchMetadataWithFocus
~~~~~~~~~~~~~~~~~~~~~~

Synchronizes metadata from a given CSV file with the NEMO project
metadata.

This method reads metadata from a CSV file, processes it, and
synchronizes it with the metadata of a specified NEMO project. It
handles the creation of groups first and then processes individual
attributes.

.. code:: python

   from nemo_library import NemoLibrary

   nl = NemoLibrary()
   projectId = nl.getProjectID(projectname="VH0001_21_XVH001_SNrNemo")
   nl.synchMetadataWithFocus(metadatafile="d:\\temp\\SNr.metadata.csv", projectId=projectId)

This code snipped gets the projectid identified by its name in NEMO and
then synchronizes the meta data (exported by synchMetadataWithFocus)
with NEMO.

At the moment the following pieces are synchronized - Groups (and sub
groups and sub sub groups etc) - sequence of attributes (and allocation
with groups)

This is a list of pieces that are currently ignored - Couples - Formulae
- case statements - aggregations - this list is not complete

HubSpot
-------

HubSpot is the very first CRM product that we support in this library.
This adapter provides a method that uses the HubSpot API to extract
deals and their history (deal changes as well as documented
communication) and finally uploads this into a NEMO project given by
it’s name.

If you want to use this, you have to enable this feature in Hubspot
first. Steps: - create a private app in HubSpot (e.g. export for NEMO) -
you are given an API token and a secret. Note them and enter the API
token in the config.ini-file. Example:

::

   hubspot_api_token = <your API token>

-  provide read access to all objects, e.g. crm.schemas.deals.read, etc.

Then you can use the HubSpot adapter like in this example:

.. code:: python

   nl = NemoLibrary()
   nl.FetchDealFromHubSpotAndUploadToNEMO(projectname="21 CRM Activities")

Contributions
=============

Contributions are welcome! If you would like to suggest improvements or
have found a bug, please open an issue or submit a pull request.

License
=======

This project is released under the Unlicense. You can find the full text
of the Unlicense in the `UNLICENSE <UNLICENSE>`__ file. This means that
the code is released into the public domain, and you are free to use,
modify, distribute, and do whatever you want with it, without any
restrictions or requirements.
