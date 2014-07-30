# coding:utf-8
from django.shortcuts import redirect
from django.contrib.auth.models import Group, User
from django.db import transaction


@transaction.commit_on_success
def carga(request):

    #Administrador
    grupo_admin = 'Administrador'
    grupo_vendedor = 'Vendedor'

    gp_administrador = Group.objects.filter(name=grupo_admin)

    if len(gp_administrador) == 0:
        gp_administrador = Group(name=grupo_admin)
        gp_administrador.save()
    else:
        gp_administrador = gp_administrador.get()

    #Vendedor
    gp_vendedor = Group.objects.filter(name=grupo_vendedor)

    if len(gp_vendedor) == 0:
        gp_vendedor = Group(name=grupo_vendedor)
        gp_vendedor.save()
    else:
        gp_vendedor = gp_vendedor.get()

    admin = 'admin'

    user = User.objects.filter(username=admin)

    if len(user) == 0:

        user = User.objects.create_user(admin, '', 'teste')
        user.is_superuser = True
        user.save()
    else:
        user = user.get()

    user.groups.add(gp_administrador)
    user.groups.add(gp_vendedor)

    return redirect('/')