import configparser
import os
from typing import List, Tuple
import pandas as pd
import xml.etree.ElementTree as ET


class SQLGeneratorPL:
    """
    A class to generate SQL files and validate column data from an XML import file.
    """

    def generate_sql(self) -> None:
        """
        Generates the SQL file based on the configuration provided in 'sql_generator_config.ini'.
        """

        sql_fragments = []

        # Load configuration
        config = configparser.ConfigParser()
        config.read("sql_generator_config.ini")
        import_file = config["PL"]["import_file"]
        output_file = config["PL"]["output_file"]
        years_back = int(config["PL"]["years_back"])
        booking_period_offset = int(config["PL"]["booking_period_offset"])
        column_id = int(config["PL"]["column_id"])
        company = int(config["PL"]["company"])

        # Validate configuration
        self.validateImportFile(import_file)
        self.validateColumn(import_file, column_id)

        # some pre-calculations
        business_periods = self.generate_business_periods(years_back)
        labels = self.generate_labels(business_periods)
        date_calulations = self.generate_date_calculations(
            years_back, booking_period_offset, business_periods
        )

        # header
        self.generate_header(sql_fragments, business_periods, labels)

        # SQL finally

        self.generate_PandL(
            sql_fragments, business_periods, labels, import_file, column_id, company
        )

        select = date_calulations
        ordered_fragments = []

        for idx, frag in enumerate(sql_fragments):
            ordered_fragments.append(
                f"""SELECT
    {idx +1} AS SortOrder,
{frag}"""
            )

        select += "\nUNION ALL\n".join(ordered_fragments)
        select += "\nORDER BY SortOrder"

        # export
        self.export(select, output_file)

    def validateImportFile(self, import_file: str) -> None:
        """
        Validates that the import file exists.

        Args:
            import_file (str): The path to the XML import file.
        """
        if not os.path.exists(import_file):
            raise FileNotFoundError(f"The import file '{import_file}' does not exist.")
        print(f"validation: import file {import_file} exists")

    def validateColumn(self, import_file: str, column_id: int) -> None:
        """
        Validates the column data from the given XML import file and column ID.

        Args:
            import_file (str): The path to the XML import file.
            column_id (int): The column ID to validate.
        """
        # Parse the XML file
        tree = ET.parse(import_file)
        root = tree.getroot()

        # Find all entries under 'ttSA_Spalte' and 'ttSA_SpalteSpr'
        ttSA_Spalte_entries = root.findall(".//ttSA_Spalte")
        ttSA_SpalteSpr_entries = root.findall(".//ttSA_SpalteSpr")

        # Extract all values in 'ttSA_Spalte'
        ttSA_Spalte_values = []
        for entry in ttSA_Spalte_entries:
            entry_dict = {}
            for elem in entry:
                entry_dict[elem.tag] = elem.text
            ttSA_Spalte_values.append(entry_dict)

        df_ttSA_Spalte = pd.DataFrame(
            ttSA_Spalte_values, columns=["SpaltenID", "SpaltenNr"]
        ).sort_values(by="SpaltenNr")

        # Extract all values in 'ttSA_SpalteSpr' where Sprache is 'D'
        ttSA_SpalteSpr_values = []
        for entry in ttSA_SpalteSpr_entries:
            entry_dict = {}
            for elem in entry:
                entry_dict[elem.tag] = elem.text
            if entry_dict.get("Sprache") == "D":
                ttSA_SpalteSpr_values.append(entry_dict)

        df_ttSA_SpalteSpr = pd.DataFrame(
            ttSA_SpalteSpr_values, columns=["SpaltenID", "Ueberschrift"]
        )

        # Merge the DataFrames on 'SpaltenID'
        df_ttSA_Spalte = df_ttSA_Spalte.merge(
            df_ttSA_SpalteSpr, on="SpaltenID", how="left"
        )

        # Check if a record with the given column_id exists
        row = df_ttSA_Spalte[df_ttSA_Spalte["SpaltenID"] == str(column_id)]
        if row.empty:
            print(df_ttSA_Spalte)
            raise Exception(f"No record found with SpaltenID = {column_id}")
        else:
            # Print the matching record
            row = row.iloc[0]
            col_no = row["SpaltenNr"]
            col_label = row["Ueberschrift"]
            print(
                f"validation: column_id {column_id} verfied. Label: {col_label}, col no: {col_no}"
            )

    def generate_business_periods(self, years_back: int) -> list[tuple[int, int]]:
        """
        Generates a list of business periods for the specified number of years back from the current year.

        Args:
            years_back (int): The number of years back from the current year for which to generate business periods.

        Returns:
            list: A list of tuples representing business periods. Each tuple contains a year and a month.
        """
        # Initialize an empty list to store the business periods
        business_periods = []

        # Loop over the range of years from (-years_back + 1) to 1 (inclusive)
        for year in range((-years_back + 1), 1):
            # Loop over the months from 1 to 12 (inclusive)
            for month in range(1, 13):
                # Append a tuple (-year, month) to the business_periods list
                # The year is negated to match the required format
                business_periods.append((-year, month))

        # Return the list of business periods
        return business_periods

    def generate_labels(self, business_periods: list[tuple[int, int]]) -> list[str]:
        """
        Generates a list of labels for the given business periods.

        Args:
            business_periods (list[tuple[int, int]]): A list of tuples representing business periods.
                Each tuple contains a year and a month.

        Returns:
            list[str]: A list of formatted string labels for each business period.
        """
        # Create a list of formatted labels for each business period
        labels = [
            f'"P&L_FY{year:02d}_FM{month:02d}"'  # Format the label as "P&L_FYyy_FMmm"
            for (
                year,
                month,
            ) in business_periods  # Iterate over each year and month tuple in business_periods
        ]

        # Return the list of labels
        return labels

    def generate_date_calculations(
        self,
        years_back: int,
        booking_period_offset: int,
        business_periods: List[Tuple[int, int]],
    ) -> str:
        """
        Generates SQL fragments for calculating fiscal years and calendar periods based on input parameters.

        Args:
            years_back (int): The number of years to go back from the current date for fiscal year calculations.
            booking_period_offset (int): The offset in months to adjust the booking period.
            business_periods (list of tuples): A list of tuples where each tuple contains a year and month representing business periods.

        Returns:
            str: A SQL fragment containing CTEs (Common Table Expressions) for DateCalculationsFiscalYear and DateCalculations.

            - DateCalculationsFiscalYear: Calculates fiscal years based on the current date, years_back, and booking_period_offset.
            - DateCalculations: Adds calendar periods to the fiscal years based on business_periods and booking_period_offset.

        Example:
            years_back = 5
            booking_period_offset = 3
            business_periods = [(0, 1), (0, 2), (1, 3), (1, 4)]

            This would generate SQL fragments for fiscal years from the current date going back 5 years with a 3 month booking period offset,
            and then calculate calendar periods for the specified business periods.

        """
        # fiscal years
        frags = [
            f"YEAR(ADD_YEARS(ADD_MONTHS(CURRENT_DATE, -{booking_period_offset}), {year})) AS FiscalYearMinus{-year}"
            for year in range((-years_back + 1), 1)
        ]
        lines = ",\n        ".join(frags)

        fragment = f"""WITH DateCalculationsFiscalYear AS (
    SELECT  
        {lines}
    FROM 
        DUMMY            
    ),
"""
        # fiscal months
        frags = [
            f"ADD_MONTHS(TO_DATE(FiscalYearMinus{year:01d} || '-{month:02d}-01'),{booking_period_offset}) AS CalendarPeriod{idx}"
            for idx, (year, month) in enumerate(business_periods)
        ]
        lines = ",\n        ".join(frags)

        fragment += f"""DateCalculations AS (
    SELECT  
        *,
        {lines}
    FROM 
        DateCalculationsFiscalYear            
    )
"""
        return fragment

    def generate_header(
        self,
        sql_fragments: List[str],
        business_periods: List[Tuple[int, int]],
        labels: List[str],
    ) -> None:
        """
        Generates and appends SQL header fragments for fiscal years and fiscal months to the provided list of SQL fragments.

        Args:
            sql_fragments (list of str): The list of SQL fragments to which the header fragments will be appended.
            business_periods (list of tuples): A list of tuples where each tuple contains a year and month representing business periods.
            labels (list of str): A list of labels corresponding to the business periods.

        Returns:
            list of str: The updated list of SQL fragments with the header fragments for fiscal years and fiscal months appended.

        Example:
            sql_fragments = []
            business_periods = [(0, 1), (0, 2), (1, 3), (1, 4)]
            labels = ["Label1", "Label2", "Label3", "Label4"]

            This would append SQL header fragments for the specified business periods and labels to the sql_fragments list.
        """
        self.generate_header_fiscal_year(sql_fragments, business_periods, labels)
        self.generate_header_fiscal_month(sql_fragments, business_periods, labels)
        self.generate_header_calendar_year(sql_fragments, business_periods, labels)
        self.generate_header_calendar_month(sql_fragments, business_periods, labels)

    def generate_header_fiscal_year(
        self,
        sql_fragments: List[str],
        business_periods: List[Tuple[int, int]],
        labels: List[str],
    ) -> None:
        """
        Generates a SQL header fragment for fiscal years based on the provided business periods and labels.

        Args:
            sql_fragments (list of str): The list of SQL fragments to which the header fragments will be appended.
            business_periods (list of tuples): A list of tuples where each tuple contains a year and month representing business periods.
            labels (list of str): A list of labels corresponding to the business periods.

        Returns:
            str: A SQL fragment that selects fiscal years with corresponding labels.

        Example:
            business_periods = [(0, 1), (0, 2), (1, 3), (1, 4)]
            labels = ["Label1", "Label2", "Label3", "Label4"]

            This would generate a SQL fragment that maps each fiscal year to the corresponding label from the labels list.
        """
        frags = [
            f"    FiscalYearMinus{year:01d} AS {labels[idx]}"
            for idx, (year, month) in enumerate(business_periods)
        ]

        fragment = "    'fiscal_year' AS DESCRIPTION,\n"
        fragment += ",\n".join(frags)
        fragment += "\nFROM DateCalculations"
        sql_fragments.append(fragment)

    def generate_header_fiscal_month(
        self,
        sql_fragments: List[str],
        business_periods: List[Tuple[int, int]],
        labels: List[str],
    ) -> str:
        """
        Generates a SQL header fragment for fiscal months based on the provided business periods and labels.

        Args:
            sql_fragments (list of str): The list of SQL fragments to which the header fragments will be appended.
            business_periods (list of tuples): A list of tuples where each tuple contains a year and month representing business periods.
            labels (list of str): A list of labels corresponding to the business periods.

        Returns:
            str: A SQL fragment that selects fiscal months with corresponding labels.

        Example:
            business_periods = [(0, 1), (0, 2), (1, 3), (1, 4)]
            labels = ["Label1", "Label2", "Label3", "Label4"]

            This would generate a SQL fragment that maps each fiscal month to the corresponding label from the labels list.
        """
        frags = [
            f"    {month:01d} AS {labels[idx]}"
            for idx, (year, month) in enumerate(business_periods)
        ]

        fragment = "    'fiscal_month' AS DESCRIPTION,\n"
        fragment += ",\n".join(frags)
        fragment += "\nFROM DateCalculations"
        sql_fragments.append(fragment)

    def generate_header_calendar_year(
        self,
        sql_fragments: List[str],
        business_periods: List[Tuple[int, int]],
        labels: List[str],
    ) -> str:
        """
        Generates a SQL header fragment for calendar years based on the provided business periods and labels.

        Args:
            sql_fragments (list of str): The list of SQL fragments to which the header fragments will be appended.
            business_periods (list of tuples): A list of tuples where each tuple contains a year and month representing business periods.
            labels (list of str): A list of labels corresponding to the business periods.

        Returns:
            str: A SQL fragment that selects calendar years with corresponding labels.

        Example:
            business_periods = [(0, 1), (0, 2), (1, 3), (1, 4)]
            labels = ["Label1", "Label2", "Label3", "Label4"]

            This would generate a SQL fragment that maps each calendar year to the corresponding label from the labels list.
        """
        frags = [
            f"    YEAR(CalendarPeriod{idx}) AS {labels[idx]}"
            for idx, (year, month) in enumerate(business_periods)
        ]

        fragment = "    'calendar_year' AS DESCRIPTION,\n"
        fragment += ",\n".join(frags)
        fragment += "\nFROM DateCalculations"
        sql_fragments.append(fragment)

    def generate_header_calendar_month(
        self,
        sql_fragments: List[str],
        business_periods: List[Tuple[int, int]],
        labels: List[str],
    ) -> str:
        """
        Generates a SQL header fragment for calendar months based on the provided business periods and labels.

        Args:
            sql_fragments (list of str): The list of SQL fragments to which the header fragments will be appended.
            business_periods (list of tuples): A list of tuples where each tuple contains a year and month representing business periods.
            labels (list of str): A list of labels corresponding to the business periods.

        Returns:
            str: A SQL fragment that selects calendar months with corresponding labels.

        Example:
            business_periods = [(0, 1), (0, 2), (1, 3), (1, 4)]
            labels = ["Label1", "Label2", "Label3", "Label4"]

            This would generate a SQL fragment that maps each calendar month to the corresponding label from the labels list.
        """
        frags = [
            f"    MONTH(CalendarPeriod{idx}) AS {labels[idx]}"
            for idx, (year, month) in enumerate(business_periods)
        ]

        fragment = "    'calendar_month' AS DESCRIPTION,\n"
        fragment += ",\n".join(frags)
        fragment += "\nFROM DateCalculations"
        sql_fragments.append(fragment)

    def getLines(
        self,
        import_file: str,
    ) -> pd.DataFrame:
        """
        Parse the given XML file and extract specific data into a DataFrame.

        This method performs the following steps:
        1. Parses the XML file.
        2. Finds all entries under 'ttSA_Zeile' and 'ttSA_ZeileSpr'.
        3. Extracts values from 'ttSA_Zeile' entries into a DataFrame.
        4. Extracts values from 'ttSA_ZeileSpr' entries where 'Sprache' is 'D' into another DataFrame.
        5. Merges the two DataFrames on 'ZeilenID'.
        6. Converts the 'ZeilenNr' column to numeric and sorts the DataFrame by 'ZeilenNr'.

        Args:
            import_file (str): The path to the XML file to be parsed.

        Returns:
            pd.DataFrame: A DataFrame containing the merged and sorted data.
        """
        # Parse the XML file
        tree = ET.parse(import_file)
        root = tree.getroot()

        # Find all entries under 'ttSA_Zeile' and 'ttSA_ZeileSpr'
        ttSA_Zeile_entries = root.findall(".//ttSA_Zeile")
        ttSA_ZeileSpr_entries = root.findall(".//ttSA_ZeileSpr")

        # Extract all values in 'ttSA_Zeile'
        ttSA_Zeile_values = []
        for entry in ttSA_Zeile_entries:
            entry_dict = {}
            for elem in entry:
                entry_dict[elem.tag] = elem.text
            ttSA_Zeile_values.append(entry_dict)

        df_ttSA_Zeile = pd.DataFrame(
            ttSA_Zeile_values, columns=["ZeilenID", "ZeilenNr"]
        )

        # Extract all values in 'ttSA_SpalteSpr' where Sprache is 'D'
        ttSA_ZeileSpr_values = []
        for entry in ttSA_ZeileSpr_entries:
            entry_dict = {}
            for elem in entry:
                entry_dict[elem.tag] = elem.text
            if entry_dict.get("Sprache") == "D":
                ttSA_ZeileSpr_values.append(entry_dict)

        df_ttSA_ZeileSpr = pd.DataFrame(
            ttSA_ZeileSpr_values, columns=["ZeilenID", "Bezeichnung1"]
        )

        # Merge the DataFrames on 'SpaltenID'
        df_ttSA_Zeile = df_ttSA_Zeile.merge(df_ttSA_ZeileSpr, on="ZeilenID", how="left")

        df_ttSA_Zeile["ZeilenNr"] = pd.to_numeric(df_ttSA_Zeile["ZeilenNr"])
        df_ttSA_Zeile_sorted = df_ttSA_Zeile.sort_values(by="ZeilenNr")
        return df_ttSA_Zeile_sorted

    def getAccountIDs(self, import_file: str, line_id: int) -> List[int]:
        """
        Extract account ID pairs (Konto_min, Konto_max) from an XML file where the ZeilenID matches the provided line_id.

        Parameters:
        import_file (str): Path to the XML file to be parsed.
        line_id (int): The line ID used to filter the ttSA_Konto entries.

        Returns:
        List[int]: A list of account ids.
        """
        accounts = []

        # Parse the XML file
        tree = ET.parse(import_file)
        root = tree.getroot()

        # Find all entries under 'ttSA_Konto'
        ttSA_Konto_entries = root.findall(".//ttSA_Konto")

        # Filter entries by ZeilenID element value
        for entry in ttSA_Konto_entries:
            zeilen_id = entry.find("ZeilenID")
            if zeilen_id is not None and zeilen_id.text == str(line_id):
                konto_min = entry.find("Konto_min")
                konto_max = entry.find("Konto_max")

                if konto_min is not None and konto_max is not None:
                    konto_min_value = int(konto_min.text)
                    konto_max_value = int(konto_max.text)
                    
                    if konto_min ==konto_max:
                        accounts.append(konto_min_value)
                    else:
                        accounts.extend(range(konto_min_value, konto_max_value + 1))
        
        return accounts

    def generate_sql_fragment(
        self,
        rowdesc: str,
        labels: List[str],
        business_periods: List[Tuple[int, int]],
        account_ids: List[int],
        company: str
    ) -> str:
        """
        Generate a single SQL fragment for a given row description and account IDs.
        
        Parameters:
        rowdesc (str): Description for the current row.
        labels (List[str]): List of labels for the SQL columns.
        business_periods (List[Tuple[int, int]]): List of tuples representing fiscal year and period.
        account_ids (List[int]): List of account IDs.
        company (str): Company ID to be used in the SQL statement.
        
        Returns:
        str: Generated SQL fragment.
        """
        if not account_ids:
            frags = [f"NULL AS {label}" for label in labels]
            fragment = f"    '{rowdesc}' AS DESCRIPTION,\n"
            fragment += ",\n".join(frags)
            fragment += f"""
        FROM 
            DUMMY"""
        else:
            account_ids_str = ",".join(map(str, account_ids))
            frags = [
                f"""    ROUND(
        SUM(
            CASE 
                WHEN FA_MAIN_POST_YEAR = FiscalYearMinus{year:01d}
                    AND FA_MAIN_POST_PERIOD = {month} THEN 
                    FA_MAIN_POST_AMOUNT 
                    * CASE WHEN FA_MAIN_POST_DC_INDICATOR = 'C' THEN 1 ELSE -1 END
                ELSE 
                    0
            END),
        2) AS {labels[idx]}"""
                for idx, (year, month) in enumerate(business_periods)
            ]
            fragment = f"    '{rowdesc}' AS DESCRIPTION,\n"
            fragment += ",\n".join(frags)
            fragment += f"""
        FROM 
            nemo."pa_export" 
        CROSS JOIN
            DateCalculations
        WHERE
            COMPANY = {company}
            AND FA_MAIN_POST_ACCOUNT in ({account_ids_str})
            AND FA_MAIN_POST_DATE >= CalendarPeriod0"""

        return fragment

    def generate_PandL(
        self,
        sql_fragments: List[str],
        business_periods: List[Tuple[int, int]],
        labels: List[str],
        import_file: str,
        column_id: int,
        company: str,
    ) -> None:
        """
        Generate SQL fragments for profit and loss statements based on report lines from an XML file.
        
        Parameters:
        sql_fragments (List[str]): List to store generated SQL fragments.
        business_periods (List[Tuple[int, int]]): List of tuples representing fiscal year and period.
        labels (List[str]): List of labels for the SQL columns.
        import_file (str): Path to the XML file containing report lines.
        column_id (int): Column ID to filter report lines.
        company (str): Company ID to be used in the SQL statement.
        
        Returns:
        None
        """
        # Load report lines from XML file
        df_ttSA_Zeile_sorted = self.getLines(import_file)

        # Iterate lines
        for idx, row in df_ttSA_Zeile_sorted.iterrows():
            # Get description for current row
            rowdesc = row["Bezeichnung1"] if row["Bezeichnung1"] is not None else ""

            # Check whether this is a row with accounts attached
            account_ids = self.getAccountIDs(import_file, row["ZeilenID"])

            # Generate SQL fragment for the current row
            fragment = self.generate_sql_fragment(rowdesc, labels, business_periods, account_ids, company)
            sql_fragments.append(fragment)

    def export(self, select: str, output_file: str) -> None:
        """
        Generates two SQL files from the given select statement. The first file contains the original select statement.
        The second file contains the select statement with 'nemo."pa_export"' replaced by '$schema.$table '.

        Args:
            select (str): The select statement to be written to the files.
            output_file (str): The name of the output file for the original select statement.
                            The modified file will have '_nemo' inserted before '.sql'.
        """
        # Write the original select statement to the specified file
        with open(output_file, "w") as file:
            print(select, file=file)
        print(f"file {output_file} generated")

        # Generate the nemo filename by inserting "_nemo" before ".sql"
        nemo_output_file = output_file.replace(".sql", "_nemo.sql")

        # Write the modified select statement to the nemo file
        with open(nemo_output_file, "w") as nemo_file:
            print(select.replace('nemo."pa_export"', "$schema.$table "), file=nemo_file)
        print(f"file {nemo_output_file} generated")


if __name__ == "__main__":
    gen = SQLGeneratorPL()
    gen.generate_sql()
