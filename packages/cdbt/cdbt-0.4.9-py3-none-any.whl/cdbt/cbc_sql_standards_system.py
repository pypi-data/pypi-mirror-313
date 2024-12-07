import os
import re
from typing import List
from typing import Tuple

import pyperclip
import wordninja
from dotenv import load_dotenv

from cdbt.main import ColdBoreCapitalDBT

load_dotenv()


class SQLModelCleaner(ColdBoreCapitalDBT):
    def __init__(self):
        super().__init__()
        pass

    def main(
        self, select, split_names, remove_airbyte, overwrite, files_override=None
    ) -> None:
        """
        Reads the SQL file, cleans up merged words, and sorts lines based on specified criteria.
        """
        if files_override:
            if "," in files_override:
                files = files_override.split(",")
            else:
                files = [files_override]
        else:
            args = [
                "--select",
                select,
                "--exclude",
                "path:tests/* resource_type:test resource_type:seed resource_type:snapshot",
                "--output-keys",
                "original_file_path",
            ]
            # Read the file content
            files = self.dbt_ls_to_json(args)
            files = [x["original_file_path"] for x in files]

        for file_path in files:
            directory, filename = self._extract_path_and_filename(file_path)
            all_lines = self._read_sql_file_to_lines(os.path.join(directory, filename))

            all_lines = self._remove_empty_lines(all_lines)

            if remove_airbyte:
                # Remove Airbyte specific lines
                all_lines = self._remove_airbyte_specific_lines(all_lines)

            lines, lines_start, lines_end = self._read_sort_section(all_lines)

            lines = self._remove_trailing_comma(lines)

            # Sort all lines alphabetically first.
            lines = self._sort_lines_alphabetically(lines)

            lines_w_dtype = self._extract_datatypes(lines)

            if split_names:
                # Clean up merged words
                lines = self._clean_merged_words(lines_w_dtype)

            # Sort the lines according to the logic order
            sorted_lines = self._sort_sql_lines(lines)

            sorted_lines = self._alias_id_column(sorted_lines, filename.split(".")[0])

            sorted_lines = self._add_trailing_comma(sorted_lines)

            all_lines = self._insert_sorted_lines(
                all_lines, sorted_lines, lines_start, lines_end
            )

            # if self._args.approve:
            #     # Print the cleaned and sorted lines to the console and prompt the user to approve the changes
            #     self._approve_output(all_lines)
            self._write_sql_file(all_lines, directory, filename, overwrite)

    def sort_clipboard_lines(self):
        lines = pyperclip.paste().split("\n")

        lines = self._remove_trailing_comma(lines)

        # Sort all lines alphabetically first.
        lines = self._sort_lines_alphabetically(lines)

        sorted_lines = self._sort_sql_lines(lines)

        pyperclip.copy("\n".join(sorted_lines))

    @staticmethod
    def _extract_path_and_filename(file_path):
        directory, filename = os.path.split(file_path)
        return directory, filename

    @staticmethod
    def _read_sql_file_to_lines(file_path):
        with open(file_path, "r") as file:
            all_lines = file.readlines()
        return all_lines

    @staticmethod
    def _remove_empty_lines(all_lines: list) -> list:
        """
        Remove empty lines that are just \n
        Args:
            all_lines: A list containing all the selected lines.

        Returns:
            A list with the empty lines removed.
        """
        all_lines = [x for x in all_lines if x.strip() != "\n"]
        return all_lines

    @staticmethod
    def _read_sort_section(all_lines) -> Tuple[List[str], int, int]:
        """
        Reads the SQL file and returns the lines between `final as (` and `from raw_source` as a list of strings.

        Returns:
            List[str]: The lines of the SQL file between the specified sections.
        """
        begin_capture = False
        lines_to_return = []
        start_index = 0
        end_index = 0
        for ix, line in enumerate(all_lines):
            # Check for the start of the section we're interested in
            if "final as (" in line.lower():
                start_index = ix + 3  # account for the /n and 'select' in the line
                begin_capture = True
                continue  # Skip the line with 'final as ('
            # Check for the end of the section we're interested in
            elif "from raw_source" in line.lower():
                end_index = ix - 1  # account for a /n at the bottom.
                break  # Stop capturing when 'from raw_source' is found
            # Capture lines if we are within the section
            if begin_capture:
                lines_to_return.append(line)

        # Strip the \n and 'select' from the top and a '\n' from the bottom.
        lines_to_return = lines_to_return[2:-1]
        return lines_to_return, start_index, end_index

    @staticmethod
    def _remove_trailing_comma(lines: List[str]) -> List[str]:
        """
        Removes trailing commas from lines.

        Args:
            lines (List[str]): The lines of the SQL file to clean.

        Returns:
            List[str]: The cleaned lines with trailing commas removed.
        """
        cleaned_lines = []
        for line in lines:
            if line.endswith(",\n"):
                line = line[:-2]
            elif line.endswith("\n"):
                line = line[:-1]
            cleaned_lines.append(line)
        return cleaned_lines

    def _clean_merged_words(self, lines: List[List[str]]) -> List[str]:
        """
        Identifies merged words in SQL aliases and separates them using the OpenAI API.

        Args:
            lines (List[str]): The lines of the SQL file to clean.

        Returns:
            List[str]: The cleaned lines with separated alias words.
        """
        pattern = re.compile(r"\b(as\s+)(?P<alias>\w+)(,?)\b", re.IGNORECASE)

        # Extract aliases that are merged words
        merged_words = []
        for line in lines:

            match = pattern.search(line[0])
            if match:
                alias = match.group("alias")
                alias = self._ensure_is_flag_split(alias)
                merged_words.append(
                    (alias, match.start("alias"), match.end("alias"), line[0], line[1])
                )

        # Call OpenAI API to separate words
        separated_words = self._split_words([mw[0] for mw in merged_words])
        output = []
        # Replace merged words with separated words in the lines
        for (alias, start, end, orig_line, data_type), separated in zip(
            merged_words, separated_words
        ):
            separated_with_underscores = separated.replace(
                " ", "_"
            )  # Replace spaces with underscores
            new_line = orig_line[:start] + separated_with_underscores + orig_line[end:]
            # make sure date or datetime lines end in at
            new_line = self._check_that_datetime_contains_at(new_line, data_type)
            new_line = self._check_that_bool_starts_with_is(new_line, data_type)
            output.append(new_line)

        return output

    @staticmethod
    def _ensure_is_flag_split(alias: str):
        """
        Ensures that if the line starts with is, it will be split into `is_` and the rest of the line.

        Args:
            alias (str): The line to check.

        Returns:
            str: The line with is_ prefixed if necessary.
        """
        if alias.startswith("is"):
            alias = "is_" + alias[2:]
            return alias
        else:
            return alias

    @staticmethod
    def _check_that_datetime_contains_at(line: str, data_type: str) -> str:
        """
        Checks that the line ends in _at if the data type is a date type.

        Args:
            line (str): The line to check.
            data_type (str): The data type of the line.

        Returns:
            str: The line with _at appended if necessary.
        """
        list_of_date_type = [
            "date",
            "datetime",
            "timestamp",
            "timestamp_tz",
            "time",
            "timestamp_ltz",
            "timestamp_ntz",
        ]
        if data_type in list_of_date_type:
            if not line.endswith("_at"):
                return line + "_at"
        return line

    def _check_that_bool_starts_with_is(self, line: str, data_type: str) -> str:
        """
        Checks that the alias starts with is_ if the data type is a bool type.

        Args:
            line (str): The line to check.
            data_type (str): The data type of the line.

        Returns:
            str: The line with is_ prepended if necessary.
        """
        pattern = r"\bas\s+(\w+)"

        # Search for the alias in the string
        match = re.search(pattern, line)
        if not match:
            raise ValueError("No alias found in the string")

        # Extract the alias
        alias = match.group(1)

        # Apply the transformation function to the alias
        transformed_alias = self._is_transform_function(alias, data_type)

        # Replace the original alias with the transformed alias
        transformed_string = re.sub(pattern, f" as {transformed_alias}", line)

        return transformed_string

    @staticmethod
    def _is_transform_function(alias: str, data_type: str) -> str:
        """

        Args:
            alias:

        Returns:

        """
        list_of_date_type = ["boolean", "bool"]
        if data_type in list_of_date_type:
            if not alias.startswith("is_"):
                return "is_" + alias
        return alias

    @staticmethod
    def _extract_datatypes(lines: List[str]) -> List[List[str]]:
        pattern = re.compile(r"::(\w+)")
        lines_w_dtype = []

        for line in lines:
            if line.strip().startswith("--"):
                lines_w_dtype.append([line, "comment"])
            else:
                match = pattern.search(line)
                if match:
                    data_type = match.group(1)
                    lines_w_dtype.append([line, data_type])
                else:
                    raise Exception(f"SQL Line {line} does not have a datatype.")

        return lines_w_dtype

    @staticmethod
    def _split_words(words: List[str]) -> List[str]:
        """
        Calls the OpenAI API to separate merged words.

        Args:
            words (List[str]): The list of merged words to separate.

        Returns:
            List[str]: The separated words.
        """
        # lm = wordninja.LanguageModel('wordninja_custom.txt.gz')
        lm = wordninja
        responses = []
        for word in words:
            split_words = lm.split(word)
            if len(split_words) > 1:
                final_word = "_".join(split_words)
            else:
                final_word = word
            responses.append(final_word)
        return responses

    @staticmethod
    def _remove_airbyte_specific_lines(lines: List[str]) -> List[str]:
        """
        Removes specific lines containing unwanted SQL patterns related to Airbyte.

        Args:
            lines (List[str]): The lines of the SQL file to clean.

        Returns:
            List[str]: The lines of the SQL file with the specified lines removed.
        """
        patterns_to_remove = [
            re.escape('"_AIRBYTE_RAW_ID"::varchar as airbyte_raw_id,'),
            re.escape('"_AIRBYTE_EXTRACTED_AT"::timestamp_tz as airbyte_extracted_at,'),
            re.escape('"_AIRBYTE_META"::variant as airbyte_meta,'),
        ]
        cleaned_lines = [
            line
            for line in lines
            if not any(re.search(pattern, line) for pattern in patterns_to_remove)
        ]
        return cleaned_lines

    @staticmethod
    def _sort_lines_alphabetically(lines: List[str]) -> List[str]:
        """
        Sorts the lines of the SQL file alphabetically.

        Args:
            lines (List[str]): The lines of the SQL file to sort.

        Returns:
            List[str]: The alphabetically sorted lines of the SQL file.
        """
        return sorted(lines, key=lambda line: line.lower())

    @staticmethod
    def _sort_sql_lines(lines: List[str]) -> List[str]:
        """
        Sorts the lines of the SQL file based on the specified criteria.

        Args:
            lines (List[str]): The lines of the SQL file to sort.

        Returns:
            List[str]: The sorted lines of the SQL file.
        """

        # Define sorting criteria
        def sort_criteria(line: str) -> Tuple[int, str]:
            lower_line = line.lower()
            if lower_line.startswith("ID"):
                return 0, lower_line
            elif lower_line.endswith(" as id"):
                return 1, lower_line
            elif lower_line.endswith("_id"):
                return 2, lower_line
            elif lower_line.endswith("_at"):
                return 3, lower_line
            elif "is_" in lower_line:
                return 4, lower_line
            elif "_airbyte" in lower_line:
                return 6, lower_line
            else:
                return 5, lower_line

        # Sort the lines based on the criteria
        sorted_lines = sorted(lines, key=sort_criteria)
        return sorted_lines

    @staticmethod
    def _alias_id_column(lines: List[str], model_name: str) -> List[str]:
        """
        Adds the name of the model to ID column. For example, id becomes appointment_id

        Args:
            lines (List[str]): The lines of the SQL file to clean.
            model_name (str): The name of the model to append.

        Returns:
            List[str]: The cleaned lines with trailing commas removed.
        """
        id_line = lines[0]
        parts = id_line.split(" as ")
        if len(parts) == 2:
            new_id_line = f"{parts[0]} as {model_name}_{parts[1]}"
        else:
            raise Exception(f"ID line {id_line} does not have an alias.")
        lines[0] = new_id_line
        return lines

    @staticmethod
    def _add_trailing_comma(lines: List[str]) -> List[str]:
        """
        Adds trailing comma and /n to all lines except for the last. The last line is only given a /n.

        Args:
            lines (List[str]): The lines of the SQL file to clean.

        Returns:
            List[str]: The cleaned lines with trailing commas added.
        """
        cleaned_lines = []
        for ix, line in enumerate(lines):
            if ix < len(lines) - 1:
                line = line + ",\n"
            else:
                line = line + "\n"
            cleaned_lines.append(line)
        return cleaned_lines

    @staticmethod
    def _insert_sorted_lines(
        full_lines: List[str], sorted_lines: List[str], start_ix: int, end_ix: int
    ) -> List[str]:
        """
        Inserts the sorted lines back into the full list of lines.

        Args:
            full_lines (List[str]): The full list of lines to insert the sorted lines into.
            sorted_lines (List[str]): The sorted lines to insert into the full list of lines.
            start_ix (int): The starting index of the section to insert the sorted lines into.
            end_ix (int): The ending index of the section to insert the sorted lines into.

        Returns:
            List[str]: The full list of lines with the sorted lines inserted.
        """
        full_lines = full_lines[:start_ix] + sorted_lines + full_lines[end_ix:]
        return full_lines

    @staticmethod
    def _approve_output(full_lines: List[str]) -> None:
        """
        Prints the cleaned and sorted lines to the console and prompts the user to approve the changes.

        Args:
            full_lines (List[str]): The cleaned and sorted lines to print to the console.
        """
        print("".join(full_lines))
        approved = input("Approve changes? (y/n): ")
        if approved.lower() != "y":
            raise Exception("Changes not approved.")

    @staticmethod
    def _write_sql_file(
        lines: List[str], directory: str, filename: str, overwrite: str
    ) -> None:
        """
        Writes the cleaned and sorted lines back to the SQL file.

        Args:
            lines (List[str]): The cleaned and sorted lines to write to the file.
        """
        subfolder = "_cleaned_files"
        if not overwrite:
            directory = os.path.join(directory, subfolder)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, filename), "w") as file:
            file.writelines(lines)


def cli_function():
    c = SQLModelCleaner()
    # c.main(select='Test',
    #        remove_airbyte=False,
    #        overwrite=False,
    #        files_override='tests/cbc_sql_standards_test_file.sql')

    c.main(
        select="stg_wt_schedule_details",
        remove_airbyte=False,
        overwrite=False,
        files_override=None,
    )


if __name__ == "__main__":
    """
    IMPORTANT. If you are debugging this in pycharm, you need to edit the run config, go to more options,
    then turn on emulate terminal.
    """
    cli_function()
