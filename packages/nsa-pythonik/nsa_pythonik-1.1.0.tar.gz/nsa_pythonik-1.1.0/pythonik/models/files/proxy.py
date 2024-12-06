from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from pythonik.models.base import PaginatedResponse


class Resolution(BaseModel):
    height: Optional[int]
    width: Optional[int]


class Proxy(BaseModel):
    asset_id: Optional[str] = ""
    audio_bitrate: Optional[int] = None
    bit_rate: Optional[int] = None
    codec: Optional[str] = ""
    filename: Optional[str] = ""
    format: Optional[str] = ""
    frame_rate: Optional[str] = ""
    id: Optional[str] = ""
    is_drop_frame: Optional[bool] = None
    is_public: Optional[bool] = None
    multipart_upload_url: Optional[str] = ""
    name: Optional[str] = ""
    resolution: Optional[Resolution] = None
    rotation: Optional[int] = None
    size: Optional[int] = None
    start_time_code: Optional[str] = ""
    status: Optional[str] = ""
    storage_id: Optional[str] = ""
    storage_method: Optional[str] = ""
    upload_credentials: Optional[Dict[str, Any]] = {}
    upload_method: Optional[str] = ""
    upload_url: Optional[str] = ""
    url: Optional[str] = ""
    version_id: Optional[str] = ""


class Proxies(PaginatedResponse):
    objects: Optional[List[Proxy]] = []
