from typing import Any, List, Tuple, Union

from gable.api.client import GableAPIClient
from gable.openapi import GableSchemaContractField, PostContractRequest
from gable.sdk.converters.trino import (
    convert_trino_timestamp_to_spark_timestamp,
    trino_to_gable_type,
)

from .helpers import external_to_internal_contract_input
from .models import ContractPublishResponse, ExternalContractInput, TrinoDataType


class GableContract:
    def __init__(self, api_endpoint, api_key) -> None:
        self.api_client = GableAPIClient(api_endpoint, api_key)

    def publish(
        self,
        contracts: list[ExternalContractInput],
    ) -> ContractPublishResponse:
        api_response, success, _status_code = self.api_client.post_contract(
            PostContractRequest(
                __root__=[
                    external_to_internal_contract_input(contract)
                    for contract in contracts
                ],
            )
        )

        # Currently, the behavior is either all contracts are published or none are (if there is one invalid contract)
        # Ideally, we can refactor this code and the API to allow for partial success in the future

        if not success or not isinstance(api_response, dict):
            failure_message = (
                api_response["message"]
                if isinstance(api_response, dict)
                else "Unknown error"
            )
            return ContractPublishResponse(
                success=False, updatedContractIds=[], message=failure_message
            )
        else:
            updated_contract_ids = api_response["contractIds"]
            return ContractPublishResponse(
                success=True,
                updatedContractIds=updated_contract_ids,
                message=api_response["message"],
            )

    def trino_to_gable_schema(
        self,
        dict_schema: dict[
            str, Union[str, Union[TrinoDataType, Tuple[TrinoDataType, Tuple[Any, ...]]]]
        ],
        convert_to_spark_types: bool = False,
    ) -> List[GableSchemaContractField]:
        results = [
            trino_to_gable_type(key, value) for key, value in dict_schema.items()
        ]
        if convert_to_spark_types:
            results = [
                convert_trino_timestamp_to_spark_timestamp(result) for result in results
            ]
        return results
