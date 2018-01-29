from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    """
    Root page view. This is essentially a SPA, if you ignore the login and admin parts.
    :param request:
    :return: render that in the index template
    """
    return render(request, "index.html")

