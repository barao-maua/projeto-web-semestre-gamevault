from django.urls import path

from .views import (
    diferenciais_view,
    home_view,
    sobre_view,
    login_view,
    logout_view,
    register_view,
    profile_view,
    library_view,
    add_to_library_view,
    update_library_entry_view,
    remove_from_library_view,
    game_catalog_view,
    game_detail_view,
    add_review_view,
)

app_name = "core"

urlpatterns = [
    path("", home_view, name="home"),
    path("sobre/", sobre_view, name="sobre"),
    path("diferenciais/", diferenciais_view, name="diferenciais"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    path("library/", library_view, name="library"),
    path("add-to-library/", add_to_library_view, name="add_to_library"),
    path(
        "update-library-entry/", update_library_entry_view, name="update_library_entry"
    ),
    path("remove-from-library/", remove_from_library_view, name="remove_from_library"),
    path("catalog/", game_catalog_view, name="game_catalog"),
    path("game/<int:game_id>/", game_detail_view, name="game_detail"),
    path("game/<int:game_id>/review/", add_review_view, name="add_review"),
]
