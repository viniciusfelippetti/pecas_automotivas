from dataclasses import dataclass
from typing import List
from uuid import UUID

from comum.base_transport import BaseTransport


@dataclass(frozen=True)
class UserTransport(BaseTransport):
    username: str
    email: str

@dataclass(frozen=True)
class AddUserGroupTransport(BaseTransport):
    group_ids: List[UUID]