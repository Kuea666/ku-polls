"""Create view KU Polls."""
from django.shortcuts import redirect


def index(request):
    """Landing page for KU Polls.
    Return:
        redirect to index page.
    """
    return redirect("polls:index")
