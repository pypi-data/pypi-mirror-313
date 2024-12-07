import re

import click

from cdbt.build_dbt_docs_ai import BuildDBTDocs
from cdbt.build_unit_test_data_ai import BuildUnitTestDataAI
from cdbt.cbc_sql_standards_system import SQLModelCleaner
from cdbt.main import ColdBoreCapitalDBT
from cdbt.pop_yaml_gen import BuildCBCUtilsYAML
from cdbt.sort_yaml_fields import SortYAML

cdbt_class = ColdBoreCapitalDBT()


# Create a Click group
class CustomCmdLoader(click.Group):

    def get_command(self, ctx, cmd_name):
        ctx.ensure_object(dict)

        # Match commands ending with + optionally followed by a number, such as 'sbuild+' or 'sbuild+3'
        suffix_match = re.match(r"(.+)\+(\d*)$", cmd_name)
        if suffix_match:
            cmd_name, count = suffix_match.groups()
            ctx.obj["build_children"] = True
            ctx.obj["build_children_count"] = (
                int(count) if count else None
            )  # Default to 1 if no number is specified

        # Match commands starting with a number followed by +, such as '3+sbuild'
        prefix_match = re.match(r"(\d+)\+(.+)", cmd_name)
        if prefix_match:
            count, cmd_name = prefix_match.groups()
            ctx.obj["build_parents"] = True
            ctx.obj["build_parents_count"] = (
                int(count) if count else None
            )  # Default to 1 if no number is specified

        return click.Group.get_command(self, ctx, cmd_name)

    def list_commands(self, ctx):
        # List of all commands
        return [
            "help",
            "build",
            "trun",
            "run",
            "test",
            "compile",
            "clip-compile",
            "unittest",
            "sbuild",
            "pbuild",
            "gbuild",
            "build-docs",
            "build-unit",
            "ld-preview",
            "clean-stg",
            "clean-clip",
            "pre-commit",
            "pop-yaml",
            "ma-yaml",
            "sort-yaml",
        ]


cdbt = CustomCmdLoader()


@cdbt.command()
@click.option(
    "--full-refresh", "-f", is_flag=True, help="Run a full refresh on all models."
)
@click.option("--select", "-s", type=str, help="DBT style select string")
@click.option("--fail-fast", is_flag=True, help="Fail fast on errors.")
@click.option(
    "--threads", "-t", type=int, help="Number of threads to use during DBT operations."
)
@click.pass_context
def build(ctx, full_refresh, select, fail_fast, threads):
    """Execute a DBT build command passthrough."""
    cdbt_class.build(ctx, full_refresh, select, fail_fast, threads)


@cdbt.command()
@click.option(
    "--full-refresh", "-f", is_flag=True, help="Run a full refresh on all models."
)
@click.option("--select", "-s", type=str, help="DBT style select string")
@click.option("--fail-fast", is_flag=True, help="Fail fast on errors.")
@click.option(
    "--threads", "-t", type=int, help="Number of threads to use during DBT operations."
)
@click.pass_context
def trun(ctx, full_refresh, select, fail_fast, threads):
    """Execute a DBT run, then test command."""
    cdbt_class.trun(ctx, full_refresh, select, fail_fast, threads)


@cdbt.command()
@click.option(
    "--full-refresh", "-f", is_flag=True, help="Run a full refresh on all models."
)
@click.option("--select", "-s", type=str, help="DBT style select string")
@click.option("--fail-fast", is_flag=True, help="Fail fast on errors.")
@click.option(
    "--threads", "-t", type=int, help="Number of threads to use during DBT operations."
)
@click.pass_context
def run(ctx, full_refresh, select, fail_fast, threads):
    """Pass through to DBT run command."""
    cdbt_class.run(ctx, full_refresh, select, fail_fast, threads)


@cdbt.command()
@click.option("--select", "-s", type=str, help="DBT style select string")
@click.option("--fail-fast", is_flag=True, help="Fail fast on errors.")
@click.option(
    "--threads", "-t", type=int, help="Number of threads to use during DBT operations."
)
@click.pass_context
def test(ctx, select, fail_fast, threads):
    """Pass through to DBT test command."""
    cdbt_class.test(ctx, select, fail_fast, threads)


@cdbt.command()
@click.option("--select", "-s", type=str, help="DBT style select string")
@click.option("--fail-fast", is_flag=True, help="Fail fast on errors.")
@click.pass_context
def unittest(ctx, select, fail_fast):
    """Run unit tests on models."""
    cdbt_class.unittest(ctx, select, fail_fast)


@cdbt.command()
@click.option("--select", "-s", type=str, help="Name of the model(s) to compile.")
@click.pass_context
def compile(ctx, select):
    """Pass through to DBT compile."""
    cdbt_class.compile(ctx, select)


@cdbt.command()
@click.option(
    "--select",
    "-s",
    type=str,
    help="Name of the model to compile. Recommend only running one.",
)
@click.pass_context
def clip_compile(ctx, select):
    """Pass through to DBT compile."""
    cdbt_class.clip_compile(ctx, select)


@cdbt.command()
@click.option(
    "--full-refresh",
    "-f",
    is_flag=True,
    help="Force a full refresh on all models in build scope.",
)
@click.option(
    "--threads", "-t", type=int, help="Number of threads to use during DBT operations."
)
@click.pass_context
def sbuild(ctx, full_refresh, threads):
    """Build models based on changes in current state since last build."""
    cdbt_class.sbuild(ctx, full_refresh, threads)


@cdbt.command()
@click.option(
    "--full-refresh",
    "-f",
    is_flag=True,
    help="Force a full refresh on all models in build scope.",
)
@click.option(
    "--threads", "-t", type=int, help="Number of threads to use during DBT operations."
)
@click.option(
    "--skip-dl",
    "--sd",
    is_flag=True,
    help="Skip downloading the manifest file from Snowflake. Use the one that was already downloaded.",
)
@click.pass_context
def pbuild(ctx, full_refresh, threads, skip_dl):
    """Build models based on changes from production to current branch."""
    cdbt_class.pbuild(ctx, full_refresh, threads, skip_dl)


@cdbt.command()
@click.option(
    "--main",
    "-m",
    is_flag=True,
    help="Build all models vs diff to the main branch. Make sure to pull main so it"
    "s up-to-date.",
)
@click.option(
    "--full-refresh",
    "-f",
    is_flag=True,
    help="Force a full refresh on all models in build scope.",
)
@click.option(
    "--threads", "-t", type=int, help="Number of threads to use during DBT operations."
)
@click.pass_context
def gbuild(ctx, main, full_refresh, threads):
    """Build models based on Git changes from production to current branch."""
    cdbt_class.gbuild(ctx, main, full_refresh, threads)


@cdbt.command()
@click.option(
    "--select",
    "-s",
    type=str,
    required=True,
    help="Name of the model to build unit test data for.",
)
@click.pass_context
def build_docs(ctx, select):
    """Build dbt YML model docs for a model. This command will sample the database."""
    dbt_docs = BuildDBTDocs()
    dbt_docs.main(select)


@cdbt.command()
@click.option(
    "--select",
    "-s",
    type=str,
    required=True,
    help="Name of the model to build unit test data for.",
)
@click.pass_context
def build_unit(ctx, select):
    """Build unit test mock and expect data for a model. This command will sample the database."""
    build_unit_test_data = BuildUnitTestDataAI()
    build_unit_test_data.main(select)


@cdbt.command()
@click.option(
    "--select",
    "-s",
    type=str,
    help="Name of the model to start a lightdash preview for. If not provided, all models will be previewed.",
)
@click.option(
    "--name",
    "-n",
    type=str,
    help="Name of the lightdash preview. If no name given, the preview will take the name of the current branch.",
)
@click.option(
    "--l43",
    is_flag=True,
    help="Include L3 and L4 models in the preview. Default is False.",
)
@click.pass_context
def ld_preview(ctx, select, name, l43):
    """Start a lightdash preview for a model."""
    preview_name = name
    cdbt_class.lightdash_start_preview(ctx, select, preview_name, l43)


@cdbt.command()
@click.option(
    "--select",
    "-s",
    type=str,
    help="Name of the model(s) to format. Takes precidence over --all and --main.",
)
@click.option("--all", "-a", is_flag=True, help="Format all models.")
@click.option(
    "--main",
    "-m",
    is_flag=True,
    help="Format all models vs diff to the main branch. Make sure to pull main so it"
    "s up-to-date.",
)
@click.pass_context
def format(ctx, select, all, main):
    """Format models using sqlfluff."""
    cdbt_class.format(ctx, select, all, main)


@cdbt.command()
@click.option("--select", "-s", type=str, help="Names of the model(s) to clean.")
@click.option(
    "--split-names", is_flag=True, help="Split names like isupdated into is_updated."
)
@click.option(
    "--remove-airbyte",
    is_flag=True,
    help="Whether to remove Airbyte specific lines. Default is True.",
)
@click.option(
    "--overwrite",
    is_flag=True,
    help="Will overwrite the files. If not set, files will be saved to a folder.",
)
@click.pass_context
def clean_stg(select, split_names, remove_airbyte, overwrite):
    """Designed to clean files in the L1_stg folders only"""
    sql_model_cleaner = SQLModelCleaner()
    sql_model_cleaner.main(select, split_names, remove_airbyte, overwrite)


@cdbt.command()
def clean_clip():
    """This will clean and sort a series of select statements from your clipboard and put back to clipboard when done."""
    sql_model_cleaner = SQLModelCleaner()
    sql_model_cleaner.sort_clipboard_lines()


@cdbt.command()
@click.option(
    "--select", "-s", type=str, help="Names of the model to build PoP YAML string for."
)
@click.option("--include-avg", is_flag=True, help="Include metric blocks for averages.")
def pop_yaml(select, include_avg):
    """Build the YAML PoP macro columns for a given model targeted in the select statement."""
    yml = BuildCBCUtilsYAML()
    yml.build_pop_yaml(select, include_avg)


@cdbt.command()
@click.option(
    "--select", "-s", type=str, help="Names of the model to build MA YAML string for."
)
def ma_yaml(select):
    """Build the YAML Moving Avearage macro columns for a given model targeted in the select statement."""
    yml = BuildCBCUtilsYAML()
    yml.build_ma_yaml(select)


@cdbt.command()
@click.option("--select", "-s", type=str, help="Name of model to sort YML columns for.")
@click.option("--all-files", is_flag=True, help="Sort all YML files in the project.")
@click.option("--overwrite", is_flag=True, help="Overwrite the existing YML file.")
def sort_yaml(select, all_files, overwrite):
    sy = SortYAML()
    sy.main(select, all_files, overwrite)


@cdbt.command()
@click.pass_context
def pre_commit(ctx):
    """Run pre-commit hooks."""
    cdbt_class.pre_commit(ctx)
