from django_inscode.services import ModelService
from comum.repositories import car_model_repository


class CarModelService(ModelService):
    def __init__(
        self,
    ):
        self.car_model_repository = car_model_repository
        super().__init__(car_model_repository)

car_model_service = CarModelService()