from . import views

from django.urls import path

app_name = "accounts"
urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("profile/", views.profile_view, name="profile"),
    path("signout/", views.logged_out_view, name="signout"),
]
