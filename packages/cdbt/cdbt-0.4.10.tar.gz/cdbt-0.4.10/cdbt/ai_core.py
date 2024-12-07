import os
import re
import subprocess
from typing import Dict
from typing import List

import snowflake.connector as snow
from dotenv import find_dotenv
from dotenv import load_dotenv

from cdbt.main import ColdBoreCapitalDBT
from cdbt.prompts import Prompts

load_dotenv(find_dotenv("../.env"))
load_dotenv(find_dotenv(".env"))
# Have to load env before import openai package.
# flake8: noqa: E402
import openai


class AiCore:

    def __init__(self):
        self.model = "o1-mini"
        # Make sure you have OPENAI_API_KEY set in your environment variables.
        self.client = openai.OpenAI()

        self.prompts = Prompts()
        self._conn = None
        self._cur = None
        self._create_snowflake_connection()

    def _create_snowflake_connection(self):
        self._conn = snow.connect(
            account=os.environ.get("DATACOVES__MAIN__ACCOUNT"),
            password=os.environ.get("DATACOVES__MAIN__PASSWORD"),
            schema=os.environ.get("DATACOVES__MAIN__SCHEMA"),
            user=os.environ.get("DATACOVES__MAIN__USER"),
            warehouse=os.environ.get("DATACOVES__MAIN__WAREHOUSE"),
            database=os.environ.get("DATACOVES__MAIN__DATABASE"),
            role=os.environ.get("DATACOVES__MAIN__ROLE"),
        )

        self._cur = self._conn.cursor()

    def send_message(self, _messages: List[Dict[str, str]]) -> object:
        print("Sending to API")
        completion = self.client.chat.completions.create(
            model=self.model, messages=_messages
        )
        return completion.choices[0].message.content

    @staticmethod
    def read_file(path: str) -> str:
        with open(path, "r") as file:
            return file.read()

    def _get_file_path(self, model_name):
        cdbt_main = ColdBoreCapitalDBT()
        # This will get the path of the model. note, that unit tests show up as models, so must be excluded via the folder.
        #
        args = [
            "--select",
            model_name,
            "--exclude",
            "path:tests/* resource_type:test",
            "--output-keys",
            "original_file_path",
        ]
        model_ls_json = cdbt_main.dbt_ls_to_json(args)
        file_path = model_ls_json[0]["original_file_path"]
        return file_path

    @staticmethod
    def is_file_committed(file_path):
        try:
            # Check the Git status of the file
            subprocess.run(
                ["git", "ls-files", "--error-unmatch", file_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            # If the file is tracked, check if it has any modifications
            status_result = subprocess.run(
                ["git", "status", "--porcelain", file_path], stdout=subprocess.PIPE
            )
            status_output = status_result.stdout.decode().strip()
            # If the output is empty, file is committed and has no modifications
            return len(status_output) == 0
        except subprocess.CalledProcessError:
            # The file is either untracked or does not exist
            return False

    def _get_sample_data_from_snowflake(self, model_names: List[str]):
        """
        Compiles the target model to SQL, then breaks out each sub query and CTE into a separate SQL strings, executing
        each to get a sample of the data.
        Args:
            model_name: A list of target model names to pull sample data from.

        Returns:

        """
        cdbt_main = ColdBoreCapitalDBT()
        sample_results = {}
        for model_name in model_names:
            print(f"Getting sample data for {model_name}")
            args = ["--select", model_name]
            cmd = "compile"
            results = cdbt_main.execute_dbt_command_capture(cmd, args)
            extracted_sql = self.extract_sql(results)
            sample_sql = self.build_sample_sql(extracted_sql)
            try:
                self._cur.execute(sample_sql)
            except snow.DatabaseError as e:
                print(f"Error executing sample SQL for {model_name}")
                print(e)
                print("\n\n" + sample_sql + "\n\n")
                raise e
            tmp_df = self._cur.fetch_pandas_all()
            sample_results[model_name] = tmp_df.to_csv(index=False)

        return sample_results

    @staticmethod
    def build_sample_sql(sql: str) -> str:
        sql = f"""
            with tgt_table as (
                {sql}
            )
            select *
            from tgt_table
            sample (75 rows)
            """
        return sql

    @staticmethod
    def extract_sql(log):
        sql_lines = [line for line in log.splitlines() if not re.match(r"--\s.*", line)]

        keyword_line_index = 0
        for i, line in enumerate(sql_lines):
            if "Compiled node" in line:
                keyword_line_index = i + 1
                break

        sql_lines = sql_lines[keyword_line_index:]

        # Join the remaining lines and remove escape sequences
        sql = "\n".join(sql_lines).replace("\x1b[0m", "").strip()
        return sql
