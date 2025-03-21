from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone


'''
def index(request):
    latest_question_list = Question.objects.order_by('pub_date')[:5] old date first
    latest_question_list = Question.objects.order_by('-pub_date')[5] error
    latest_question_list = Question.objects.order_by('-pub_date')[5:] 5th index
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list' : latest_question_list}
    return HttpResponse(template.render(context, request))

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list' : latest_question_list}
    return render(request, 'polls/index.html', context) 
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
'''


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    #return the last 5 published questions (not include those set to be published in the future)
    def get_queryset(self):
        #lte = less than or equal to
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]


'''
def detail(request, question_id):
    return HttpResponse('You are looking at %s' %  question_id)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        #without raise Http404 will occur UnboundLocalError at /polls/111/
        raise Http404('Question HaGa does not exist !')
    return render(request, 'polls/detail.html', {'question' : question})

def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    #'question' is for detail.html {{ question }}
    return render(request, 'polls/detail.html', {'question' : question})
'''
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        #exclude any questions that are not published yet
        return Question.objects.filter(pub_date__lte = timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Question.DoesNotExist): #KeyError = pk
        return render(
            request,
            'polls/detail.html',
            {
                "question" : question,
                'error_message' : 'You did not select any choice !'
            }
        )
    else:
        selected_choice.votes = F('votes') + 1 
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args = (question.id, )))


'''
def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id);
    return render(request, 'polls/results.html', {'question' : question})
'''
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
