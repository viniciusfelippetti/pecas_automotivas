from dataclasses import dataclass
from uuid import UUID

from django_inscode.transports import Transport


@dataclass(frozen=True)
class BaseTransport(Transport):
    pass