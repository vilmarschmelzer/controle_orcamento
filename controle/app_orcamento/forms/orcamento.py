#coding: utf-8
from django import forms


class FormOrcamento(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'id'}), required=False)
    cliente = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'id': 'cliente'}))
    aprovado = forms.NullBooleanField(widget=forms.Select(choices=((-1, 'Aguardando'), (1, 'Sim'), (0, 'Não')))
                                      , required=False)
    observacao = forms.CharField(widget=forms.Textarea, max_length=250, required=False)
    nr_dias_validade = forms.IntegerField(min_value=1, initial=1)


class FormItem(forms.Form):
    produto = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'id': 'produto'}))
    valor = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'id': 'valor'}))
    quantidade = forms.FloatField(min_value=0.1)
    observacao = forms.CharField(widget=forms.Textarea, max_length=250, required=False)
    vl_desconto = forms.FloatField(min_value=0, required=False)