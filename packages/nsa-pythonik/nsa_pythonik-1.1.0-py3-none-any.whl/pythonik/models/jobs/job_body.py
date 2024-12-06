from __future__ import annotations
from enum import Enum

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class JobStatus(str, Enum):
    """
    Possible Job statuses
    """

    READY = "READY"
    STARTED = "STARTED"
    FINISHED = "FINISHED"
    FINISHED_WITH_WARNING = "FINISHED_WITH_WARNING"
    FAILED = "FAILED"
    WAITING = "WAITING"
    ABORT_PENDING = "ABORT_PENDING"
    ABORTED = "ABORTED"
    SKIPPED = "SKIPPED"
    PAUSED = "PAUSED"
    EMPTY = ""


class JobTypes(str, Enum):
    """
    Possible Job types
    """

    TRANSFER = "TRANSFER"
    COPY = "COPY"
    CUSTOM = "CUSTOM"
    EMPTY = ""


class ABORT(BaseModel):
    bulk: Optional[bool] = None
    url: Optional[str] = ""


class CHANGEPRIORITY(BaseModel):
    bulk: Optional[bool] = None
    url: Optional[str] = ""


class PAUSE(BaseModel):
    bulk: Optional[bool] = None
    url: Optional[str] = ""


class RESTART(BaseModel):
    bulk: Optional[bool] = None
    url: Optional[str] = ""


class RESUME(BaseModel):
    bulk: Optional[bool] = None
    url: Optional[str] = ""


class ActionContext(BaseModel):
    ABORT: Optional[ABORT]
    CHANGE_PRIORITY: Optional[CHANGEPRIORITY]
    PAUSE: Optional[PAUSE]
    RESTART: Optional[RESTART]
    RESUME: Optional[RESUME]


class RelatedObject(BaseModel):
    object_id: Optional[str] = ""
    object_type: Optional[str] = ""


class JobBody(BaseModel):
    action_context: Optional[ActionContext] = None
    completed_at: Optional[str] = ""
    custom_type: Optional[JobTypes] = JobTypes.EMPTY.value
    error_message: Optional[str] = ""
    has_children: Optional[bool] = None
    job_context: Optional[Dict[str, Any]] = {}
    message: Optional[str] = ""
    metadata: Optional[Dict[str, Any]] = {}
    object_id: Optional[str] = ""
    object_type: Optional[str] = ""
    parent_id: Optional[str] = ""
    progress_processed: Optional[int] = None
    progress_total: Optional[int] = None
    related_objects: Optional[List[RelatedObject]] = []
    started_at: Optional[str] = ""
    status: Optional[JobStatus] = JobStatus.EMPTY.value
    title: Optional[str] = ""
    type: Optional[str] = ""
