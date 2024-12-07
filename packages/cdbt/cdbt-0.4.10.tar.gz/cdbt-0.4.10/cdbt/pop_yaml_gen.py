import ast
import re

import pyperclip

from cdbt.main import ColdBoreCapitalDBT


class BuildCBCUtilsYAML:

    def __init__(self):
        pass

    def build_pop_yaml(self, select_target: str, include_avg: bool = False):

        file_path = self._get_file_path(select_target)

        # Read the file into a string
        with open(file_path, "r") as file:
            file_contents = file.read()

        query_args = self.extract_macro_args(file_contents, "generate_pop_columns")

        if not query_args:
            raise Exception(
                "Macro not found in the file. Please check the macro name and try again."
            )

        column_names = query_args.get("column_names")
        lookback_values = query_args.get("look_back_values")
        grain = query_args.get("grain")
        column_prefix = query_args.get("column_prefix")
        date_field = query_args.get("date_field")

        output = self.build_primary_date_blocks(lookback_values, grain, date_field)

        output += "#####\n#Column Data\n####"

        output += self.build_pop_lag_output(
            column_names, lookback_values, grain, column_prefix, include_avg
        )

        print(output)

        print("\n\nResults copied to clipboard\n")

        pyperclip.copy(output)

    def build_ma_yaml(self, select_target: str):
        file_path = self._get_file_path(select_target)
        # Read the file into a string
        with open(file_path, "r") as file:
            file_contents = file.read()

        query_args = self.extract_macro_args(file_contents, "generate_ma_columns")
        if not query_args:
            raise Exception(
                "Macro not found in the file. Please check the macro name and try again."
            )
        column_names = query_args.get("column_names")
        ma_windows = query_args.get("ma_windows")
        grain = query_args.get("grain")
        output = self.build_ma_columns(column_names, ma_windows, grain)
        print(output)
        print("\n\nResults copied to clipboard\n")
        pyperclip.copy(output)

    def _get_file_path(self, select_target: str) -> str:
        cbc = ColdBoreCapitalDBT()
        args = [
            "-s",
            select_target,
            "--exclude",
            "path:tests/* resource_type:test",
            "--output-keys",
            "original_file_path",
        ]

        models_ls_json = cbc.dbt_ls_to_json(args)
        if len(models_ls_json) > 1:
            raise Exception(
                "Please don" "t select more than one model for this function."
            )
        file_path = models_ls_json[0]["original_file_path"]
        return file_path

    def extract_macro_args(self, query: str, macro_name: str):
        # remove newlines
        query = query.replace("\n", "").replace(" ", "")
        pattern = rf"cbc_utils\.{macro_name}\((.*?)\)"
        match = re.search(pattern, query, re.DOTALL)

        if not match:
            return None

        args = match.group(1)
        args_dict = {}

        # Function to split arguments without disturbing the nested structures
        def split_args(args_str):
            depth = 0
            current_arg = []
            result = []
            in_string = False
            escape = False

            for char in args_str:
                if char == "," and depth == 0 and not in_string:
                    result.append("".join(current_arg).strip())
                    current_arg = []
                    continue

                current_arg.append(char)

                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == '"' or char == "'":
                    if in_string:
                        in_string = False
                    else:
                        in_string = True
                elif char == "{" or char == "[" or char == "(":
                    if not in_string:
                        depth += 1
                elif char == "}" or char == "]" or char == ")":
                    if not in_string:
                        depth -= 1

            if current_arg:
                result.append("".join(current_arg).strip())
            return result

        arg_pairs = split_args(args)

        for pair in arg_pairs:
            key, value = pair.split("=")
            key = key.strip()
            value = value.strip()

            # Convert the value from string to Python object (e.g., list, str, etc.)
            if value.startswith("[") or value.startswith("{"):
                value = ast.literal_eval(value)
            elif value.startswith("'") or value.startswith('"'):
                value = value[1:-1]

            args_dict[key] = value

        return args_dict

    def build_pop_lag_output(
        self,
        column_names,
        look_back_values,
        grain,
        column_prefix=None,
        include_avg=False,
    ):
        output = ""

        grain_lookup = {
            "d": "Days",
            "w": "Weeks",
            "m": "Months",
            "q": "Quarters",
            "y": "Years",
        }

        grain_str = grain_lookup.get(grain, grain)

        for column_name in column_names:
            for look_back_val in look_back_values:
                if "revenue" in column_name.lower() or "cost" in column_name.lower():
                    format_str = 'format: "usd"'
                else:
                    format_str = ""
                if column_prefix:
                    column_alias = (
                        f"{column_prefix}_{column_name}_{look_back_val}{grain}_pop"
                    )
                else:
                    column_alias = f"{column_name}_{look_back_val}{grain}_pop"
                column_name_title_case = column_name.replace("_", " ").title()
                if include_avg:
                    # noqa: disable=All
                    avg_block = f"""
                        {column_alias}_avg_pop:
                            label: "{column_name_title_case} - PoP {look_back_val} {grain_str} - Average"
                            description: "Average for prior period {column_name_title_case} looking back {look_back_val} {grain_str.lower()}"
                            group_label: "Period Over Period - {look_back_val} {grain_str}"
                            type: average
                            round: 0
                            compact: thousands
                        {format_str}"""
                    # noqa: enable=All
                else:
                    avg_block = ""

                output_tmp = f"""
                - name: {column_alias}
                  meta:
                      dimension:
                          type: number
                          hidden: true

                      metrics:
                          {column_alias}_sum_pop:
                              label: "{column_name_title_case} - PoP {look_back_val} {grain_str}"
                              group_label: "Period Over Period - {look_back_val} {grain_str}"
                              type: sum
                              description: "Total for prior period {column_name_title_case} looking back {look_back_val} {grain_str.lower()}"
                              round: 0
                              compact: thousands
                              {format_str}{avg_block}"""

                output += output_tmp

        output += (
            "\n#####\n#Reminder, remove the compact:thousands where not needed\n####"
        )

        return output

    def build_ma_columns(self, column_names, ma_windows, grain):
        output = ""

        grain_lookup = {
            "d": "Day",
            "w": "Week",
            "m": "Month",
            "q": "Quarter",
            "y": "Year",
        }

        grain_str = grain_lookup.get(grain, grain)

        for column_name in column_names:
            for days in ma_windows:
                if "revenue" in column_name.lower() or "cost" in column_name.lower():
                    format_str = 'format: "usd"'
                else:
                    format_str = ""
                column_alias = f"{column_name}_{days}{grain}_ma"
                column_name_title_case = column_name.replace("_", " ").title()

                output_tmp = f"""
                - name: {column_alias}
                  meta:
                      dimension:
                          hidden: true
                      metrics:
                          {column_alias}_sum:
                              label: "{column_name_title_case} - {days} {grain_str} MA"
                              group_label: "Moving Average"
                              type: sum
                              description: "{days} {grain_str.lower()} moving average for {column_name_title_case}."
                              round: 0
                              compact: thousands
                              {format_str}"""

                output += output_tmp

        output += (
            "\n#####\n#Reminder, remove the compact:thousands where not needed\n####"
        )

        return output

    def build_primary_date_blocks(self, look_back_values, grain, date_field):

        grain_lookup = {
            "d": "Days",
            "w": "Weeks",
            "m": "Months",
            "q": "Quarters",
            "y": "Years",
        }

        grain_str = grain_lookup.get(grain, grain)

        output = """
            additional_dimensions:"""

        for look_back_val in look_back_values:
            output_tmp = f"""
                period_{look_back_val}_{grain_str.lower()}:
                  type: string
                  label: "Period - {look_back_val} {grain_str}"
                  sql: "case when floor(datediff({grain_str.lower()}, {date_field}, current_date()) / {look_back_val}) = 0 then 'Current Period'
                        else 'Period ' || (floor(datediff({grain_str.lower()}, {date_field}, current_date()) / {look_back_val})+1)::string end"
                  group_label: "Period Indicators"
            """

            output += output_tmp

        output += f"""
            metrics:
                {grain_str.lower()}_in_period:
                  type: number
                  label: "Days in Period"
                  sql: "(datediff('{grain_str.lower()}', min({date_field}), max({date_field})) + 1)"
                  group_label: "Period Indicators"

                sort_order:
                  type: number
                  label: "Period Sort Order"
                  # Note an extra max is added here to ensure that the value is treated as an aggregate and doesn't require
                  # a group by.
                  sql: "floor(max(datediff({grain_str.lower()}, {date_field}, current_date())+1) / ${{{grain_str.lower()}_in_period}})"
                  group_label: "Period Indicators"
        """

        return output


# # Path to your JSON file
# config_file_path = 'build_pop_outputs_config.json'
#
# # Read the configuration
# with open(config_file_path, 'r') as file:
#     config = json.load(file)
#
# _column_names = config['column_names']
# _look_back_values = config['look_back_values']
# _grain = config['grain']
# _date_field =config['date_field']
#
# print('############ Primary Date additional dims ############\n\n\n')
# print(build_primary_date_blocks(look_back_values=_look_back_values, grain=_grain,date_field=_date_field))
# print('\n\n\n############ Primary Date additional dims ############\n\n\n')
# print(build_pop_lag_output(column_names=_column_names, look_back_values=_look_back_values, grain=_grain))
