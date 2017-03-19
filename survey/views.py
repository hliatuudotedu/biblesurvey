from django.shortcuts import render
from django.http import HttpResponse
import re

from .models import (
    Question,
    Choice,
    SurveyQuestion,
    SurveyResult,
    Survey,
    Provider)

from .forms import (
    SurveyForm,
    ImportQuestionsChoicesForm,
    ImportBibleVersesForm)

from django.utils import timezone

from django.db.models import (
    Max,
    Min,
    Avg)


def index(request):
    return HttpResponse("Hello, world. Index Page")


def main_function(request):
    return render(request, 'survey/main.html')


def import_questions_choices(request):
    if request.method == "GET":
        form = ImportQuestionsChoicesForm()
        return render(request, 'survey/import_questions_choices.html',
                      {'form': form})

    elif request.method == "POST":
        form = ImportQuestionsChoicesForm(request.POST)
        if form.is_valid():

            # delete all Questions and Choices
            Question.objects.all().delete()
            Choice.objects.all().delete()

            result = form.cleaned_data["all_info"]
            lines = result.splitlines()
            print(len(lines))
            for one_line in lines:
                if one_line.strip() == "":
                    lines.remove(one_line)

            print(len(lines))

            error_flag = False
            error_message = ""

            counter1 = 0
            a_question = None
            specified_category_id = 1
            for line1 in lines:
                print(line1)
                if line1.startswith("Question"):
                    # Remove the first word at the beginning
                    no_1st_word = line1.split(None, 1)[1]

                    a_question = Question(
                        question_text=no_1st_word,
                        pub_date=timezone.now(),
                        category_id=specified_category_id)
                    a_question.save()

                elif line1.startswith("Choice"):
                    # it must be a choice. Need to
                    # attach the choice to the previous
                    # question

                    no_1st_word = line1.split(None, 1)[1]

                    value_part_only = no_1st_word.split(None, 1)[0]

                    pure_text_only = no_1st_word.split(None, 1)[1]

                    value = float(value_part_only)
                    a_choice = Choice(
                        choice_text=pure_text_only,
                        point_value=value,
                        question_id=a_question.id)
                    a_choice.save()
                elif line1.strip() == "":
                    pass
                else:
                    error_flag = True
                    error_message = \
                        "Unrecognized line[#" + \
                        str(int(counter1) + 1) + "]:" + \
                        line1 + "***"

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


def get_questions(survey_name):
    sid = Survey.objects.get(name=survey_name)
    query_results = SurveyQuestion.objects.filter(
        survey_id=sid)

    question_ids = list()
    for result in query_results:
        question_ids.append(result.question_id)

    questions = Question.objects.filter(
        id__in=question_ids).order_by('?')

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

    questions = get_questions(survey_name)
    return render(request, 'survey/survey_display.html',
                  {'questions': questions})


def store_in_db(patient_name, choice_ids_list):
    a_survey = SurveyResult(
        patient_name=patient_name,
        choice_ids=choice_ids_list)
    a_survey.save()
    print(a_survey)


def display_using_render():
    result = "raw score is XX out of total" +\
             "percentage is: "
    return HttpResponse(result)


def survey_processing(request, provider_name, survey_name):
    if request.method == "GET":

        a_provider = Provider.objects.filter(name=provider_name)
        if a_provider.count() == 0:
            return HttpResponse(
                "Provider name " +
                provider_name + " is not found!")

        a_survey = Survey.objects.filter(name=survey_name)
        if a_survey.count() == 0:
            return HttpResponse(
                "Survey name " +
                survey_name + " not found!")

        form = SurveyForm()
        questions = get_questions(survey_name)
        return render(request, 'survey/survey_display.html',
                      {'questions': questions,
                       'form': form,
                       'provider_name': provider_name,
                       'survey_name': survey_name})

    elif request.method == "POST":
        form = SurveyForm(request.POST)
        choice_ids_list = list()
        question_ids_list = list()

        patient_name = request.POST['patient_name']

        for key, value in form.data.items():
            if key.startswith('__QuestionNum__'):
                choice_ids_list.append(int(value))

        object_list = Choice.objects.filter(
            id__in=choice_ids_list)

        store_in_db(patient_name, choice_ids_list)

        my_own_points = 0.00
        for obj in object_list:
            my_own_points += float(obj.point_value)
            a_question_id = obj.question_id
            question_ids_list.append(a_question_id)
            obj.the_question_text = Question.objects.get(
                id=a_question_id).question_text
        #  Need to get rid of duplicates
        #  within question_ids_list
        no_duplicates = list(set(question_ids_list))

        all_max = 0.00
        all_min = 0.00

        for q_id in no_duplicates:
            single_max = Choice.objects.filter(
            question_id=q_id).aggregate(Max('point_value'))
            all_max += float(single_max.get('point_value__max'))

            single_min = Choice.objects.filter(
            question_id=q_id).aggregate(Min('point_value'))
            all_min += float(single_min.get('point_value__min'))

        return render(request, 'survey/survey_2_provider.html',
                      {'object_list': object_list,
                       'patient_name': patient_name,
                       'my_own_points': my_own_points,
                       'all_max':all_max,
                       'all_min':all_min})


def import_bible_verses(request):
        if request.method == "GET":
            form = ImportBibleVersesForm()
            return render(request, 'survey/import_bible_verses.html', {'form': form})

        elif request.method == "POST":
            form = ImportBibleVersesForm(request.POST)
            if form.is_valid():

                result = form.cleaned_data["all_verses"]

                error_flag = False
                error_message = "Nothing wrong!"

                # split the result on periods
                sentences = result.split('.')

                # result for new string
                new_result = ""

                # strip leading and trailing white spaces and replace first
                # instance of valid number with ____
                # skip last split item, which is just a white space
                for i in range(0, len(sentences) - 1):
                    test = re.sub(' ([1-9])([0-9]*)(,[0-9]+)*', " ______", sentences[i], 1)
                    if (sentences[i] != test):
                        new_result = "%s%s%s%s" % (new_result, test.strip('\n').strip(), ".", re.search(' ([1-9])([0-9]*)(,[0-9]+)*', sentences[i]), "\n\n")

                if error_flag:
                    result = error_message
                else:
                    result = new_result

                return HttpResponse(result, content_type='text/plain')
            else:
                pass
        else:
            pass
