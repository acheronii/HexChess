from django.http import HttpResponse
from django.template import loader


# Create your views here.
def home_page_view(request):
    template = loader.get_template("home/home.html")
    context = {}
    return HttpResponse(template.render(context, request))
