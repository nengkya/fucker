from django.http import HttpResponse
from .models import Question


def index(request):
    #latest_question_list = Question.objects.order_by('pub_date')[:5] old date first
    #latest_question_list = Question.objects.order_by('-pub_date')[5] error
    #latest_question_list = Question.objects.order_by('-pub_date')[5:] 5th index
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)


def detail(request, question_id):
    return HttpResponse('You are looking at %s', question_id)
