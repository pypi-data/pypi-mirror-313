"""The main command line interface."""

import contextlib
import os
import sys
import traceback
from importlib.resources import open_text
from subprocess import CalledProcessError  # nosec

import click
import requests.exceptions

from cmem_cmemc import completion
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.commands import (
    admin,
    config,
    dataset,
    graph,
    project,
    query,
    vocabulary,
    workflow,
)
from cmem_cmemc.context import CONTEXT
from cmem_cmemc.exceptions import InvalidConfigurationError
from cmem_cmemc.manual_helper.graph import print_manual_graph
from cmem_cmemc.manual_helper.multi_page import create_multi_page_documentation
from cmem_cmemc.manual_helper.single_page import print_manual
from cmem_cmemc.utils import check_python_version, extract_error_message, get_version

CMEMC_VERSION = get_version()

# this will output a custom zsh completion function
if os.environ.get("_CMEMC_COMPLETE", "") == "zsh_source":
    with open_text("cmem_cmemc", "_cmemc.zsh") as zsh_output:
        CONTEXT.echo_info(zsh_output.read())
    sys.exit(0)

version = sys.version_info
PYTHON_VERSION = f"{version.major}.{version.minor}.{version.micro}"
check_python_version(ctx=CONTEXT)

# set the user-agent environment for the http request headers
os.environ["CMEM_USER_AGENT"] = f"cmemc/{CMEMC_VERSION} (Python {PYTHON_VERSION})"

# https://github.com/pallets/click/blob/master/examples/complex/complex/cli.py
CONTEXT_SETTINGS = {"auto_envvar_prefix": "CMEMC", "help_option_names": ["-h", "--help"]}


@click.group(name="cmemc", cls=CmemcGroup, context_settings=CONTEXT_SETTINGS)
@click.option(
    "-c",
    "--connection",
    type=click.STRING,
    shell_complete=completion.connections,
    help="Use a specific connection from the config file.",
)
@click.option(
    "--config-file",
    shell_complete=completion.ini_files,
    type=click.Path(readable=True, allow_dash=False, dir_okay=False),
    default=CONTEXT.config_file_default,
    show_default=True,
    help="Use this config file instead of the default one.",
)
@click.option("-q", "--quiet", is_flag=True, help="Suppress any non-error info messages.")
@click.option(
    "-d", "--debug", is_flag=True, help="Output debug messages and stack traces after errors."
)
@click.version_option(
    version=CMEMC_VERSION,
    message="%(prog)s, version %(version)s, " f"running under python {PYTHON_VERSION}",
)
@click.pass_context
def cli(
    ctx: click.core.Context, debug: bool, quiet: bool, config_file: str, connection: str
) -> None:
    """Eccenca Corporate Memory Control (cmemc).

    cmemc is the eccenca Corporate Memory Command Line Interface (CLI).

    Available commands are grouped by affecting resource type (such as graph,
    project and query).
    Each command and group has a separate --help screen for detailed
    documentation.
    In order to see possible commands in a group, simply
    execute the group command without further parameter (e.g. cmemc project).

    If your terminal supports colors, these coloring rules are applied:
    Groups are colored in white; Commands which change data are colored in
    red; all other commands as well as options are colored in green.

    Please also have a look at the cmemc online documentation:

                        https://eccenca.com/go/cmemc

    cmemc is © 2024 eccenca GmbH, licensed under the Apache License 2.0.
    """
    ctx.obj = CONTEXT
    # hidden feature: 'CMEMC_MANUAL=true cmemc -q config list' will output
    #     the whole markdown manual
    if os.getenv("CMEMC_MANUAL_DIR"):
        create_multi_page_documentation(ctx, str(os.getenv("CMEMC_MANUAL_DIR")))
        ctx.exit()
    # hidden feature: 'CMEMC_MANUAL=true cmemc -q config list' will output
    #     the whole markdown manual
    if os.getenv("CMEMC_MANUAL"):
        print_manual(ctx)
        ctx.exit()
    # hidden feature: 'CMEMC_MANUAL_GRAPH=true cmemc -q config list' will
    # output the documentation graph
    if os.getenv("CMEMC_MANUAL_GRAPH"):
        print_manual_graph(ctx, get_version())
        ctx.exit()
    ctx.obj.set_quiet(quiet)
    ctx.obj.set_debug(debug)
    ctx.obj.set_config_file(config_file)
    try:
        ctx.obj.set_connection(connection)
    except InvalidConfigurationError:
        # if config is broken still allow for "config edit"
        # means: do not forward this exception if "config edit"
        if " ".join(sys.argv).find("config edit") == -1:
            raise


cli.add_command(admin.admin)
cli.add_command(config.config)
cli.add_command(dataset.dataset)
cli.add_command(graph.graph)
cli.add_command(project.project)
cli.add_command(query.query)
cli.add_command(vocabulary.vocabulary)
cli.add_command(workflow.workflow)


def main() -> None:
    """Start the command line interface."""
    try:
        cli()  # pylint: disable=no-value-for-parameter
    except (
        OSError,
        CalledProcessError,
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        ValueError,
        NotImplementedError,
        KeyError,
    ) as error:
        if CONTEXT.is_completing():
            # if currently autocompleting -> silently die with exit 1
            sys.exit(1)
        CONTEXT.echo_debug(traceback.format_exc())
        CONTEXT.echo_error(extract_error_message(error))
        with contextlib.suppress(
            requests.exceptions.ConnectionError, requests.exceptions.HTTPError
        ):
            CONTEXT.check_versions()
        sys.exit(1)
