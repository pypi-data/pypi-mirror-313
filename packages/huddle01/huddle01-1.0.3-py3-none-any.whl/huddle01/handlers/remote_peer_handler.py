from typing import Optional

from pydantic import BaseModel


class RemotePeerEvents(str):
    StreamAvailable = "stream_available"
    StreamPlayable = "stream_playable"
    StreamClosed = "stream_closed"
    StreamPaused = "stream_paused"
    MetaDataUpdated = "metadata_updated"
    RoleUpdated = "role_updated"


class StreamCloseReason(BaseModel):
    code: int
    tag: str
    message: str


class StreamClosedEvent(BaseModel):
    label: str
    reason: Optional[StreamCloseReason]
