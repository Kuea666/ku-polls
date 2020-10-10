from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.utils import timezone
from django.contrib import messages



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
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

def detail(request,pk):
    question = get_object_or_404(Question, pk=pk)
    if question.can_vote():
        return render(request,'polls/detail.html',{
            'question': question,
        })
    else:
        messages.error(request, "You can't vote")
        return redirect('polls:index')                      

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.order_by('-pub_date')

