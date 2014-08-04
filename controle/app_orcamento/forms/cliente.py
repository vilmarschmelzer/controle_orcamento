#coding: utf-8
from django import forms
from app_orcamento.models import Cliente, Estado, Cidade, TipoContato
from utils.verificadorcpf import CPF
from utils.verificadorcnpj import CNPJ
from django.db.models import Q
import re

# traduz 123.456.789-10 para 12345678910
_translate = lambda doc: ''.join(re.findall("\d", doc))


def valida_documento(doc):

    doc_valido = CPF(doc).isValid()

    if doc_valido is False:
        try:
            doc_valido = CNPJ(doc).valido()
        except:
            doc_valido = False

    return doc_valido


def valida_existe_cliente(documento, id=None):

    if id is not None:
        qy = Cliente.objects.filter(Q(documento=documento), ~Q(id=int(id)))
    else:
        qy = Cliente.objects.filter(Q(documento=documento))

    return len(qy.all())>0


class FormCliente(forms.Form):

    def __init__(self, estado_id, id=0, *args, **kwargs):

        super(FormCliente, self).__init__(*args, **kwargs)

        if estado_id == '':
            estado_id = None

        self.fields['id'] = forms.IntegerField(initial=id, widget=forms.HiddenInput(attrs={'id': 'id'}), required=False)
        self.fields['documento'] = forms.CharField(max_length=18, widget=forms.TextInput(attrs={'id': 'documento'}))
        self.fields['nome'] = forms.CharField(max_length=200)
        self.fields['estado'] = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'estado'}),
                                                       queryset=Estado.objects.all(), empty_label="Selecione um Estado")

        self.fields['cidade'] = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'cidade'}),
                                                       queryset=Cidade.objects.filter(estado_id=estado_id).all(),
                                                       empty_label="Selecione uma Cidade")

        self.fields['bairro'] = forms.CharField(max_length=200)
        self.fields['cep'] = forms.IntegerField()
        self.fields['rua'] = forms.CharField(max_length=200)
        self.fields['numero'] = forms.CharField(max_length=100)
        self.fields['referencia'] = forms.CharField(max_length=200, widget=forms.Textarea, required=False)

    def get_documento(self):
        doc = self.cleaned_data['documento']
        if not doc.isdigit():
            doc = _translate(doc)

        return doc

    def clean_documento(self):
        doc = self.get_documento()
        if valida_documento(doc):
            if valida_existe_cliente(doc, self.fields['id'].initial):
                raise forms.ValidationError('Cliente já cadastrado!')
        else:
            raise forms.ValidationError('Documento inválido!')

        return doc


class FormContato(forms.Form):

    tipo_contato = forms.ModelChoiceField(widget=forms.Select(attrs={'id': 'TipoContato'}),
                                          queryset=TipoContato.objects.all(),
                                          empty_label="Selecione um tipo de contato")
    contato = forms.CharField(max_length=200)
