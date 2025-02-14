from django_inscode.services import ModelService
from comum.repositories import part_repository


class PartService(ModelService):
    def __init__(
        self,
    ):
        self.part_repository = part_repository
        super().__init__(part_repository)

part_service = PartService()