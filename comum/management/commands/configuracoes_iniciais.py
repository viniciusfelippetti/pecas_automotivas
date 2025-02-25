from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from comum.models import Users


def criar_grupos_e_usuarios():
    # Grupos
    grupo_administrador = Group.objects.create(name='administrador')
    grupo_comum = Group.objects.create(name='comum')
    all_permissions = Permission.objects.all()
    for permission in all_permissions:
        grupo_administrador.permissions.add(permission)

    view_car_model_permission = Permission.objects.get(codename="view_carmodel")
    view_part_permission = Permission.objects.get(codename="view_part")

    grupo_comum.permissions.add(view_car_model_permission, view_part_permission)


    print("Grupos e permissões criados/verificados.")

class Command(BaseCommand):
    help = 'Cria grupos, permissões e usuários iniciais.'

    def handle(self, *args, **options):
        criar_grupos_e_usuarios()
        self.stdout.write(self.style.SUCCESS('Configurações iniciais aplicadas.'))