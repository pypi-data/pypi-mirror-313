import datetime

from gable.openapi import ContractInput

from .models import ExternalContractInput

DUMMY_GIT_HASH = "1234567890abcdefghijklmnopqrstuvwxyzABCD"
DUMMY_GIT_REPO = "https://placeholder.com"
DUMMY_FILE_PATH = "placeholder"


def external_to_internal_contract_input(
    input: ExternalContractInput,
) -> ContractInput:
    return ContractInput(
        id=input.contractSpec.id,
        gitHash=(input.gitMetadata.gitHash if input.gitMetadata else DUMMY_GIT_HASH),
        gitRepo=(
            input.gitMetadata.gitRepo
            if input.gitMetadata
            else DUMMY_GIT_REPO  # type: ignore
        ),
        gitUser=input.gitMetadata.gitUser if input.gitMetadata else "",
        mergedAt=(
            input.gitMetadata.mergedAt
            if input.gitMetadata
            else datetime.datetime.now(datetime.timezone.utc)
        ),
        filePath=(input.gitMetadata.filePath if input.gitMetadata else DUMMY_FILE_PATH),
        version=input.version or "",
        status=input.status,
        enforcementLevel=input.enforcementLevel,
        contractSpec=input.contractSpec,
    )
