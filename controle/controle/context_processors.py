from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
    'PERM_GRUPO_ADM': settings.PERM_GRUPO_ADM,
    'PERM_GRUPO_VENDEDOR': settings.PERM_GRUPO_VENDEDOR
    }