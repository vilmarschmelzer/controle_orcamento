from django.db import models

class Cliente(models.Model):
    documento = models.CharField(max_length=14)
    nome = models.CharField(max_length=200)

    class Meta:
        app_label = 'orcamento'