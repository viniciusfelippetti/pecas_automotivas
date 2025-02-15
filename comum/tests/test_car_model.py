from django.contrib.auth.models import Permission
from django.test import TestCase, Client
from comum.factories.car_model import CarModelFactory
from comum.factories.group import GroupFactory
from comum.factories.part import PartFactory
from comum.factories.permission import PermissionFactory
from comum.factories.user import UserFactory
from django.urls import reverse

from comum.models import CarModel, Part


class CarModelTest(TestCase):
    def setUp(self):
        self.client = Client()

        #Groups
        self.common_group = GroupFactory(name="comum")
        self.admin_group = GroupFactory(name="administrador")

        #Permissions
        self.add_car_model_permission = Permission.objects.get(codename="add_carmodel")
        self.view_car_model_permission = Permission.objects.get(codename="view_carmodel")
        self.change_car_model_permission = Permission.objects.get(codename="change_carmodel")
        self.delete_car_model_permission = Permission.objects.get(codename="delete_carmodel")
        self.add_part_permission = Permission.objects.get(codename="add_part")
        self.view_part_permission = Permission.objects.get(codename="view_part")
        self.change_part_permission = Permission.objects.get(codename="change_part")
        self.delete_part_permission = Permission.objects.get(codename="delete_part")

        self.common_group.permissions.add(
            self.view_car_model_permission,
            self.view_part_permission
        )
        self.admin_group.permissions.add(
            self.add_car_model_permission,
            self.view_car_model_permission,
            self.change_car_model_permission,
            self.delete_car_model_permission,
            self.add_part_permission,
            self.view_part_permission,
            self.change_part_permission,
            self.delete_part_permission
        )

        self.common_user = UserFactory(password="password123")
        self.common_user.groups.add(self.common_group)
        self.admin_user = UserFactory(password="password123")
        self.admin_user.groups.add(self.admin_group)
        self.part = PartFactory(part_number="EREIFHEIUF3929", name="teste", details="teste do Part", price=100.00, quantity=10)
        self.car_model = CarModelFactory(name="TORO", manufacturer="FIAT", year=1999)
        self.data = {
            "name": "gol",
            "manufacturer": "volkswagen",
            "year": 2010,
        }
        session = self.client.session
        session.save()

        self.common_token = self._get_jwt_token(self.common_user.username, "password123")
        self.admin_token = self._get_jwt_token(self.admin_user.username, "password123")


    def _get_jwt_token(self, username, password):
        # Assumindo que você tem um endpoint '/api/token/' para gerar o token JWT
        response = self.client.post(reverse("token_obtain_pair"), data={
            "username": username,
            "password": password,
        })
        return response.json().get("access")

    def test_create_car_model_without_permission(self):
        self.client.login(username=self.common_user.username, password="password123")
        response = self.client.post(
            path=reverse("car-model"),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.common_token}",  # Usuário comum não tem permissão
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['errors']['message'], 'Você não tem permissão para realizar esta ação.')

    def test_create_car_model_without_token(self):
        self.client.login(username=self.admin_user.username, password="password123")
        response = self.client.post(
            path=reverse("car-model"),
            data=self.data,
            content_type="application/json", # Usuário comum não tem permissão
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['errors']['message'], 'No Authorization header provided.')

    def test_create_car_model(self):
        self.client.login(username=self.admin_user.username, password="password123")
        response = self.client.post(
            path=reverse("car-model"),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_token}",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("name", response.json())

    def test_update_car_model(self):
        self.client.login(username=self.admin_user.username, password="password123")
        session = self.client.session
        session.save()
        update_data = {"year": "2020"}
        response = self.client.patch(
            path=reverse("manage-car-model", kwargs={"car_model_id": self.car_model.id}),
            data=update_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_token}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.json()["year"]), "2020")

    def test_update_car_model_without_permission(self):
        self.client.login(username=self.common_user.username, password="password123")
        session = self.client.session
        session.save()
        update_data = {"year": "2020"}
        response = self.client.patch(
            path=reverse("manage-car-model", kwargs={"car_model_id": self.car_model.id}),
            data=update_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.common_token}",
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['errors']['message'], 'Você não tem permissão para realizar esta ação.')

    def test_update_car_model_without_token(self):
        self.client.login(username=self.admin_user.username, password="password123")
        session = self.client.session
        session.save()
        update_data = {"year": "2020"}
        response = self.client.patch(
            path=reverse("manage-car-model", kwargs={"car_model_id": self.car_model.id}),
            data=update_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['errors']['message'], 'No Authorization header provided.')

    def test_delete_car_model(self):
        self.client.login(username=self.admin_user.username, password="password123")
        session = self.client.session
        session.save()
        response = self.client.delete(
            path=reverse("manage-car-model", kwargs={"car_model_id": self.car_model.id}),
            data=None,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_token}",
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_car_model_without_permission(self):
        self.client.login(email=self.common_user.email, password="password123")
        session = self.client.session
        session.save()

        response = self.client.delete(
            path=reverse("manage-car-model", kwargs={"car_model_id": self.car_model.id}),
            data=None,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.common_token}",
        )
        self.assertEqual(response.status_code, 500)

    def test_delete_car_model_without_token(self):
        self.client.login(email=self.common_user.email, password="password123")
        session = self.client.session
        session.save()

        response = self.client.delete(
            path=reverse("manage-car-model", kwargs={"car_model_id": self.car_model.id}),
            data=None,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['errors']['message'], 'No Authorization header provided.')


    def test_list_cars_models(self):
        self.client.login(username=self.admin_user.username, password="password123")
        session = self.client.session
        session.save()
        response = self.client.get(
            path=reverse("car-model"),
            data=None,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_list_cars_models_without_token(self):
        self.client.login(username=self.admin_user.username, password="password123")
        session = self.client.session
        session.save()
        response = self.client.get(
            path=reverse("car-model"),
            data=None,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['errors']['message'], 'No Authorization header provided.')

    def test_view_car_model(self):
        self.client.login(username=self.common_user.username, password="password123")
        session = self.client.session
        session.save()
        response = self.client.get(
            path=reverse("manage-car-model", kwargs={"car_model_id": self.car_model.id}),
            data=None,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.common_token}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'TORO')
        self.assertEqual(response.json()['manufacturer'], 'FIAT')

    def test_view_cars_model_part(self):
        self.client.login(username=self.common_user.username, password="password123")
        session = self.client.session
        session.save()
        response = self.client.get(
            path=reverse("cars-model-part", kwargs={"part_id": self.part.id}),
            data=None,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.common_token}",
        )
        self.assertEqual(response.status_code, 200)

    def test_view_cars_model_part_without_token(self):
        self.client.login(username=self.common_user.username, password="password123")
        session = self.client.session
        session.save()
        response = self.client.get(
            path=reverse("cars-model-part", kwargs={"part_id": self.part.id}),
            data=None,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['errors']['message'], 'No Authorization header provided.')

    def test_associate_parts_car_model(self):
        self.client.login(username=self.common_user.username, password="password123")
        session = self.client.session
        session.save()
        data = {
            "part_ids": [self.part.id],
            "car_model_ids": [self.car_model.id]
        }
        response = self.client.post(
            path=reverse("associate-parts-cars-model"),
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.common_token}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Peças associadas com sucesso')

    def test_associate_parts_car_model_without_token(self):
        self.client.login(username=self.common_user.username, password="password123")
        session = self.client.session
        session.save()
        data = {
            "part_ids": [self.part.id],
            "car_model_ids": [self.car_model.id]
        }
        response = self.client.post(
            path=reverse("associate-parts-cars-model"),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['detail'], 'As credenciais de autenticação não foram fornecidas.')