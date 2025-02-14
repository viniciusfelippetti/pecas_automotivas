from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from django_inscode.transports import Transport


@dataclass(frozen=True)
class PartTransport(Transport):
    part_number: str
    name: str
    details: str
    price: Decimal
    quantity: int
    updated_at: datetime