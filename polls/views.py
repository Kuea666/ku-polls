"""Create view."""
import logging
import logging.config

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from polls.models import Vote
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from mysite.settings import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("polls")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def logged_in_logging(sender, request, user, **kwargs):
    logger.info(f"{user.username} {get_client_ip(request)} has logged in")

@receiver(user_logged_out)
def logged_out_logging(sender, request, user, **kwargs):
    logger.info(f"{user.username} {get_client_ip(request)} has logged out")

@receiver(user_login_failed)
def logged_in_failed_logging(sender, request, credentials, **kwargs):
    logger.warning(f"{request.POST['username']} {get_client_ip(request)} login failed")


class ResultsView(generic.DetailView):
    """Result view for polls."""

    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """Vote the selected choice.
    Arguments:
        question_id - is id of the question.
    Return:
        Redirect to results page.
        Render the detail page.
    """
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if(Vote.objects.filter(question=question,user=request.user).exists()):
            Vote.objects.update(question=question, choice=selected_choice, user=request.user)
        else:
            Vote.objects.create(question=question, choice=selected_choice, user=request.user)
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def detail(request, pk):
    """detail page.
    Arguments:
        pk - primary key (id) of the question.
    Return:
        Render HTML detail page.
    """
    question = get_object_or_404(Question, pk=pk)
    if not question.can_vote():
        return redirect("polls:index")
    else:
        try:
            previous_vote = Vote.objects.filter(question=question,user=request.user).first().choice
            return render(request, 'polls/detail.html', {'question': question, 'previous_vote': previous_vote})
        except:
            return render(request, 'polls/detail.html',{'question':question,})
        

class IndexView(generic.ListView):
    """IndexView page."""    

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        
        return Question.objects.order_by('-pub_date')
