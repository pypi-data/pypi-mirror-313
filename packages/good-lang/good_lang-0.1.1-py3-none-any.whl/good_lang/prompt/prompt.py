import asyncio
import collections
import contextlib
import contextvars
import functools
import inspect
import re
import typing
from abc import ABC, abstractmethod
from contextlib import AsyncExitStack, ExitStack
from dataclasses import dataclass, field
from typing import Any, Coroutine

from good_lang.providers.litellm import litellm
import nest_asyncio
from fast_depends import Depends, inject
from fast_depends.core import build_call_model
from good_common.utilities import yaml_dumps
from IPython import embed
from jinja2 import BaseLoader, Environment, StrictUndefined
from litellm import TextCompletionResponse
from litellm.types.utils import ModelResponse
from litellm.utils import CustomStreamWrapper
from loguru import logger
from pydantic import BaseModel

nest_asyncio.apply()


class AbstractRegistry(ABC):
    __registry__: typing.ClassVar[dict[str, typing.Self]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__registry__ = {}


def is_async_context():
    return asyncio.get_event_loop().is_running()


MessageRole = typing.Literal["system", "user", "assistant", "tool"]


T = typing.TypeVar("T", bound=BaseModel)


class Response(BaseModel, typing.Generic[T]):
    model_response: ModelResponse | TextCompletionResponse

    def choice(self, index: int = 0):
        return self.model_response.choices[index]

    @property
    def message(self):
        return self.choice(0).message.content

    structured_output: T | None = None

    @property
    def tool_calls(self):
        return self.choice(0).message.tool_calls


class Message(BaseModel):
    content: str
    role: MessageRole = "user"
    tool_calls: list[typing.Any] | None = None

    def get(self, key, default=None):
        # Custom .get() method to access attributes with a default value if the attribute doesn't exist
        return getattr(self, key, default)

    def __getitem__(self, key):
        # Allow dictionary-style access to attributes
        return getattr(self, key)

    def __setitem__(self, key, value):
        # Allow dictionary-style assignment of attributes
        setattr(self, key, value)

    def json(self, **kwargs):
        return self.model_dump(mode="json")  # noqa


class Tool(AbstractRegistry):
    name: str
    fn: typing.Callable
    tools: "ToolManager"

    def __init__(
        self,
        fn: typing.Callable,
        tools: "ToolManager",
        name: str | None = None,
    ):
        self.name = name or fn.__name__
        self.fn = inject(fn)
        self.tools = tools
        self.__registry__[fn.__name__] = self


@dataclass
class Profile:
    name: str
    model: str
    system_prompt: str | None = None

    timeout: float | int | None = None
    temperature: float | None = None
    top_p: float | None = None
    n: int | None = None
    stream: bool | None = None
    stream_options: dict | None = None
    stop: str | list[str] | None = None
    max_tokens: int | None = None
    presence_penalty: float | None = None
    frequency_penalty: float | None = None
    logit_bias: dict | None = None
    user: str | None = None
    # openai v1.0+ new params
    response_format: dict | None = None
    seed: int | None = None
    # tools: Optional[List] = None,
    tools: list[Tool] | None = None
    tool_choice: str | None = None
    parallel_tool_calls: bool | None = None
    logprobs: bool | None = None
    top_logprobs: int | None = None
    deployment_id: str | None = None
    # set api_base, api_version, api_key
    base_url: str | None = None
    api_version: str | None = None
    api_key: str | None = None
    model_list: list[str] | None = None  # pass in a list of api_base,keys, etc.
    extra_headers: dict | None = None

    on_response: list[typing.Callable] | None = None

    def merge_arguments(self, **kwargs):
        for arg in (
            "model",
            "timeout",
            "temperature",
            "top_p",
            "n",
            "stream",
            "stream_options",
            "stop",
            "max_tokens",
            "presence_penalty",
            "frequency_penalty",
            "logit_bias",
            "user",
            "response_format",
            "seed",
            "tools",
            "tool_choice",
            "parallel_tool_calls",
            "logprobs",
            "top_logprobs",
            "deployment_id",
            "base_url",
            "api_version",
            "api_key",
            "model_list",
            "extra_headers",
        ):
            kwargs[arg] = kwargs.get(arg, getattr(self, arg))

        if "messages" in kwargs:
            # resolve model objects
            kwargs["messages"] = [
                message.model_dump(mode="json") for message in kwargs["messages"]
            ]

        return kwargs

    async def call_async(
        self, on_response_callback: typing.Callable | None = None, **kwargs
    ) -> Response:
        logger.debug(self.merge_arguments(**kwargs))
        resp = await litellm.acompletion(**self.merge_arguments(**kwargs))
        if isinstance(resp, CustomStreamWrapper):
            chunks = []
            async for chunk in resp:
                chunks.append(chunk)
            resp = litellm.stream_chunk_builder(
                chunks,
                # messages=messages
            )

        if on_response_callback:
            on_response_callback(resp)
        return Response(model_response=resp)

    def call_sync(self, on_response_callback: typing.Callable | None = None, **kwargs):
        resp = litellm.completion(**self.merge_arguments(**kwargs))
        if isinstance(resp, CustomStreamWrapper):
            chunks = []
            for chunk in resp:
                chunks.append(chunk)
            resp = litellm.stream_chunk_builder(
                chunks,
                # messages=messages
            )
        if on_response_callback:
            on_response_callback(resp)
        return Response(model_response=resp)

    def send(self, message: str) -> Response:
        resp = self.call_sync(messages=[Message(content=message, role="user")])
        return resp.message

    async def asend(self, message: str) -> Response:
        resp = await self.call_async(messages=[Message(content=message, role="user")])
        return resp.message


class Context:
    manager: "PromptManager"

    messages: dict[str, list[Message]]

    prompts: dict[str, "Prompt"]

    tools: dict[str, Tool]

    def __init__(
        self,
        manager: "PromptManager",
        messages: dict[str, list[Message]] | None = None,
        prompts: dict[str, "Prompt"] | None = None,
        tools: dict[str, Tool] | None = None,
    ):
        self.manager = manager
        self.messages = collections.defaultdict(list)
        if messages:
            for _profile, _messages in messages.items():
                for msg in _messages:
                    self.messages[_profile].append(msg)
        self.prompts = prompts or {}
        self.tools = tools or {}

    def __enter__(self):
        self.manager.current_context = self
        return self

    def __exit__(self, *args):
        self.manager.reset_context()

    async def prompt(self, name: str, **kwargs):
        _prompt = self.prompts.get(name)
        if _prompt:
            resp = await _prompt.acall(**kwargs)
            return resp.message

    def copy(self, copy_tools: bool = False, copy_prompts: bool = False):
        return Context(
            manager=self.manager,
            messages=self.messages.copy() if self.messages else None,
            prompts=self.prompts.copy() if copy_prompts else None,
            tools=self.tools.copy() if copy_tools else None,
        )

    def completion(self, profile: str = "default", **kwargs):
        _profile = self.manager.profiles.get(profile)

        if not _profile:
            raise ValueError(f"Profile '{profile}' not found.")

        return _profile.call_sync(
            messages=self.messages,
            on_response_callback=functools.partial(self.on_response, profile=_profile),
            **kwargs,
        )

    async def acompletion(self, profile: str = "default", **kwargs):
        _profile = self.manager.profiles.get(profile)

        if not _profile:
            raise ValueError(f"Profile '{profile}' not found.")

        return await _profile.call_async(
            messages=self.messages,
            on_response_callback=functools.partial(self.on_response, profile=_profile),
            **kwargs,
        )

    def on_response(
        self, profile: Profile, messages: list[Message], response: Response
    ) -> None:
        for message in messages:
            self.messages[profile.name].append(message)

        self.messages[profile.name].append(
            Message(
                content=response.choice().message.content,
                role=response.choice().message.role,
            )
        )


T = typing.TypeVar("T", bound=BaseModel)


class Prompt(AbstractRegistry, typing.Generic[T]):
    role: MessageRole

    response_model: typing.Type[BaseModel] | None = None

    def __init__(
        self,
        fn: typing.Callable,
        manager: "PromptManager",
        role: MessageRole = "user",
        template: str | None = None,
    ):
        self.fn = fn
        self.role = role

        functools.update_wrapper(self, fn)

        self._manager = manager
        self._template = template or fn.__doc__
        self.overrides = {}

        if self.is_async():

            async def _return_args(*args, **kwargs):
                return args, kwargs

            signature = inspect.signature(fn)

            return_annotation = signature.return_annotation

            _return_args.__signature__ = signature.replace(
                return_annotation=inspect.Signature.empty
            )  # type: ignore

            self.call_model = build_call_model(_return_args)

            if issubclass(return_annotation, BaseModel):
                self.response_model = return_annotation
            # self.response_model = return_annotation
            self.call_model.response_model = None

        else:

            def _return_args(*args, **kwargs):
                return args, kwargs

            signature = inspect.signature(fn)

            return_annotation = signature.return_annotation

            _return_args.__signature__ = signature.replace(
                return_annotation=inspect.Signature.empty
            )

            self.call_model = build_call_model(_return_args)
            # self.response_model = self.call_model.response_model
            self.response_model = return_annotation
            self.call_model.response_model = None

        self.__registry__[fn.__name__] = self

    def is_async(self):
        return inspect.iscoroutinefunction(self.fn)

    @property
    def manager(self) -> "PromptManager":
        return self._manager

    @property
    def parameters(self):
        return list(self.signature.parameters.keys())

    @property
    def signature(self):
        return inspect.signature(self.fn)

    @property
    def name(self):
        return self.fn.__name__

    def render(self, *args, **kwargs):
        bound_arguments = self.signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        with ExitStack() as stack:
            resolved = self.call_model.solve(
                *args,
                stack=stack,
                dependency_overrides=self.overrides,
                cache_dependencies={},
                nested=False,
                **bound_arguments.arguments,
            )
            _, arguments = resolved

        return self.manager.render(
            template=self.template, template_context=self.template_context, **arguments
        )

    async def render_async(self, *args, **kwargs):
        bound_arguments = self.signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        async with AsyncExitStack() as stack:
            resolved = await self.call_model.asolve(
                *args,
                stack=stack,
                dependency_overrides=self.overrides,
                cache_dependencies={},
                nested=True,
                **bound_arguments.arguments,
            )
            _, arguments = resolved

        return self.manager.render(
            template=self.template, template_context=self.template_context, **arguments
        )

    @property
    def template_context(self):
        return {
            # 'prompts': self.manager.current_context.prompts,
        }

    @property
    def template(self):
        if not self._template:
            raise TypeError("Could not find a template in the function's docstring.")
        return self._template

    def __str__(self):
        return self._template

    def __call__(self, *args, **kwargs) -> Coroutine[Any, Any, str] | str:
        """Render and return the template.

        Returns
        -------
        The rendered template as a Python ``str``.

        """
        # print("call")
        if self.is_async() and is_async_context():
            return self.render_async(*args, **kwargs)
        else:
            return self.render(*args, **kwargs)

    def __await__(self):
        return self.render_async().__await__()

    def call(
        self,
        /,
        profile: str = "default",
        in_context: bool = True,
        model_kwargs: dict = {},
        **template_args,
    ) -> Response[T]:
        _profile = self.manager.profiles.get(profile)

        if not _profile:
            raise ValueError(f"Profile '{profile}' not found.")

        logger.debug(self.manager.current_context)

        messages = (
            self.manager.current_context.messages.get(profile, []) if in_context else []
        )

        messages.append(self.as_message(**template_args))

        if self.response_model:
            model_kwargs["response_format"] = self.response_model

        resp = _profile.call_sync(messages=messages, **model_kwargs)

        if self.response_model:
            resp.structured_output = self.response_model.model_validate_json(
                resp.message
            )

        return resp

    async def acall(
        self,
        /,
        profile: str = "default",
        in_context: bool = True,
        model_kwargs: dict = {},
        **template_args,
    ) -> Response[T]:
        _profile = self.manager.profiles.get(profile)

        if not _profile:
            raise ValueError(f"Profile '{profile}' not found.")

        messages = (
            self.manager.current_context.messages.get(profile, []) if in_context else []
        )

        messages.append(await self.async_as_message(**template_args))

        if self.response_model:
            model_kwargs["response_format"] = self.response_model

        resp = await _profile.call_async(messages=messages, **model_kwargs)

        if self.response_model:
            resp.structured_output = self.response_model.model_validate_json(
                resp.message
            )

        return resp

    def as_message(self, *args, **kwargs) -> Message:
        rendered = self(*args, **kwargs)
        # print(rendered)
        return Message(content=rendered, role=self.role)

    async def async_as_message(self, *args, **kwargs) -> Message:
        return Message(content=await self.render_async(*args, **kwargs), role=self.role)


class ToolManager:
    def __init__(self, manager: "PromptManager"):
        self._manager = manager

    def __call__(
        self, fn, name: str | None = None, **kwargs
    ) -> Tool | typing.Callable[..., Tool]:
        def wrapper(
            fn: typing.Callable,
        ) -> Tool:
            tool_name = name or fn.__name__
            return Tool(name=tool_name, fn=fn, tools=self)

        if fn:
            return wrapper(fn)
        else:
            return wrapper


T = typing.TypeVar("T")


class Renderer(typing.Generic[T]):
    # __registry__: typing.ClassVar[dict[str, typing.Self]] = {}
    def __init__(self, _type: typing.Type[T], fn: typing.Callable[[T], str]):
        self.type = _type
        self.fn = fn

    def __call__(self, obj: T, **kwargs) -> str:
        return self.fn(obj, **kwargs)


class PromptManager:
    profiles: dict[str, Profile] = {}

    def __init__(self):
        self.tools = ToolManager(manager=self)
        self.global_context = Context(manager=self)
        self._current_context = contextvars.ContextVar(
            "current_context", default=self.global_context
        )
        self._current_context_token = None

    def tool(
        self, fn, name: str | None = None, **kwargs
    ) -> Tool | typing.Callable[..., Tool]:
        return self.tools(fn, name=name, **kwargs)

    def __call__(
        self, fn, role: MessageRole = "user", **kwargs
    ) -> Prompt | typing.Callable[..., Prompt]:
        def wrapper(
            fn: typing.Callable,
        ) -> Prompt:
            _prompt = Prompt(fn, manager=self)
            self.current_context.prompts[_prompt.name] = _prompt
            return _prompt

        if fn:
            return wrapper(fn)
        else:
            return wrapper

    @property
    def context(self) -> Context:
        return self._current_context.get() or self.global_context

    @context.setter
    def current_context(self, value: Context):
        self._current_context_token = self._current_context.set(value)

    def reset_context(self):
        if self._current_context_token:
            self._current_context.reset(self._current_context_token)

    def new_context(
        self, *args, copy_tools: bool = False, copy_prompts: bool = False, **kwargs
    ) -> Context:
        ctx = self.current_context.copy(
            copy_tools=copy_tools,
            copy_prompts=copy_prompts,
        )

        return ctx

    def process_template_values(self, **values: typing.Any) -> dict[str, typing.Any]:
        # TO DO - custom renderers

        def render_pydantic(model: BaseModel):
            return yaml_dumps(model.model_dump(mode="json"))

        return {
            k: render_pydantic(value) if isinstance(value, BaseModel) else value
            for k, value in values.items()
        }

    def render(
        self,
        template: str,
        template_context: dict[str, typing.Any] = {},
        **values: typing.Optional[typing.Any],
    ):
        cleaned_template = inspect.cleandoc(template)

        # Add linebreak if there were any extra linebreaks that
        # `cleandoc` would have removed
        ends_with_linebreak = template.replace(" ", "").endswith("\n\n")
        if ends_with_linebreak:
            cleaned_template += "\n"

        # Remove extra whitespaces, except those that immediately follow a newline symbol.
        # This is necessary to avoid introducing whitespaces after backslash `\` characters
        # used to continue to the next line without linebreak.
        cleaned_template = re.sub(r"(?![\r\n])(\b\s+)", " ", cleaned_template)

        env = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            undefined=StrictUndefined,
            loader=BaseLoader(),
            enable_async=True,
        )

        env.globals["context"] = self.current_context

        embedded_profile = self.profiles.get("embedded")

        if embedded_profile:
            if is_async_context():
                env.globals["send"] = embedded_profile.asend
            else:
                env.globals["send"] = embedded_profile.send

        # def direct_prompt(name: str, *args, **kwargs):
        #     return self.current_context.prompts[name](*args, **kwargs)

        if template_context:
            env.globals.update(template_context)

        jinja_template = env.from_string(cleaned_template)

        return jinja_template.render(**values)


prompt = PromptManager()

prompt.profiles["default"] = Profile(name="default", model="gpt-4o-mini")

prompt.profiles["embedded"] = Profile(
    name="embedded",
    model="gpt-4o-mini",
    system_prompt=(
        "You are an embedded prompt generating function "
        "that is called within the template of another prompt. "
        "You will only respond to what is asked. Do not give any preamble, "
        "introduction or additional explanation. Do not make any mention of the fact "
        "that the response is for a prompt. The response must be able to be "
        "directly inserted into the parent prompt."
    ),
    temperature=0.2,
)
