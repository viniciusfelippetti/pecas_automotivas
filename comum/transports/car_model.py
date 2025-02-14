from dataclasses import dataclass
from typing import List
from uuid import UUID
from django_inscode.transports import Transport
from comum.base_transport import BaseTransport

@dataclass(frozen=True)
class CarModelTransport(Transport):
    name: str
    manufacturer: str
    year: int

class PartsToRemoveTransport(BaseTransport):
    part_ids: List[UUID]