from django.shortcuts import render
from django.http import HttpResponse

from .models import (
    Question, Choice)


def index(request):
    return HttpResponse("Hello, world. Index Page")


def one_survey(request, provider_name, survey_name):
    print(provider_name)
    print(survey_name)

    questions = Question.objects.all().order_by('?')[:20]

    for q in questions:
        q.its_own_choices = Choice.objects.filter(
            question_id=q.id).order_by('?')

    return render(request, 'survey/survey_display.html',
                  {'questions': questions})

