import os

import click
from gable.openapi import GetNpmCredentialsResponse
from loguru import logger

AUTH_BLOCK_START = "### Gable Auth Block Start ###"
AUTH_BLOCK_END = "### Gable Auth Block End ###"


def format_npmrc_credentials(npm_credentials: GetNpmCredentialsResponse) -> str:
    """
    Format the NPM credentials as a string for writing to the .npmrc file
    """

    registry_endpoint_http_trimmed = npm_credentials.repositoryEndpoint[
        npm_credentials.repositoryEndpoint.find("//") :
    ]
    return f"""
@gable-eng:registry={npm_credentials.repositoryEndpoint}
{registry_endpoint_http_trimmed}:_authToken={npm_credentials.authToken}
{registry_endpoint_http_trimmed}:always-auth=true
    """.strip()


def set_npm_config_credentials(npm_credentials: GetNpmCredentialsResponse):
    """
    Set the NPM_CONFIG environment variables for the credentials
    """

    registry_endpoint_http_trimmed = npm_credentials.repositoryEndpoint[
        npm_credentials.repositoryEndpoint.find("//") :
    ]
    os.environ["NPM_CONFIG_@gable-eng:REGISTRY"] = npm_credentials.repositoryEndpoint
    os.environ[f"NPM_CONFIG_{registry_endpoint_http_trimmed}:_authToken"] = (
        npm_credentials.authToken
    )


def write_npm_credentials(
    creds: GetNpmCredentialsResponse, npmrcPath: str = "~/.npmrc"
):
    """
    Write or update the Gable NPM credentials to the user's .npmrc file
    """
    # Check if the file exists
    if not os.path.exists(npmrcPath):
        raise click.ClickException(
            f"Error writing NPM credentials: {npmrcPath} does not exist"
        )
    # Read the file contents
    with open(npmrcPath, "r") as f:
        text = f.read()
        if AUTH_BLOCK_START in text and AUTH_BLOCK_END in text:
            # Replace the existing block
            start = text.find(AUTH_BLOCK_START) + len(AUTH_BLOCK_START)
            end = text.find(AUTH_BLOCK_END)
            text = (
                text[:start]
                + "\n"
                + format_npmrc_credentials(creds)
                + "\n"
                + text[end:]
            )
        else:
            # Add a new block
            text += (
                "\n\n"
                + AUTH_BLOCK_START
                + "\n"
                + format_npmrc_credentials(creds)
                + "\n"
                + AUTH_BLOCK_END
                + "\n"
            )
    # Write the file contents
    with open(npmrcPath, "w") as f:
        f.write(text)
