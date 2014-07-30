#coding: utf-8
from django import forms
from django.contrib.auth.models import Group, User
from django.db.models import Q


class FormSalvarUsuario(forms.Form):
    nome = forms.CharField(max_length=30)
    sobrenome = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)
    usuario = forms.CharField(max_length=30)
    senha = forms.CharField(widget=forms.PasswordInput())
    grupos = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)

    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']

        existe = User.objects.filter(username=usuario)

        if len(existe) > 0:
            raise forms.ValidationError('Usuário já cadastrado')

        return usuario


class FormSalvarPerfil(FormSalvarUsuario):

    id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'id'}), required=False)
    nova_senha = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput(), required=False)
    usuario = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'readonly': True}))

    def __init__(self, id, *args, **kwargs):
        super(FormSalvarPerfil, self).__init__(*args, **kwargs)
        self.fields.pop('grupos')
        self.fields['id'].initial = id

    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']

        existe = User.objects.filter(Q(username=usuario), ~Q(id=self.fields['id'].initial))

        if len(existe) > 0:
            raise forms.ValidationError('Usuário já cadastrado')

        return usuario

    def clean_senha(self):
        senha = self.cleaned_data['senha']

        if self.fields['id'].initial > 0:
            user = User.objects.filter(id=self.fields['id'].initial, username=self.cleaned_data['usuario']).get()
            if user.check_password(self.cleaned_data['senha']) is False:
                raise forms.ValidationError('Senha invalida!')

        return senha

    def clean_confirmar_senha(self):
        if 'nova_senha' not in self.cleaned_data and self.cleaned_data['confirmar_senha'] != self.cleaned_data['senha']:
            raise forms.ValidationError('Confirmação da senha não confere!')

        if 'nova_senha' in self.cleaned_data and self.cleaned_data['confirmar_senha'] != self.cleaned_data['nova_senha']:
            raise forms.ValidationError('Confirmação da senha não confere!')

        return self.cleaned_data['confirmar_senha']