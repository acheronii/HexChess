from .forms import LowercaseUserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse

# Create your views here.


def signup_view(request):
    if request.method == "POST":
        form = LowercaseUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # save user
            return redirect("login")  # go to login page
    else:
        form = LowercaseUserCreationForm()
    template = loader.get_template("registration/signup.html")
    return HttpResponse(template.render({"form": form}, request))


def logged_out_view(request):
    template = loader.get_template("registration/signout.html")
    return HttpResponse(template.render({}, request))


@login_required
def profile_view(request):
    template = loader.get_template("registration/profile.html")
    return HttpResponse(template.render({"user": request.user}, request))
