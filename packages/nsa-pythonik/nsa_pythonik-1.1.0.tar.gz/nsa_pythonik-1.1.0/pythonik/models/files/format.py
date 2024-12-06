from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from pythonik.models.base import Status, ArchiveStatus, PaginatedResponse


class Component(BaseModel):
    id: Optional[str] = ""
    metadata: Optional[dict]
    name: Optional[str] = ""
    type: Optional[str] = ""


class Format(BaseModel):
    archive_status: Optional[ArchiveStatus] = None
    asset_id: Optional[str] = ""
    components: Optional[List[Component]] = []
    date_deleted: Optional[str] = ""
    deleted_by_user: Optional[str] = ""
    id: Optional[str] = ""
    is_online: Optional[bool] = None
    metadata: List[dict] = []
    name: Optional[str] = ""
    status: Optional[Status] = Status.ACTIVE
    storage_methods: List[str] = []
    user_id: Optional[str] = ""
    version_id: Optional[str] = ""
    warnings: Optional[List[str]] = []


class FormatCreate(Format):
    name: str
    is_online: bool = True
    metadata: Optional[List[dict]] = []
    storage_methods: List[str] = ["FILE"]


class Formats(PaginatedResponse):
    objects: Optional[List[Format]] = []
