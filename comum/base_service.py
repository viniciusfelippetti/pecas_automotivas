from typing import Any, Protocol
from uuid import UUID


class RepositoryProtocol(Protocol):
    def create(self, **kwargs) -> Any: ...
    def read(self, id: UUID) -> Any: ...
    def update(self, id: UUID, **kwargs) -> Any: ...
    def delete(self, id: UUID) -> Any: ...
    def filter(self, **kwargs) -> Any: ...


class BaseService:
    def __init__(self, repository: RepositoryProtocol) -> None:
        self._repository = repository

    def add(self, **kwargs) -> Any:
        return self._repository.create(**kwargs)

    def read_by_id(self, id: UUID) -> Any:
        return self._repository.read(id)

    def patch_by_id(self, id: UUID, **kwargs) -> Any:
        return self._repository.update(id, **kwargs)

    def remove_by_id(self, id: UUID) -> Any:
        return self._repository.delete(id)

    def filter_by_attrs(self, **kwargs) -> Any:
        return self._repository.filter(**kwargs)