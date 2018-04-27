from django.shortcuts import render
from docencia.models import Universidad


def index(request):
    context = {
        "universidades": Universidad.objects.all(),
    }

    return render(request, 'tizanegra/index.html', context)
