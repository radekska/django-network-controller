from django.shortcuts import render


# Create your views here.
def homepage_view(request, *args, **kwargs):
    context = {

    }
    return render(request, "home.html", context)


def contactpage_view(request, *args, **kwargs):
    context = {

    }
    return render(request, "contact.html", context)
