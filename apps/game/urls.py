from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path("", views.board_view, name="game_page"),
    path("reset/", views.reset_board, name="reset"),
    path("flip/", views.flip_board, name="flip"),
    path("ajax/move/", views.ajax_move_view, name="ajax_move"),
]
