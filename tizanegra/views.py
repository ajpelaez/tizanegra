from django.shortcuts import render
from teaching.models import University


def index(request):
    context = {
        "universidades": University.objects.all(),
    }

    return render(request, 'tizanegra/index.html', context)
