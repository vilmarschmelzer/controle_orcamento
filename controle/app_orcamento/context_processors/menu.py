#coding: utf-8
from django.conf import settings

class Menu:
    nome = None
    url = None
    itens = []


def get_menu(request):
    html = ''
    if request.user.is_authenticated():

        grupos_id = request.user.groups.values_list('id',flat=True).all()
        if settings.PERM_GRUPO_ADMINISTRADOR in grupos_id:
            html += '''<li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                        Administração
                        <b class="caret"></b>
                    </a>
                    <ul class="dropdown-menu">
                        <li>
                            <a href="/admin/consulta/usuarios/" class="addlink">Usuários</a>
                        </li>
                        <li>
                            <a href="/admin/add/usuario/" class="addlink">Adicionar usuário</a>
                        </li>
                        <li>
                            <a href="/produto/salvar/" class="addlink">Cadastro de produto</a>
                        </li>
                        <li>
                            <a href="/produto/consultar/" class="addlink">Consultar produtos</a>
                        </li>
                    </ul>
                </li>'''

            if settings.PERM_GRUPO_VENDEDOR not in grupos_id:
                html += '''<li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                        Cliente
                        <b class="caret"></b>
                    </a>
                    <ul class="dropdown-menu">
                        <li>
                            <a href="/cliente/consulta/" class="addlink">Consultar</a>
                        </li>
                    </ul>
                </li>'''

        if settings.PERM_GRUPO_VENDEDOR in grupos_id:
            html += '''<li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                        Orçamento
                        <b class="caret"></b>
                    </a>
                    <ul class="dropdown-menu">
                        <li>
                            <a href="/orcamento/salvar/" class="addlink">Criar</a>
                        </li>
                        <li>
                            <a href="/orcamento/consulta/" class="addlink">Consultar</a>
                        </li>
                    </ul>
                </li>
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                        Cliente
                        <b class="caret"></b>
                    </a>
                    <ul class="dropdown-menu">
                        <li>
                            <a href="/cliente/salvar/" class="addlink">Cadastrar</a>
                        </li>
                        <li>
                            <a href="/cliente/consulta/" class="addlink">Consultar</a>
                        </li>
                    </ul>
                </li>'''

    return {'menu':html}