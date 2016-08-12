from django.shortcuts import render
from django.http import HttpResponse

from .models import (
    Question, Choice)

from .forms import (
    SurveyForm,
    ImportQuestionsChoicesForm)


def index(request):
    return HttpResponse("Hello, world. Index Page")


def main_function(request):
    return render(request, 'survey/main.html',
                  {})


def import_questions_choices(request):
    if request.method == "GET":
        form = ImportQuestionsChoicesForm()
        return render(request, 'survey/import_questions_choices.html',
                      {'form': form})

    elif request.method == "POST":
        form = ImportQuestionsChoicesForm(request.POST)
        if form.is_valid():
            result = form.cleaned_data["all_info"]
            lines = result.splitlines()
            print(len(lines))
            for one_line in lines:
                if one_line.strip() == "":
                    lines.remove(one_line)

            print(len(lines))

            error_flag = False
            error_message = "Nothing"

            counter1 = 0
            has_a_new_question = False
            a_question = None
            for line1 in lines:
                if line1.startswith("Q"):
                    has_a_new_question = True
                    # Remove the first word at the beginning

                    a_question = Question(
                        question_text=line1,
                        pub_date='2015-11-11',
                        category_id=1)
                    # it must be a question:
                    pass
                elif line1.startswith("C"):
                    # it must be a choice. Need to
                    # attach the choice to the previous
                    # question
                    choice_text = line1
                    value = float(line1)
                    a_choice = Choice(
                        choice_text=choice_text,
                        point_value=value,
                        question_id=a_question.id)
                    pass
                else:
                    error_flag = True
                    error_message = \
                        "Unrecognized line[#" + \
                        str(int(counter1) + 1) + "]: " + line1

                    break
                counter1 += 1

            if error_flag:
                result = error_message
            else:
                result = "Processed Successfully. Thank you."

            return HttpResponse(
                result, content_type='text/plain')
        else:
            pass
    else:
        pass


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
