from django.shortcuts import render


def home_view(request):
    return render(request, "pages/home.html")


def sobre_view(request):
    return render(request, "pages/sobre.html")


def diferenciais_view(request):
    return render(request, "pages/diferenciais.html")
