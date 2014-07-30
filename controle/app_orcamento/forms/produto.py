#coding: utf-8
from django import forms
from app_orcamento.models import Produto


class FormProduto(forms.ModelForm):

    def __init__(self, id=None, *args, **kwargs):
        if id:
            self.id = id
            produto = Produto.objects.get(pk=id)
            super(FormProduto, self).__init__(instance=produto, *args, **kwargs)
        else:
            super(FormProduto, self).__init__(*args, **kwargs)

    class Meta:
        model = Produto