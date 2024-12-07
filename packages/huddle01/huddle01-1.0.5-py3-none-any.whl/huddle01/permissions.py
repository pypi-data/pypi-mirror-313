from typing import Optional

from pydantic import BaseModel


class ProduceSources(BaseModel):
    cam: bool
    mic: bool
    screen: bool


class ACL(BaseModel):
    admin: bool
    can_consume: bool
    can_produce: bool
    can_produce_sources: ProduceSources
    can_send_data: bool
    can_recv_data: bool
    can_update_metadata: bool


class Permissions:
    def __init__(self, acl: ACL, role: Optional[str]):
        self.acl = acl
        self.role = role
