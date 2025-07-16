from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path("", views.game_index_view, name="index_page"),
    path("<str:room>", views.board_view, name="game_page"),
]
