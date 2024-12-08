"""Database models and utilities for logging agent interactions."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, ClassVar

from pydantic_ai import messages
from pydantic_ai.result import Cost, RunResult
from sqlmodel import JSON, Field, Session, SQLModel, create_engine


class InteractionType(str, Enum):
    """Types of agent interactions to log."""

    AGENT_START = "agent_start"
    AGENT_COMPLETE = "agent_complete"
    AGENT_ERROR = "agent_error"
    MODEL_REQUEST = "model_request"
    MODEL_RESPONSE = "model_response"
    TOOL_CALL = "tool_call"
    TOOL_RETURN = "tool_return"
    STREAM_START = "stream_start"
    STREAM_CHUNK = "stream_chunk"
    STREAM_COMPLETE = "stream_complete"
    VALIDATION = "validation"


class AgentInteraction(SQLModel, table=True):
    """Log entry for agent interactions."""

    id: int | None = Field(default=None, primary_key=True)
    agent_name: str = Field(index=True)
    interaction_type: InteractionType = Field(index=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: str = Field(index=True)

    # Input
    prompt: str | None = None
    messages: list[messages.Message] | None = Field(default=None, sa_column=JSON)
    model_name: str | None = None

    # Tool information
    tool_name: str | None = None
    tool_args: dict[str, Any] | None = Field(default=None, sa_column=JSON)
    tool_result: Any | None = Field(default=None, sa_column=JSON)

    # Results
    result: Any | None = Field(default=None, sa_column=JSON)
    total_tokens: int | None = None
    cost: Cost | None = Field(default=None, sa_column=JSON)
    duration_ms: float | None = None

    # Error info
    error: str | None = None
    error_traceback: str | None = None

    model_config = {"arbitrary_types_allowed": True}


class AgentLogger:
    """Database logger for agent interactions."""

    _engine: ClassVar[Any] = None

    def __init__(
        self,
        agent_name: str,
        session_id: str,
        db_url: str = "sqlite:///agent_logs.db",
    ) -> None:
        """Initialize the logger."""
        self.agent_name = agent_name
        self.session_id = session_id

        if not AgentLogger._engine:
            AgentLogger._engine = create_engine(db_url)
            SQLModel.metadata.create_all(AgentLogger._engine)

    async def log_start(
        self,
        prompt: str,
        messages: list[messages.Message],
        model_name: str,
    ) -> None:
        """Log start of agent run."""
        await self._log(
            InteractionType.AGENT_START,
            prompt=prompt,
            messages=messages,
            model_name=model_name,
        )

    async def log_complete(
        self,
        result: RunResult[Any],
        duration_ms: float,
    ) -> None:
        """Log completion of agent run."""
        await self._log(
            InteractionType.AGENT_COMPLETE,
            result=result.data,
            messages=result.messages,
            duration_ms=duration_ms,
            total_tokens=result.usage.total_tokens if result.usage else None,
            cost=result.cost,
        )

    async def log_model_request(
        self,
        messages: list[messages.Message],
    ) -> None:
        """Log model request."""
        await self._log(
            InteractionType.MODEL_REQUEST,
            messages=messages,
        )

    async def log_model_response(
        self,
        response: messages.ModelAnyResponse,
        cost: Cost,
    ) -> None:
        """Log model response."""
        await self._log(
            InteractionType.MODEL_RESPONSE,
            result=response.model_dump(),
            cost=cost,
        )

    async def log_tool_call(
        self,
        tool_name: str,
        tool_args: dict[str, Any],
    ) -> None:
        """Log tool call."""
        await self._log(
            InteractionType.TOOL_CALL,
            tool_name=tool_name,
            tool_args=tool_args,
        )

    async def log_tool_return(
        self,
        tool_name: str,
        result: Any,
        duration_ms: float,
    ) -> None:
        """Log tool return."""
        await self._log(
            InteractionType.TOOL_RETURN,
            tool_name=tool_name,
            tool_result=result,
            duration_ms=duration_ms,
        )

    async def log_validation(
        self,
        result: Any,
        validation_name: str,
        retry_count: int,
    ) -> None:
        """Log result validation."""
        await self._log(
            InteractionType.VALIDATION,
            result=result,
            tool_name=validation_name,  # Reuse field for validator name
            tool_args={"retry_count": retry_count},  # Reuse field for retry info
        )

    async def log_error(
        self,
        error: Exception,
        interaction_type: InteractionType,
        duration_ms: float | None = None,
    ) -> None:
        """Log error."""
        import traceback
        await self._log(
            interaction_type,
            error=str(error),
            error_traceback=traceback.format_exc(),
            duration_ms=duration_ms,
        )

    async def _log(
        self,
        interaction_type: InteractionType,
        **data: Any,
    ) -> None:
        """Internal method to log an interaction."""
        interaction = AgentInteraction(
            agent_name=self.agent_name,
            session_id=self.session_id,
            interaction_type=interaction_type,
            **data,
        )

        with Session(AgentLogger._engine) as session:
            session.add(interaction)
            session.commit()
