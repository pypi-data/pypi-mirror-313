import subprocess

import click
from click.core import Context as ClickContext
from gable.api.client import GableAPIClient
from gable.cli.helpers.npm import get_sca_cmd, prepare_npm_environment
from gable.cli.options import global_options
from loguru import logger


@click.group(hidden=True)
def demo():
    """Demo commands"""


@demo.command(
    # Disable help, we re-add it in global_options()
    add_help_option=False,
)
@global_options(add_endpoint_options=False)
@click.option(
    "--project-root",
    help="The directory of the Java project that will be analyzed.",
    type=click.Path(exists=True),
    required=True,
)
@click.option(
    "--build-command",
    help="The build command used to build the java project (e.g. mvn clean install).",
    type=str,
    required=True,
)
@click.option(
    "--java-version",
    help="The version of Java used to build the project.",
    type=str,
    default="17",
)
@click.pass_context
def java_dataflow(
    ctx: ClickContext, project_root: str, build_command: str, java_version: str
):
    """Prints connections between sources and sinks in Java code"""
    client: GableAPIClient = ctx.obj.client
    prepare_npm_environment(client)
    args = [
        "java-dataflow",
        project_root,
        "--build-command",
        build_command,
        "--java-version",
        java_version,
    ]
    cmd = get_sca_cmd(None, args)

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        logger.debug(result.stderr)
        raise click.ClickException(f"Error running Gable SCA: {result.stderr}")
    logger.trace(result.stderr)
    print(result.stdout)
