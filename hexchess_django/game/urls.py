from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path('', views.board_view, name='game_page'),
    path('click/', views.on_click, name='click'),
]