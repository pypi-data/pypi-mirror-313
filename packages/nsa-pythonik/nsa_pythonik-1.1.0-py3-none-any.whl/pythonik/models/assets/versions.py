from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from pythonik.models.base import Status, ArchiveStatus, UserInfo

class AssetVersionCreate(BaseModel):
    copy_metadata: bool = True
    copy_segments: bool = True
    include_segment_types: Optional[List[str]] = None
    source_version_id: Optional[str] = None

class AssetVersion(BaseModel):
    analyze_status: str
    archive_status: ArchiveStatus
    created_by_user: str
    created_by_user_info: UserInfo
    date_created: datetime
    face_recognition_status: str
    has_unconfirmed_persons: bool
    id: str
    is_online: bool
    person_ids: List[str]
    status: Status
    transcribe_status: str
    version_number: int

class AssetVersionResponse(BaseModel):
    asset_id: str
    system_domain_id: str
    versions: List[AssetVersion]

class AssetVersionFromAssetCreate(BaseModel):
    copy_previous_version_segments: bool = True
    include_segment_types: Optional[List[str]] = None
    source_metadata_asset_id: Optional[str] = None