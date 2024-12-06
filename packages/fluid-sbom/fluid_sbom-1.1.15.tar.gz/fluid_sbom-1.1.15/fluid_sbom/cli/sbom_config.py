import logging
import os
from typing import (
    TypedDict,
    Unpack,
)

import confuse

from fluid_sbom.config.config import (
    SbomConfig,
    SbomOutputFormat,
    SourceType,
)
from fluid_sbom.utils.exceptions import (
    InvalidConfigFileError,
)

LOGGER = logging.getLogger(__name__)


class ScanArgs(TypedDict):
    o_from: str
    output_format: str
    output: str
    docker_user: str | None
    docker_password: str | None
    config: bool


def _build_config(config_path: str) -> confuse.Configuration:
    template = confuse.Configuration("sbom", read=False)
    template.set_file(config_path)
    template.read(user=False, defaults=False)
    return template.get(
        confuse.Template(
            {
                "source": confuse.String(),
                "source_type": confuse.String(),
                "execution_id": confuse.String(),
                "exclude": confuse.Sequence(confuse.String()),
                "docker_credentials": confuse.Optional(
                    confuse.Template(
                        {
                            "username": confuse.Optional(confuse.String()),
                            "password": confuse.Optional(confuse.String()),
                        },
                    ),
                ),
                "output": confuse.Template(
                    {
                        "name": confuse.String(),
                        "format": confuse.OneOf([_format.value for _format in SbomOutputFormat]),
                    },
                ),
            },
        ),
    )


def load(config_path: str) -> SbomConfig:
    config = _build_config(config_path)
    config_docker = config.pop("docker_credentials", {})

    try:
        output = config.pop("output", None)

        sbom_config = SbomConfig(
            source=config.pop("source", None),
            source_type=config.pop("source_type", "dir"),
            output_format=output["format"],
            output=output["name"],
            resolver=None,
            exclude=config.pop("exclude", None) or (),
            docker_user=config_docker.pop("username", None),
            docker_password=config_docker.pop("password", None),
            execution_id=config.pop("execution_id", None),
        )

        if config:
            unrecognized_keys = ", ".join(config)
            msg = (
                f"Some keys were not recognized: {unrecognized_keys}."
                " The analysis will be performed only using the supported keys"
                " and defaults."
            )
            LOGGER.warning(msg)
    except KeyError as exc:
        raise confuse.ConfigError(f"Key: {exc.args[0]} is required")

    return sbom_config


def build_sbom_config(arg: str, **kwargs: Unpack[ScanArgs]) -> SbomConfig:
    if kwargs["config"]:
        if os.path.isfile(arg):
            if not arg.endswith((".yaml", ".yml")):
                raise InvalidConfigFileError("The configuration file must be a YAML format")
            return load(arg)
        raise InvalidConfigFileError(f"The configuration file is not a valid file: {arg}")

    return SbomConfig(
        source=arg,
        source_type=SourceType.from_string(kwargs["o_from"]),
        execution_id=None,
        output_format=kwargs["output_format"],
        output=kwargs["output"],
        resolver=None,
        exclude=(),
        docker_user=kwargs["docker_user"],
        docker_password=kwargs["docker_password"],
    )
