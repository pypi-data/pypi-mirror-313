from typing import Awaitable, List, Optional

from ambient_backend_api_client import Configuration
from pydantic import BaseModel, field_serializer, field_validator

from ambient_client_common.repositories import docker_repo as docker_repo_
from ambient_client_common.repositories import node_repo as node_repo_


class RetryPolicy(BaseModel):
    max_retries: int = 0
    retry_interval: int = 1  # Time interval between retries in seconds
    backoff_factor: int = 2  # Exponential backoff factor (1, 2, 4, 8)


class PluginDefinition(BaseModel):
    name: str
    topics: List[str]
    module: str
    class_name: str
    extra_data: Optional[dict] = None
    retry_policy: Optional[RetryPolicy] = None

    # request extra data from the core
    request_api_config: bool = False
    request_platform: bool = False
    request_node_repo: bool = False
    request_docker_repo: bool = False

    # ensure topics start with / or * and ends without /
    @field_validator("topics")
    def validate_topics(cls, values: List[str]):
        for value in values:
            if not value.startswith("/") and not value.startswith("*"):
                raise ValueError(f"Topic must start with / or *. Topoc: {value}")
            if value.endswith("/"):
                raise ValueError(f"Topic must not end with /. Topoc: {value}")
        return values


class ConfigPayload(BaseModel):
    class Config:
        arbitrary_types_allowed = True  # needed for logger

    node_id: int
    plugin_config: PluginDefinition
    extra_data: Optional[dict] = None

    # data available on request
    api_config: Optional[Configuration] = None
    platform: Optional[str] = None
    node_repo: Optional[node_repo_.NodeRepo] = None
    docker_repo: Optional[docker_repo_.DockerRepo] = None
    get_token: Optional[Awaitable[str]] = None

    @field_serializer("api_config")
    def serialize_api_config(cls, value: Configuration) -> dict:
        return {"name": "Ambient API Configuration"}

    @field_serializer("node_repo")
    def serialize_node_repo(cls, value: node_repo_.NodeRepo) -> dict:
        return {"name": "Node Repository"}

    @field_serializer("docker_repo")
    def serialize_docker_repo(cls, value: docker_repo_.DockerRepo) -> dict:
        return {"name": "Docker Repository"}

    @field_serializer("get_token")
    def serialize_get_token(cls, value: Awaitable[str]) -> dict:
        return {"name": "Get Token Function"}
