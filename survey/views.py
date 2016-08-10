from django.shortcuts import render
from django.http import HttpResponse

from .models import (
    Question, Choice)

from .forms import (
    SurveyForm)


def index(request):
    return HttpResponse("Hello, world. Index Page")


def get_questions(provider_name, survey_name):
    # We will use provider_name and survey_name in the future

    questions = Question.objects.all().order_by('?')
    sequence_num = 1
    for q in questions:
        q.sequence_num = sequence_num
        q.its_own_choices = Choice.objects.filter(
            question_id=q.id).order_by('?')
        sequence_num += 1
    return questions


def one_survey(request, provider_name, survey_name):
    print(provider_name)
    print(survey_name)

    questions = get_questions(provider_name, survey_name)
    return render(request, 'survey/survey_display.html',
                  {'questions': questions})


def store_in_db():
    pass


def display_using_render():
    result = "raw score is XX out of total" +\
             "percentage is: "
    return HttpResponse(result)


def survey_processing(request, provider_name, survey_name):
    if request.method == "GET":
        form = SurveyForm()
        questions = get_questions(provider_name, survey_name)
        return render(request, 'survey/survey_display.html',
                      {'questions': questions,
                       'form': form})

    elif request.method == "POST":
        form = SurveyForm(request.POST)
        all_choice_ids = ""
        for key, value in form.data.items():
            if key.startswith('__question_num'):
                all_choice_ids += ' ' + value
                store_in_db()
                display_using_render()
        print(all_choice_ids)
    else:
        pass
