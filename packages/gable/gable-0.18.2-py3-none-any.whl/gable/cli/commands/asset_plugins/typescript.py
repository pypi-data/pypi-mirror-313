import functools
from typing import Callable, List, Mapping, TypedDict, Union

import click
from gable.api.client import GableAPIClient
from gable.cli.commands.asset_plugins.baseclass import (
    AssetPluginAbstract,
    ExtractedAsset,
)
from gable.cli.helpers.data_asset import (
    get_event_schemas_from_sca_results,
    get_git_repo,
    get_relative_project_path,
)
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.npm import (
    prepare_npm_environment,
    run_sca_prime_shadow,
    run_sca_typescript,
)
from gable.openapi import Library as TypeScriptLibrary
from gable.openapi import SourceType, StructuredDataAssetResourceName

ALL_TYPESCRIPT_LIBRARY_VALUES = [library.value for library in TypeScriptLibrary]

TypeScriptConfig = TypedDict(
    "TypeScriptConfig",
    {
        "project_root": click.Path,
        "library": TypeScriptLibrary,
        "emitter_file_path": Union[str, None],
        "emitter_function": Union[str, None],
        "emitter_payload_parameter": Union[str, None],
        "emitter_name_parameter": Union[str, None],
        "event_name_key": Union[str, None],
    },
)


class TypescriptAssetPlugin(AssetPluginAbstract):
    def source_type(self) -> SourceType:
        return SourceType.typescript

    def click_options_decorator(self) -> Callable:
        def decorator(func):
            @click.option(
                "--project-root",
                help="The directory location of the Typescript project that will be analyzed.",
                type=click.Path(exists=True),
                required=True,
            )
            @click.option(
                "--library",
                help="This should indicate the library emitting the events you want detected as data assets.",
                type=click.Choice(ALL_TYPESCRIPT_LIBRARY_VALUES),
                default=TypeScriptLibrary.udf.value,
            )
            @click.option(
                "--emitter-file-path",
                help="Relative path from the root of the project to the file that contains the emitter function",
                type=str,
            )
            @click.option(
                "--emitter-function",
                help="Name of the emitter function",
                type=str,
            )
            @click.option(
                "--emitter-payload-parameter",
                help="Name of the parameter representing the event payload",
                type=str,
            )
            @click.option(
                "--emitter-name-parameter",
                help="Name of the emitter function parameter that contains the event name. Either this option, or the --event-name-key option must be provided when using --emitter-function.",
                type=str,
            )
            @click.option(
                "--event-name-key",
                help="Name of the event property that contains the event name. Either this option, or the --emitter-name-parameter option must be provided when using --emitter-function.",
                type=str,
            )
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def click_options_keys(self) -> set[str]:
        return set(TypeScriptConfig.__annotations__.keys())

    def pre_validation(self, config: Mapping) -> None:

        typed_config = TypeScriptConfig(**config)
        if (
            typed_config["library"] == TypeScriptLibrary.udf.value
            and not typed_config["emitter_function"]
        ):
            raise click.MissingParameter(
                f"{EMOJI.RED_X.value} Missing required options for Typescript project registration. Either --library or --emitter-function must be specified. You can use the --help option for more details.",
                param_type="option",
            )
        if (
            typed_config["library"] != TypeScriptLibrary.udf.value
            and typed_config["emitter_function"]
        ):
            raise click.UsageError(
                f"{EMOJI.RED_X.value} If --library is not udf then --emitter-function cannot be specified."
            )
        if typed_config["emitter_function"] and (
            not typed_config["emitter_payload_parameter"]
            or not typed_config["emitter_file_path"]
            or (
                not typed_config["event_name_key"]
                and not typed_config["emitter_name_parameter"]
            )
        ):
            raise click.MissingParameter(
                f"{EMOJI.RED_X.value} Missing required options for Typescript project registration when using --emitter-function. Options --emitter-payload-parameter, --emitter-file-path, and either --event-name-key or --event-name-parameter are required. You can use the --help option for more details.",
                param_type="option",
            )

    def extract_assets(
        self, client: GableAPIClient, config: Mapping
    ) -> List[ExtractedAsset]:
        """Extract assets from the source."""
        typed_config = TypeScriptConfig(**config)

        prepare_npm_environment(client)
        (sca_results, shadow_results) = run_sca_typescript(
            typed_config["library"],
            str(typed_config["project_root"]),
            typed_config["emitter_file_path"],
            typed_config["emitter_function"],
            typed_config["emitter_payload_parameter"],
            typed_config["event_name_key"],
            typed_config["emitter_name_parameter"],
            client.endpoint,
        )
        sca_results_dict = get_event_schemas_from_sca_results(sca_results)
        if sca_results_dict is {}:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} No data assets found to register! You can use the --debug or --trace flags for more details.",
            )

        git_ssh_repo = get_git_repo(str(typed_config["project_root"]))
        _, relative_typescript_project_root = get_relative_project_path(
            str(typed_config["project_root"])
        )
        data_source = f"git@{git_ssh_repo}:{relative_typescript_project_root}:{typed_config['library']}"
        assets = [
            ExtractedAsset(
                darn=StructuredDataAssetResourceName(
                    source_type=SourceType.typescript,
                    data_source=data_source,
                    path=event_name,
                ),
                fields=[
                    field
                    for field in map(
                        ExtractedAsset.safe_parse_field, event_schema["fields"]
                    )
                    if field is not None
                ],
                dataProfileMapping=None,
            )
            for event_name, event_schema in {
                **sca_results_dict,
                **shadow_results,
            }.items()
        ]
        return assets

    def checked_when_registered(self) -> bool:
        return False
