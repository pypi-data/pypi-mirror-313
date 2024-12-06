import logging
import random
import pandas as pd
import re
import importlib.resources
import os
import tempfile
from faker import Faker
from decimal import Decimal


from nemo_library.features.config import Config
from nemo_library.features.fileingestion import ReUploadFile
from nemo_library.features.focus import focusMoveAttributeBefore
from nemo_library.features.projects import (
    createImportedColumn,
    createProject,
    getProjectList,
)
from nemo_library.utils.utils import display_name, import_name, internal_name

__all__ = ["createProjectsForMigMan"]


def createProjectsForMigMan(config: Config, projects: list[str]) -> None:
    """Create projects for MigMan based on given config and project list."""
    for project in projects:
        scan_project(config, project)


def scan_project(config: Config, project: str) -> None:
    """Scan a single project and process its files."""
    logging.info(f"Scanning project '{project}'")

    # Get matching files
    matching_files = get_matching_files(project)
    if not matching_files:
        error_message = (
            f"No files found for project '{project}'. Please check for typos"
        )
        logging.error(error_message)
        raise ValueError(error_message)

    # Sort files
    sorted_files = sort_files(matching_files)

    # Process each file
    for filename in sorted_files:
        postfix = extract_postfix(filename)
        process_file(config, project, filename, postfix)


def get_matching_files(project: str) -> list[str]:
    """Get all matching files for the given project."""
    pattern = re.compile(f"^Template {project} (MAIN|Add\\d+)\\.csv$", re.IGNORECASE)
    return [
        resource
        for resource in importlib.resources.contents("nemo_library.migmantemplates")
        if pattern.match(resource)
    ]


def sort_files(files: list[str]) -> list[str]:
    """Sort files with 'MAIN' first, followed by 'ADD' files in numerical order."""
    return sorted(
        files,
        key=lambda x: (
            0 if "MAIN" in x else 1,
            int(re.search(r"ADD(\d+)", x).group(1)) if "ADD" in x else float("inf"),
        ),
    )


def extract_postfix(filename: str) -> str:
    """Extract the postfix from the filename."""
    match = re.search(r"(\w{4})\.", filename)
    if match:
        return match.group(1)
    else:
        error_message = f"No valid postfix found in filename '{filename}'"
        logging.error(error_message)
        raise ValueError(error_message)


def process_file(config: Config, project: str, filename: str, postfix: str) -> None:
    """Process a single file and create a project."""
    logging.info(f"Processing file {filename} (postfix {postfix})")
    with importlib.resources.open_binary(
        "nemo_library.migmantemplates", filename
    ) as file:

        # there is a bug in the migman exporter. It has too many separators and the columns are "shifted". This is the csv in plain text
        # Column;Column Name;Description / Remark;Location in proALPHA;Data Type;Format
        # 1;Kunde;Customer;S_Kunde.Kunde;INTEGER;zzzzzzzz;
        # 2;Adressnummer;Address Number;S_Adresse.AdressNr;INTEGER;zzzzzzz9;
        # 3;Name;Name 1;S_Adresse.Name1;CHARACTER;x(80);

        df = pd.read_csv(
            file,
            skiprows=2,
            encoding="ISO-8859-1",
            sep=";",
        )

        df["Format"] = df["Data Type"]
        df["Data Type"] = df["Location in proALPHA"]
        df["Location in proALPHA"] = df["Description / Remark"]
        df.drop(columns=["Description / Remark"], inplace=True)

        projectname = f"{project} ({postfix})" if postfix != "MAIN" else project

        # project already exists?
        if not projectname in getProjectList(config)["displayName"].to_list():
            logging.info(f"Project not found in NEMO. Create it...")
            createProject(
                config=config,
                projectname=projectname,
                description=f"Data Model for Mig Man table '{project}'",
            )

            process_columns(config, projectname, df)

        uploadData(config, projectname, df)


def process_columns(
    config: Config,
    projectname: str,
    df: pd.DataFrame,
) -> None:

    # synchronize columns
    lastDisplayName = None
    for idx, row in df.iterrows():

        logging.info(f"process column {row["Column"]} with index {idx}")
        displayName = display_name(row["Location in proALPHA"],idx)
        internalName = internal_name(row["Location in proALPHA"],idx)
        importName = import_name(row["Location in proALPHA"],idx)
        
        # column already exists?
        if True:
            logging.info(
                f"Colunn {displayName} not found in project {projectname}. Create it."
            )
            description = "\n".join([f"{key}: {value}" for key, value in row.items()])
            createImportedColumn(
                config=config,
                projectname=projectname,
                displayName=displayName,
                internalName=internalName,
                importName=importName,
                dataType="string",  # we try a string-only-project to avoid importing errors
                description=description,
            )

            logging.info(f"Move column {displayName} to position {idx} in focus")
            focusMoveAttributeBefore(
                config=config,
                projectname=projectname,
                sourceDisplayName=displayName,
                targetDisplayName=lastDisplayName,
            )

        lastDisplayName = displayName


def uploadData(config: Config, projectname: str, df: pd.DataFrame) -> None:
    logging.info(f"Upload dummy file for project {projectname}")

    faker = Faker("de_DE")

    columns = [
        import_name(idx, row["Location in proALPHA"]) for idx, row in df.iterrows()
    ]
    data_types = df["Data Type"].to_list()
    formats = df["Format"].to_list()

    def generate_column_data(dtype, format, num_rows):

        match dtype:
            case "character":
                # Parse format to get maximum length
                match = re.search(r"x\((\d+)\)", format)
                field_length = int(match.group(1)) if match else len(format)

                # Generate fake texts now
                if field_length <= 6:
                    return [
                        faker.word()[:field_length].strip() for _ in range(num_rows)
                    ]
                else:
                    return [
                        faker.text()[:field_length].strip() for _ in range(num_rows)
                    ]

            case "integer":
                # Parse format
                negative_numbers = "-" in format
                if negative_numbers:
                    format = format.replace("-", "")

                match = re.search(r"z\((\d+)\)", format)
                field_length = int(match.group(1)) if match else len(format)

                def generate_integer(negative_numbers, field_length):
                    # Generate the maximum integer based on the field length
                    max_integer = 10**field_length - 1

                    # Generate a random integer within the allowed range
                    result = faker.random_int(min=0, max=max_integer)

                    # Randomly make the number negative if negative numbers are allowed
                    if negative_numbers and random.choice([True, False]):
                        result *= -1

                    return result

                return [
                    generate_integer(negative_numbers, field_length)
                    for _ in range(num_rows)
                ]
            case "decimal":

                # Parse format
                negative_numbers = "-" in format
                if negative_numbers:
                    format = format.replace("-", "")

                # decimals?
                decimals = len(format.split(".")[1]) if "." in format else 0
                if decimals > 0:
                    format = format[: len(format) - decimals - 1]

                # now the format has the length without decimals and without sign

                # Parse format to get maximum length
                match = re.search(r"z\((\d+)\)", format)
                field_length = int(match.group(1)) if match else len(format)

                def generate_decimal(negative_numbers, field_length, decimals):
                    # Generate the maximum integer based on the field length
                    max_integer = 10**field_length - 1
                    # Define the range for decimal places
                    max_decimal = 10**decimals
                    # Generate a random integer within the allowed range
                    integer_part = faker.random_int(min=0, max=max_integer)
                    # Generate random decimal places
                    decimal_part = faker.random_int(min=0, max=max_decimal - 1)

                    # Combine the integer and decimal parts into a Decimal object
                    result = Decimal(f"{integer_part}.{decimal_part:0{decimals}d}")

                    # Randomly make the number negative if negative numbers are allowed
                    if negative_numbers and random.choice([True, False]):
                        result *= -1

                    return result

                return [
                    generate_decimal(negative_numbers, field_length, decimals)
                    for _ in range(num_rows)
                ]
            case "date" | "datetime" | "datetime-tz":
                return [faker.date_this_decade() for _ in range(num_rows)]
            case "logical":
                return [faker.boolean() for _ in range(num_rows)]
            case _:
                return [faker.text() for _ in range(num_rows)]

    # Introduce errors into the dataset
    def introduce_errors(df, error_rate=0.2):
        num_rows, num_cols = df.shape
        num_errors = int(num_rows * num_cols * error_rate)
        for _ in range(num_errors):
            row_idx = random.randint(0, num_rows - 1)
            col_idx = random.randint(0, num_cols - 1)
            col_name = df.columns[col_idx]
            dtype = data_types[col_idx]
            format = formats[col_idx]

            match dtype:
                case "character":
                    match = re.search(r"x\((\d+)\)", format)
                    field_length = int(match.group(1)) if match else len(format)

                    if random.choice([True, False]):
                        df.at[row_idx, col_name] = ""  # Empty field
                    else:
                        df.at[row_idx, col_name] = "X" * (field_length + 5)

                case "integer" | "decimal":
                    negative_numbers = "-" in format

                    if not negative_numbers and random.choice([True, False]):
                        df.at[row_idx, col_name] = -99999  # Out-of-range value
                    else:

                        if random.choice([True, False]):
                            df.at[row_idx, col_name] = None  # Missing value
                        else:
                            df.at[row_idx, col_name] = (
                                "INVALID NUMBER"  # Invalid format
                            )

                case "date" | "datetime" | "datetime-tz":
                    if random.choice([True, False]):
                        df.at[row_idx, col_name] = None  # Missing value
                    else:
                        df.at[row_idx, col_name] = "INVALID_DATE"  # Invalid format
                case "logical":
                    if random.choice([True, False]):
                        df.at[row_idx, col_name] = None  # Missing value
                    else:
                        df.at[row_idx, col_name] = "INVALID_BOOLEAN"  # Invalid format
                case _:
                    df.at[row_idx, col_name] = ""  # Empty field

        return df

    num_rows = 500
    data = {
        col: generate_column_data(dtype, format, num_rows)
        for col, format, dtype in zip(columns, formats, data_types)
    }

    dummy_df = pd.DataFrame(data)

    for idx, col in enumerate(columns):
        dummy_df[col] = dummy_df[col].astype("str")

    # Introduce 10% errors into the dummy dataset
    dummy_df = introduce_errors(dummy_df)

    # Write to a temporary file and upload
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "tempfile.csv")

        dummy_df.to_csv(
            temp_file_path,
            index=False,
            sep=";",
            na_rep="",
        )
        logging.info(
            f"dummy file {temp_file_path} written for project '{projectname}'. Uploading data to NEMO now..."
        )

        ReUploadFile(
            config=config,
            projectname=projectname,
            filename=temp_file_path,
            update_project_settings=False,
        )
        logging.info(f"upload to project {projectname} completed")


