#coding:utf-8
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app_orcamento.permissoes import group_required
from django.conf import settings
from django.db import transaction
from app_orcamento.forms.usuario import FormSalvarUsuario, FormSalvarPerfil
from app_orcamento.forms.pesquisa import FormPesquisa
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.core.paginator import Paginator


@transaction.commit_on_success
@group_required(settings.PERM_GRUPO_ADMINISTRADOR)
def adicionar(request):

    if request.method == 'POST':
        form = FormSalvarUsuario(request.POST)
        if form.is_valid():

            if str(settings.PERM_GRUPO_ADMINISTRADOR) in request.POST.getlist('grupos') \
                    and not request.user.is_superuser:
                return render(request, 'usuario/adicionar.html',
                              {	'form': form, 'msg_erro': 'Usuário logado não é "Super usuário", '
                                                             'não será possui criar usuário com grupo "Administrador"'})

            user = User.objects.create_user(request.POST['usuario'], request.POST['email'], request.POST['senha'])

            user.is_active = True
            user.first_name = request.POST['nome']
            user.last_name = request.POST['sobrenome']
            for gp in request.POST.getlist('grupos'):
                user.groups.add(gp)
            user.save()

            return redirect('/')
    else:
        form = FormSalvarUsuario()

    return render(request, 'usuario/adicionar.html', {	'form': form})


@transaction.commit_on_success
@group_required(settings.PERM_GRUPO_ADMINISTRADOR)
def editar(request, user_id):

    user = User.objects.get(pk=user_id)
    grupos_user = user.groups.values_list('id').all()
    msg_erro = None
    if request.method == 'POST':
        grupos_selecionado = request.POST.getlist('grupo')

        if str(settings.PERM_GRUPO_ADMINISTRADOR) in request.POST.getlist('grupo') and not request.user.is_superuser:
            msg_erro = 'Usuário logado não é "Super usuário", não será possui adicionar o "Administrador" ao usuário.'
        else:
            for grupo in grupos_selecionado:
                if (int(grupo),) not in grupos_user:
                    user.groups.add(grupo)

            for grupo in user.groups.all():
                print 'group : ',grupo
                if str(grupo.id) not in grupos_selecionado:
                    user.groups.remove(grupo)

            if 'ativo' in request.POST:
                user.is_active = True
            else:
                user.is_active = False

            user.save()
            return redirect('/admin/consulta/usuarios/')

    grupos = Group.objects.all()

    for gp in grupos:
        if (gp.id,) in grupos_user:
            gp.checked = 'checked'
        else:
            gp.checked = ''

    if user.is_active:
        user.checked = 'checked'
    else:
        user.checked = ''

    return render(request, 'usuario/editar.html', {'usuario': user, 'grupos': grupos, 'msg_erro': msg_erro})


@group_required(settings.PERM_GRUPO_ADMINISTRADOR)
def consulta(request):
    valor = None

    if request.method == 'POST':
        form = FormPesquisa(request.POST)

        if form.is_valid():
            valor = request.POST['valor']

    elif 'valor' in request.GET:
        valor = request.GET['valor']

    if valor is None or valor == 'None':
        form = FormPesquisa()
    else:
        data = {'valor': valor}
        form = FormPesquisa(initial=data)

    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1

    users = User.objects.filter(~Q(id=request.user.id))

    if not request.user.is_superuser:
        users = users.filter(Q(is_superuser=False), ~Q(groups__in=[settings.PERM_GRUPO_ADMINISTRADOR]))

    if valor is not None:
        users = users.filter(Q(firstname__icontains=valor) | Q(lastname__icontains=valor))

    paginator = Paginator(users, settings.NR_REGISTROS_PAGINA)

    try:
        users_page = paginator.page(page)
    except:
        users_page = paginator.page(paginator.num_pages)

    return render(request, 'usuario/consulta.html', {'form': form, 'usuarios': users_page})


@login_required
def salvar_perfil(request):

    if request.method == 'POST':
        form = FormSalvarPerfil(request.user.id, request.POST)

        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            if request.POST['nova_senha'] != '':
                user.set_password(request.POST['confirmar_senha'])

            user.first_name = request.POST['nome']
            user.last_name = request.POST['sobrenome']
            user.email = request.POST['email']

            user.save()

            logout(request)
            return redirect('/')
    else:
        data = {'nome': request.user.first_name, 'sobrenome': request.user.last_name,
                'email': request.user.email, 'usuario': request.user.username}
        form = FormSalvarPerfil(request.user.id, initial=data)

    return render(request, 'usuario/perfil.html', {	'form': form})
