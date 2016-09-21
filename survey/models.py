from django.db import models
import uuid

class Provider(models.Model):
    name = models.CharField(max_length=400,
                            blank=False,
                            null=False)
    full_name = models.CharField(max_length=400)
    organization = models.CharField(max_length=400)
    datetime_joined = models.DateTimeField(
        null=True, blank=True)

    def __str__(self):
        return self.name


class Survey(models.Model):
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=400,
                            blank=False,
                            null=False)
    purpose = models.CharField(max_length=400)
    datetime_created = models.DateTimeField(
        null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=400,
                            blank=False,
                            null=False)
    purpose = models.CharField(max_length=400)
    owner = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE)
    question_text = models.CharField(max_length=400,
                                     null=False,
                                     blank=False)
    pub_date = models.DateTimeField(
        verbose_name='date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=400,
                                   null=False,
                                   blank=False)
    point_value = models.DecimalField(
        verbose_name='point value',
        max_digits=4,
        decimal_places=2)

    def __str__(self):
        return self.choice_text


class SurveyQuestion (models.Model):

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'SurveyQuestion: survey_id: [' +\
            str(self.survey_id) + ']' +\
            'question_id: [' +\
            str(self.question_id) + ']'


class SurveyResult (models.Model):

    patient_name = models.CharField(max_length=100)
    datetime_created = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    choice_ids = models.CharField(max_length=400)

    def __str__(self):
        return 'SurveyResult: uuid: [' +\
            str(self.uuid) + ']'
