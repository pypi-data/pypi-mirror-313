from enum import Enum
from typing import Dict, Optional, Union
from urllib.parse import urljoin

import aiohttp
from pydantic import BaseModel

from .log import base_logger

INFRA_URL = "https://infra-api.huddle01.workers.dev"
MAX_METADATA_SIZE = 5 * 1024  # 5KB

logger = base_logger.getChild("AccessToken")


class Role(str, Enum):
    HOST = "host"
    CO_HOST = "coHost"
    SPEAKER = "speaker"
    LISTENER = "listener"
    GUEST = "guest"
    BOT = "bot"


class ProduceSources(BaseModel):
    cam: bool
    mic: bool
    screen: bool

    class Config:
        populate_by_name = True
        alias_generator = lambda string: "".join(  # noqa: E731
            word.capitalize() if i > 0 else word
            for i, word in enumerate(string.split("_"))
        )


class Permissions(BaseModel):
    admin: bool = False
    can_consume: bool = True
    can_produce: bool = True
    can_produce_sources: ProduceSources = ProduceSources(
        cam=True, mic=True, screen=True
    )
    can_send_data: bool = True
    can_recv_data: bool = True
    can_update_metadata: bool = True

    class Config:
        allow_population_by_field_name = True
        alias_generator = lambda string: "".join(  # noqa: E731
            word.capitalize() if i > 0 else word
            for i, word in enumerate(string.split("_"))
        )


DEFAULT_PERMISSIONS = Permissions()

ROLE_PERMISSIONS: Dict[Role, Permissions] = {
    Role.HOST: Permissions(admin=True),
    Role.CO_HOST: Permissions(admin=True),
    Role.LISTENER: Permissions(
        can_consume=True,
        can_produce=False,
        can_produce_sources=ProduceSources(cam=False, mic=False, screen=False),
    ),
    Role.SPEAKER: Permissions(
        can_produce=True,
        can_produce_sources=ProduceSources(cam=False, mic=True, screen=True),
    ),
    Role.BOT: Permissions(
        can_consume=True,
        can_produce=False,
        can_produce_sources=ProduceSources(cam=False, mic=False, screen=False),
        can_recv_data=False,
        can_send_data=False,
        can_update_metadata=False,
    ),
    Role.GUEST: DEFAULT_PERMISSIONS,
}


class AccessTokenOptions(BaseModel):
    ttl: Union[int, str] = "4h"
    max_peers_allowed: Optional[int] = None
    metadata: Optional[str] = None


class AccessTokenData(BaseModel):
    api_key: str
    room_id: str
    role: Optional[Union[Role, str]] = None
    permissions: Optional[Permissions] = None
    options: Optional[AccessTokenOptions] = None


class AccessToken:
    """
    AccessToken is a class that represents a token that can be used to connect to a room.

    Args:
        data (AccessTokenData): The data required to create the token.

    Attributes:
        api_key (str): The API key to use.
        room_id (str): The room ID to connect to.
        role (Role): The role of the user in the room.
        permissions (Permissions): The permissions of the user in the room.
        options (AccessTokenOptions): The options for the token.

    Example:
        ```python
        data = AccessToken
        token = AccessToken(data)

        jwt = await token.to_jwt()
    """

    def __init__(self, data: AccessTokenData):
        self.api_key = data.api_key
        self.room_id = data.room_id
        self.role: Optional[Role] = None
        self.permissions: Optional[Permissions] = data.permissions
        self.options: AccessTokenOptions = data.options or AccessTokenOptions()

        if data.role:
            if isinstance(data.role, Role) and not data.permissions:
                self.role = data.role
                self.permissions = ROLE_PERMISSIONS[data.role]
            elif isinstance(data.role, Role) and data.permissions:
                self.role = data.role
                self.permissions = Permissions(
                    **{**ROLE_PERMISSIONS[data.role].dict(), **data.permissions.dict()}
                )
            elif isinstance(data.role, str) and data.permissions:
                if len(data.role) > 20:
                    raise ValueError(
                        "Role name is too long, must be less than 20 characters"
                    )

                self.role = Role(data.role)
                self.permissions = Permissions(
                    **{
                        **ROLE_PERMISSIONS[Role(data.role)].dict(),
                        **data.permissions.dict(),
                    }
                )

        elif data.permissions:
            self.permissions = Permissions(
                **{**DEFAULT_PERMISSIONS.dict(), **data.permissions.dict()}
            )

        else:
            raise ValueError("Role or permissions must be provided")

    async def to_jwt(self) -> str:
        """
        Create a JWT token to connect to a room, using the data provided.
        """

        logger.info("Creating Access Token")

        # Use default permissions if none are specified
        permissions_dict = (
            self.permissions.dict(by_alias=True)
            if self.permissions
            else DEFAULT_PERMISSIONS.dict(by_alias=True)
        )

        payload = {
            "roomId": self.room_id,
            "permissions": permissions_dict,
            "role": self.role,
        }

        if self.options.metadata:
            if len(self.options.metadata) > MAX_METADATA_SIZE:
                raise ValueError(f"Metadata size exceeds {MAX_METADATA_SIZE} bytes")

            payload["metadata"] = self.options.metadata

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "Cache-Control": "no-store, max-age=0",
            "Pragma": "no-cache",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                urljoin(INFRA_URL, "/api/v2/sdk/create-peer-token"),
                json=payload,
                headers=headers,
            ) as response:
                if response.status == 401:
                    raise ValueError(f"Invalid API key: {self.api_key}")
                if response.status == 404:
                    raise ValueError(f"Invalid room ID: {self.room_id}")
                if response.status != 200:
                    raise Exception(
                        f"Failed to create token. Status: {response.status}"
                    )

                data = await response.json()

                return data["token"]
