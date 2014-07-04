#coding: utf-8
from django import forms


class FormSalvarVendedor(forms.Form):
    nome = forms.CharField(max_length=30)
    sobrenome = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)
    ativo = forms.BooleanField()
    usuario = forms.CharField(max_length=30)
    senha = forms.CharField(widget=forms.PasswordInput())
