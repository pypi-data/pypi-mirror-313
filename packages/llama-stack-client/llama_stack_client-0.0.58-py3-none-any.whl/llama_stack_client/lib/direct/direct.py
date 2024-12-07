import inspect
from pathlib import Path
from typing import Any, cast, get_args, get_origin, Optional, Type

import yaml
from llama_stack.distribution.build import print_pip_install_help
from llama_stack.distribution.configure import parse_and_maybe_upgrade_config
from llama_stack.distribution.datatypes import StackRunConfig
from llama_stack.distribution.resolver import ProviderRegistry
from llama_stack.distribution.server.endpoints import get_all_api_endpoints
from llama_stack.distribution.server.server import is_streaming_request
from llama_stack.distribution.stack import (
    construct_stack,
    get_stack_run_config_from_template,
    replace_env_vars,
)
from pydantic import BaseModel, parse_obj_as
from rich.console import Console

from termcolor import cprint

from ..._base_client import ResponseT
from ..._client import LlamaStackClient
from ..._streaming import Stream
from ..._types import Body, NOT_GIVEN, RequestFiles, RequestOptions


class LlamaStackDirectClient(LlamaStackClient):
    def __init__(self, config: Any, **kwargs):
        raise TypeError(
            "Use from_config() or from_template() instead of direct initialization"
        )

    @classmethod
    async def from_config(
        cls,
        config_path: str,
        custom_provider_registry: Optional[ProviderRegistry] = None,
        **kwargs,
    ):
        instance = object.__new__(cls)
        config_path = Path(config_path)
        if not config_path.exists():
            raise ValueError(f"Config file {config_path} does not exist")

        config_dict = replace_env_vars(yaml.safe_load(config_path.read_text()))
        config = parse_and_maybe_upgrade_config(config_dict)
        await instance._initialize(config, custom_provider_registry, **kwargs)
        return instance

    @classmethod
    async def from_template(
        cls,
        template_name: str,
        custom_provider_registry: Optional[ProviderRegistry] = None,
        **kwargs,
    ):
        config = get_stack_run_config_from_template(template_name)
        console = Console()
        console.print(
            f"[green]Using template[/green] [blue]{template_name}[/blue] with config:"
        )
        console.print(
            yaml.dump(config.model_dump(), indent=2, default_flow_style=False)
        )
        instance = object.__new__(cls)
        await instance._initialize(config, custom_provider_registry, **kwargs)
        return instance

    async def _initialize(
        self,
        config: StackRunConfig,
        custom_provider_registry: Optional[ProviderRegistry] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.endpoints = get_all_api_endpoints()
        self.config = config
        self.impls = None
        self.custom_provider_registry = custom_provider_registry
        await self.initialize()

    async def initialize(self) -> None:
        try:
            self.impls = await construct_stack(
                self.config, self.custom_provider_registry
            )
        except ModuleNotFoundError as e:
            print_pip_install_help(self.config.providers)
            raise e

    def _convert_param(self, annotation: Any, value: Any) -> Any:
        if annotation in (str, int, float, bool):
            return value

        origin = get_origin(annotation)
        if origin == list:
            item_type = get_args(annotation)[0]
            try:
                return [self._convert_param(item_type, item) for item in value]
            except Exception:
                return value

        elif origin == dict:
            key_type, val_type = get_args(annotation)
            try:
                return {k: self._convert_param(val_type, v) for k, v in value.items()}
            except Exception:
                return value

        try:
            # Handle Pydantic models and discriminated unions
            return parse_obj_as(annotation, value)
        except Exception as e:
            cprint(
                f"Warning: direct client failed to convert parameter {value} into {annotation}: {e}",
                "yellow",
            )
            return value

    async def _call_endpoint(self, path: str, method: str, body: dict = None) -> Any:
        for api, endpoints in self.endpoints.items():
            for endpoint in endpoints:
                if endpoint.route == path:
                    impl = self.impls[api]
                    func = getattr(impl, endpoint.name)
                    sig = inspect.signature(func)  #

                    if body:
                        # Strip NOT_GIVENs to use the defaults in signature
                        body = {k: v for k, v in body.items() if v is not NOT_GIVEN}

                        # Convert parameters to Pydantic models where needed
                        converted_body = {}
                        for param_name, param in sig.parameters.items():
                            if param_name in body:
                                value = body.get(param_name)
                                converted_body[param_name] = self._convert_param(
                                    param.annotation, value
                                )
                        body = converted_body

                    if is_streaming_request(endpoint.name, body):
                        async for chunk in func(**(body or {})):
                            yield chunk
                    else:
                        yield await func(**(body or {}))

        raise ValueError(f"No endpoint found for {path}")

    async def get(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        options: RequestOptions = None,
        stream: bool = False,
        stream_cls: type[Stream[Any]] | None = None,
    ) -> ResponseT:
        options = options or {}
        async for response in self._call_endpoint(path, "GET"):
            return cast(ResponseT, response)

    async def post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        options: RequestOptions = None,
        files: RequestFiles | None = None,
        stream: bool = False,
        stream_cls: type[Stream[Any]] | None = None,
    ) -> ResponseT:
        options = options or {}
        async for response in self._call_endpoint(path, "POST", body):
            return cast(ResponseT, response)
