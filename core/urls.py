from django.urls import path

from .views import diferenciais_view, home_view, sobre_view


app_name = "core"

urlpatterns = [
    path("", home_view, name="home"),
    path("sobre/", sobre_view, name="sobre"),
    path("diferenciais/", diferenciais_view, name="diferenciais"),
]
