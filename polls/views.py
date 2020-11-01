"""Create view."""
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
        selected_choice.votes += 1
        selected_choice.save()
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
    if question.can_vote():
        return render(request, 'polls/detail.html', {
            'question': question,
        })
    else:
        messages.error(request, "You can't vote")
        return redirect('polls:index')


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
