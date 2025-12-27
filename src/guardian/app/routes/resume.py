"""Workflow resumption API endpoints.

This module provides endpoints for resuming paused LangGraph workflows that
require human-in-the-loop (HITL) approval. Operators can submit decisions
to continue, approve, or reject paused workflow executions.

Author:
    Ruslan Magana (ruslanmv.com)

License:
    Apache 2.0

Copyright:
    Copyright (c) 2025 Ruslan Magana Vsevolodovna
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Body, HTTPException, Path


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/threads/{thread_id}/resume", summary="Resume a paused workflow")
def resume_thread(
    thread_id: str = Path(..., description="The unique ID of the paused workflow thread"),
    decision: str = Body(
        ..., embed=True, description="The human operator's decision (e.g., 'approve', 'reject')",
    ),
    comment: str | None = Body(
        None, embed=True, description="An optional comment from the operator",
    ),
) -> dict[str, Any]:
    """Resume a paused LangGraph workflow with operator decision.

    This endpoint is called by an operator (or an automated system) to resume
    a LangGraph workflow that was paused for human-in-the-loop (HITL) approval.
    The operator's decision and optional comment are passed to the workflow
    execution context.

    Args:
        thread_id: The unique identifier of the paused workflow thread
        decision: The operator's decision (e.g., "approve", "reject", "modify")
        comment: Optional comment providing additional context for the decision

    Returns:
        Dict[str, Any]: A dictionary containing:
            - thread_id (str): The workflow thread identifier
            - status (str): The new status after resumption
            - decision (str): The decision that was submitted
            - comment (Optional[str]): The operator's comment, if provided

    Raises:
        HTTPException: 500 error if the workflow thread fails to resume

    Example:
        >>> # POST /threads/abc123/resume
        >>> # Body: {"decision": "approve", "comment": "Looks good"}
        >>> {
        ...     "thread_id": "abc123",
        ...     "status": "resumed",
        ...     "decision": "approve",
        ...     "comment": "Looks good"
        ... }
    """
    try:
        # In a real implementation, you would use the LangGraph checkpointer
        # to load the thread's state and pass the decision to resume execution.
        logger.info(
            f"Resuming thread '{thread_id}' with decision '{decision}'"
            + (f" and comment '{comment}'" if comment else ""),
        )

        # Example: checkpointer.resume(
        #     thread_id,
        #     decision_data={"decision": decision, "comment": comment}
        # )

        return {
            "thread_id": thread_id,
            "status": "resumed",
            "decision": decision,
            "comment": comment,
        }
    except Exception as e:
        logger.error(f"Failed to resume thread {thread_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to resume workflow thread")


__all__ = ["router"]
