from django.shortcuts import render
from django.http import HttpResponse

from .models import (
    Question, Choice)

from .forms import (
    SurveyForm)


def index(request):
    return HttpResponse("Hello, world. Index Page")


def main_function(request):
    return render(request, 'survey/main.html',
                  {})


def get_questions(provider_name, survey_name):
    # TODO: will use provider_name and survey_name soon.
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


def store_in_db(choice_ids_list):
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
                       'form': form,
                       'provider_name': provider_name,
                       'survey_name': survey_name})

    elif request.method == "POST":
        form = SurveyForm(request.POST)
        choice_ids_list = list()

        patient_name = request.POST['patient_name']

        for key, value in form.data.items():
            if key.startswith('__QuestionNum__'):
                choice_ids_list.append(int(value))

        object_list = Choice.objects.filter(
            id__in=choice_ids_list)
        store_in_db(choice_ids_list)

        my_own_points = 0.00
        for obj in object_list:
            my_own_points += float(obj.point_value)
            a_question_id = obj.question_id
            obj.the_question_text = Question.objects.get(
                id=a_question_id).question_text
        return render(request, 'survey/survey_2_provider.html',
                      {'object_list': object_list,
                       'patient_name': patient_name,
                       'my_own_points': my_own_points})
    else:
        pass
