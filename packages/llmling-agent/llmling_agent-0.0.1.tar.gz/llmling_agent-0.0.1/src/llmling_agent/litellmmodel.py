"""LiteLLM model implementation for pydantic_ai."""

from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
import json
from typing import TYPE_CHECKING, Any, Literal

import litellm
from litellm import ModelResponse
from pydantic import BaseModel, ConfigDict
from pydantic_ai import messages, models
from pydantic_ai.exceptions import UnexpectedModelBehavior
from pydantic_ai.messages import (
    ModelAnyResponse,
    ModelStructuredResponse,
    ModelTextResponse,
)
from pydantic_ai.result import Cost


if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Mapping, Sequence


class ToolDefinition(BaseModel):
    """Pydantic model implementing AbstractToolDefinition protocol."""

    name: str
    description: str
    json_schema: dict[str, Any]
    outer_typed_dict_key: str | None = None

    model_config = ConfigDict(frozen=True)


@dataclass
class LiteLLMModel(models.Model):
    """LiteLLM-based model implementation supporting multiple providers."""

    model_name: str
    api_key: str | None = None
    model_settings: dict[str, Any] = field(default_factory=dict)

    async def agent_model(
        self,
        function_tools: Mapping[str, dict[str, Any]],
        allow_text_result: bool,
        result_tools: Sequence[dict[str, Any]] | None = None,
    ) -> models.AgentModel:
        """Create an agent model configured for the specific use case."""
        models.check_allow_model_requests()

        # Convert dicts to ToolDefinition instances
        tools = [
            self._create_tool_schema(ToolDefinition.model_validate(tool))
            for tool in function_tools.values()
        ]
        if result_tools:
            tools.extend(
                self._create_tool_schema(ToolDefinition.model_validate(tool))
                for tool in result_tools
            )

        return LiteLLMAgentModel(
            model=self.model_name,  # Fixed: use model_name instead of model
            api_key=self.api_key,
            allow_text_result=allow_text_result,
            tools=tools,
            **self.model_settings,
        )

    def name(self) -> str:
        return f"litellm:{self.model_name}"

    def _create_tool_schema(
        self,
        tool: ToolDefinition,
    ) -> dict[str, Any]:
        """Convert tool definition to LiteLLM format."""
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.json_schema,
            },
        }


@dataclass
class LiteLLMAgentModel(models.AgentModel):
    """LiteLLM implementation of AgentModel."""

    model: str
    api_key: str | None
    allow_text_result: bool
    tools: list[dict[str, Any]]
    tool_choice: Literal["none", "auto", "required"] = field(init=False)

    def __post_init__(self) -> None:
        """Configure tool choice based on settings."""
        if not self.tools:
            self.tool_choice = "none"
        elif not self.allow_text_result:
            self.tool_choice = "required"
        else:
            self.tool_choice = "auto"

    async def request(
        self, messages: list[messages.Message]
    ) -> tuple[ModelAnyResponse, Cost]:
        """Make a non-streaming request to the model."""
        litellm_messages = [self._convert_message(msg) for msg in messages]

        response = await litellm.acompletion(
            model=self.model,
            messages=litellm_messages,
            tools=self.tools or None,
            tool_choice=self.tool_choice if self.tools else None,
            api_key=self.api_key,
        )
        print("\nDebug - LiteLLM Response:")
        print(f"Response type: {type(response)}")
        print(f"Response dir: {dir(response)}")
        print(f"Response raw: {response}")
        return self._process_response(response), self._calculate_cost(response)

    @asynccontextmanager
    async def request_stream(
        self, messages: list[messages.Message]
    ) -> AsyncIterator[models.EitherStreamedResponse]:
        """Make a streaming request to the model."""
        litellm_messages = [self._convert_message(msg) for msg in messages]

        response = await litellm.acompletion(
            model=self.model,
            messages=litellm_messages,
            tools=self.tools or None,
            tool_choice="auto",  # Let's be explicit about allowing both text and tools
            api_key=self.api_key,
            stream=True,
        )

        # Create a fresh iterator
        response_iter = aiter(response)

        try:
            # Skip any empty chunks
            first_chunk = None
            while not first_chunk or not (
                getattr(first_chunk.choices[0].delta, "content", None)
                or getattr(first_chunk.choices[0].delta, "tool_calls", None)
            ):
                first_chunk = await anext(response_iter)
        except StopAsyncIteration as e:
            msg = "Stream ended without content"
            raise UnexpectedModelBehavior(msg) from e

        delta = first_chunk.choices[0].delta
        timestamp = datetime.fromtimestamp(first_chunk.created)
        start_cost = self._calculate_cost(first_chunk)

        # Check for tool calls in first delta
        if getattr(delta, "tool_calls", None):
            yield LiteLLMStreamStructuredResponse(
                response=response_iter,
                tool_calls={},
                _created_at=timestamp,
                start_cost=start_cost,
            )
        else:
            # Must be content
            yield LiteLLMStreamTextResponse(
                first_content=delta.content,
                response=response_iter,
                _created_at=timestamp,
                start_cost=start_cost,
            )

    def _convert_message(self, message: messages.Message) -> dict[str, Any]:  # noqa: PLR0911
        """Convert a pydantic_ai message to litellm format."""
        match message:
            case messages.SystemPrompt():
                return {"role": "system", "content": message.content}

            case messages.UserPrompt():
                return {"role": "user", "content": message.content}

            case messages.ToolReturn():
                return {
                    "role": "tool",
                    "tool_call_id": message.tool_id,
                    "content": message.model_response_str(),
                }

            case messages.RetryPrompt():
                if message.tool_name:
                    return {
                        "role": "tool",
                        "tool_call_id": message.tool_id,
                        "content": message.model_response(),
                    }
                return {"role": "user", "content": message.model_response()}

            case messages.ModelTextResponse():
                return {"role": "assistant", "content": message.content}

            case messages.ModelStructuredResponse():
                return {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": call.tool_id or f"call_{i}",
                            "type": "function",
                            "function": {
                                "name": call.tool_name,
                                "arguments": (
                                    call.args.args_json
                                    if isinstance(call.args, messages.ArgsJson)
                                    else json.dumps(call.args.args_dict)
                                ),
                            },
                        }
                        for i, call in enumerate(message.calls)
                    ],
                }

            case _:
                msg = f"Unknown message type: {type(message)}"
                raise ValueError(msg)

    def _process_response(self, response: ModelResponse) -> ModelAnyResponse:
        """Process a non-streaming response."""
        choice = response.choices[0]
        timestamp = datetime.fromtimestamp(response.created)

        if tool_calls := choice.message.tool_calls:
            return ModelStructuredResponse(
                calls=[
                    messages.ToolCall.from_json(
                        tool_call.function.name,
                        tool_call.function.arguments,
                        tool_call.id,
                    )
                    for tool_call in tool_calls
                ],
                timestamp=timestamp,
            )
        return ModelTextResponse(
            content=choice.message.content or "",
            timestamp=timestamp,
        )

    async def _process_stream_response(
        self, response: AsyncIterator[ModelResponse]
    ) -> models.EitherStreamedResponse:
        """Process a streaming response."""
        try:
            first_chunk = await anext(response)
        except StopAsyncIteration as e:
            msg = "Stream ended without content"
            raise UnexpectedModelBehavior(msg) from e

        timestamp = datetime.fromtimestamp(first_chunk.created)
        delta = first_chunk.choices[0].delta
        start_cost = self._calculate_cost(first_chunk)

        while not (delta.content or getattr(delta, "tool_calls", None)):
            try:
                chunk = await anext(response)
                delta = chunk.choices[0].delta
                start_cost += self._calculate_cost(chunk)
            except StopAsyncIteration as e:
                msg = "Stream ended without content or tool calls"
                raise UnexpectedModelBehavior(msg) from e

        if delta.content is not None:
            return LiteLLMStreamTextResponse(
                first_content=delta.content,
                response=response,
                _created_at=timestamp,
                start_cost=start_cost,
            )
        return LiteLLMStreamStructuredResponse(
            response=response,
            tool_calls={},  # Will be populated during streaming
            _created_at=timestamp,
            start_cost=start_cost,
        )

    def _calculate_cost(self, response: ModelResponse) -> Cost:
        """Calculate cost from a response."""
        if not hasattr(response, "usage"):
            return Cost()

        usage = response.usage
        details = {}

        # Add detailed token information if available
        if usage.completion_tokens_details:
            details.update(usage.completion_tokens_details.model_dump(exclude_none=True))
        if usage.prompt_tokens_details:
            details.update(usage.prompt_tokens_details.model_dump(exclude_none=True))

        return Cost(
            request_tokens=usage.prompt_tokens,
            response_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            details=details or None,
        )


@dataclass
class LiteLLMStreamTextResponse(models.StreamTextResponse):
    """Streaming text response implementation."""

    first_content: str | None
    response: AsyncIterator[ModelResponse]
    _created_at: datetime  # This needs to match what we pass in request_stream
    start_cost: Cost
    _current_cost: Cost = field(init=False, default_factory=Cost)
    _buffer: list[str] = field(init=False, default_factory=list)

    async def __anext__(self) -> None:
        if self.first_content is not None:
            self._buffer.append(self.first_content)
            self.first_content = None
            return

        try:
            chunk = await anext(self.response)
            if content := chunk.choices[0].delta.content:
                self._buffer.append(content)
                self._current_cost += self._calculate_chunk_cost(chunk)
        except StopAsyncIteration:
            raise

    def get(self, *, final: bool = False) -> Sequence[str]:
        chunks = self._buffer[:]
        self._buffer.clear()
        return chunks

    def cost(self) -> Cost:
        return self.start_cost + self._current_cost

    def timestamp(self) -> datetime:
        return self._created_at

    def _calculate_chunk_cost(self, chunk: ModelResponse) -> Cost:
        """Calculate cost from a chunk."""
        if not hasattr(chunk, "usage"):
            return Cost()

        usage = chunk.usage
        return Cost(
            request_tokens=usage.prompt_tokens
            if hasattr(usage, "prompt_tokens")
            else None,
            response_tokens=usage.completion_tokens
            if hasattr(usage, "completion_tokens")
            else None,
            total_tokens=usage.total_tokens if hasattr(usage, "total_tokens") else None,
        )


@dataclass
class LiteLLMStreamStructuredResponse(models.StreamStructuredResponse):
    """Streaming structured response implementation."""

    response: AsyncIterator[ModelResponse]
    tool_calls: dict[str, Any]
    _created_at: datetime
    start_cost: Cost
    _current_cost: Cost = field(init=False, default_factory=Cost)

    async def __anext__(self) -> None:
        try:
            chunk = await anext(self.response)
            delta = chunk.choices[0].delta
            if tool_calls := getattr(delta, "tool_calls", None):
                for tool_call in tool_calls:
                    self._process_tool_calls(tool_call)
            self._current_cost += self._calculate_cost(chunk)
        except StopAsyncIteration:
            raise

    def get(self, *, final: bool = False) -> ModelStructuredResponse:
        """Get current accumulated tool calls."""
        calls = []
        for call_id, call in self.tool_calls.items():
            if (
                "function" in call
                and call["function"].get("name")
                and call["function"].get("arguments")
            ):
                calls.append(
                    messages.ToolCall.from_json(
                        call["function"]["name"],
                        call["function"]["arguments"],
                        call_id,
                    )
                )
        return ModelStructuredResponse(calls=calls, timestamp=self._created_at)

    def _process_tool_calls(self, tool_call: Any) -> None:
        """Process a tool call chunk."""
        call_id = tool_call.id
        if not call_id:
            # Continuation of previous call
            for current in self.tool_calls.values():
                if func := current.get("function"):
                    if tool_call.function.name:
                        func["name"] = tool_call.function.name
                    if tool_call.function.arguments:
                        func["arguments"] = (
                            func.get("arguments", "") + tool_call.function.arguments
                        )
        else:
            # New call
            self.tool_calls[call_id] = {
                "id": call_id,
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments or "",
                },
            }

    def _calculate_cost(self, chunk: ModelResponse) -> Cost:
        """Calculate cost from a chunk."""
        if not hasattr(chunk, "usage"):
            return Cost()

        return Cost(
            response_tokens=getattr(chunk.usage, "completion_tokens", None),
            total_tokens=getattr(chunk.usage, "total_tokens", None),
        )

    def cost(self) -> Cost:
        return self.start_cost + self._current_cost

    def timestamp(self) -> datetime:
        return self._created_at


if __name__ == "__main__":
    import asyncio
    import os

    from pydantic import BaseModel

    async def main() -> None:
        # Create model (using OpenAI as example)
        model = LiteLLMModel(
            model_name="gpt-3.5-turbo",
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        # Create agent model with tool
        agent_model = await model.agent_model(
            function_tools={
                "calculate": {
                    "name": "calculate",
                    "description": "Calculate a mathematical expression",
                    "json_schema": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Math expression to evaluate",
                            }
                        },
                        "required": ["expression"],
                    },
                }
            },
            allow_text_result=True,
            result_tools=None,
        )

        # Example 1: Non-streaming tool request
        print("\nNon-streaming tool request:")
        messages_list = [
            messages.SystemPrompt(
                content="You are a helpful math assistant. Use the calculate tool."
            ),
            messages.UserPrompt(content="What is 15 * 17?"),
        ]
        response, cost = await agent_model.request(messages_list)
        print(f"Response: {response}")
        print(f"Cost: {cost}")

        # Example 2: Streaming text response
        print("\nStreaming text response:")
        messages_list = [
            messages.SystemPrompt(
                content="You are a helpful math assistant. Explain step by step without using tools."
            ),
            messages.UserPrompt(content="Explain step by step how to calculate 15 * 17"),
        ]

        async with agent_model.request_stream(messages_list) as stream:
            if isinstance(stream, models.StreamTextResponse):
                async for _ in stream:
                    for chunk in stream.get():
                        print(chunk, end="", flush=True)
                print(f"\nTotal cost: {stream.cost()}")
            else:
                print("\nReceived structured response instead of text:")
                async for _ in stream:
                    response = stream.get()
                    print(f"Tool calls: {response.calls}")
                print(f"\nTotal cost: {stream.cost()}")

    asyncio.run(main())
