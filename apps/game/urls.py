from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path("", views.board_view, name="game_page"),
]
