from __future__ import annotations

from typing import Any, Dict, Optional, List

from pydantic import BaseModel
from pythonik.models.base import PaginatedResponse


class Storage(BaseModel):
    default: Optional[bool] = None
    description: Optional[str] = ""
    id: Optional[str] = ""
    last_scanned: Optional[str] = ""
    method: Optional[str] = ""
    name: Optional[str] = ""
    purpose: Optional[str] = ""
    scanner_status: Optional[str] = ""
    settings: Optional[Dict[str, Any]] = {}
    status: Optional[str] = ""
    status_message: Optional[str] = ""
    version: Optional[str] = ""


class Storages(PaginatedResponse):
    objects: Optional[List[Storage]] = []
