from django.contrib.auth.models import Permission
from django.test import TestCase, Client

from comum.factories.group import GroupFactory
from comum.factories.user import UserFactory
from django.urls import reverse
from comum.factories.part import PartFactory


class PartTest(TestCase):
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
        self.part = PartFactory(part_number="EREIFHEIUF3929", name="teste", details="teste do PArt", price=100.00, quantity=10)
        self.data = {
            "part_number": "ISSDIUGSFUGY",
            "name": "AMORTECEDOR",
            "details": "TEste amortecedor dusidfghfug",
            "price": "200.00",
            "quantity": "15",
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

    def test_create_part(self):
        self.client.login(username=self.admin_user.username, password="password123")
        response = self.client.post(
            path=reverse("part"),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_token}",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("part_number", response.json())

    def test_create_part_without_permission(self):
        self.client.login(username=self.common_user.username, password="password123")
        response = self.client.post(
            path=reverse("part"),
            data=self.data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.common_token}",
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['errors']['message'], 'Você não tem permissão para realizar esta ação.')

    def test_create_part_without_token(self):
        self.client.login(username=self.admin_user.username, password="password123")
        response = self.client.post(
            path=reverse("part"),
            data=self.data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['errors']['message'], 'No Authorization header provided.')

    def test_update_part(self):
        self.client.login(username=self.admin_user.username, password="password123")
        session = self.client.session
        session.save()
        update_data = {"details": "Rua nova"}
        response = self.client.patch(
            path=reverse("manage-part", kwargs={"part_id": self.part.id}),
            data=update_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_token}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["details"], "Rua nova")

    def test_update_part_without_permission(self):
        self.client.login(username=self.common_user.username, password="password123")
        session = self.client.session
        session.save()
        update_data = {"details": "Rua nova"}
        response = self.client.patch(
            path=reverse("manage-part", kwargs={"part_id": self.part.id}),
            data=update_data,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.common_token}",
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['errors']['message'], 'Você não tem permissão para realizar esta ação.')

    def test_update_part_without_token(self):
        self.client.login(username=self.common_user.username, password="password123")
        session = self.client.session
        session.save()
        update_data = {"details": "Rua nova"}
        response = self.client.patch(
            path=reverse("manage-part", kwargs={"part_id": self.part.id}),
            data=update_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['errors']['message'], 'No Authorization header provided.')

    def test_delete_part(self):
        self.client.login(username=self.admin_user.username, password="password123")
        session = self.client.session
        session.save()
        response = self.client.delete(
            path=reverse("manage-part", kwargs={"part_id": self.part.id}),
            data=None,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_token}",
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_part_without_permission(self):
        self.client.login(email=self.common_user.email, password="password123")
        session = self.client.session
        session.save()
        response = self.client.delete(
            path=reverse("manage-part", kwargs={"part_id": self.part.id}),
            data=None,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.common_token}",
        )
        self.assertEqual(response.status_code, 500)

    def test_delete_part_without_token(self):
        self.client.login(email=self.common_user.email, password="password123")
        session = self.client.session
        session.save()
        response = self.client.delete(
            path=reverse("manage-part", kwargs={"part_id": self.part.id}),
            data=None,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 500)

    def test_list_parts_filter(self):
        self.client.login(username=self.common_user.username, password="password123")
        session = self.client.session
        session.save()
        response = self.client.get(
            path=reverse("part"),
            data=None,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.common_token}",
        )
        self.assertEqual(response.status_code, 200)