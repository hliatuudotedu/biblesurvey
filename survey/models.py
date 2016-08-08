from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=400)
    purpose = models.CharField(max_length=400)
    owner = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE)
    question_text = models.CharField(max_length=400)
    pub_date = models.DateTimeField(
        verbose_name='date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=400)
    point_value = models.DecimalField(
        verbose_name='point value',
        max_digits=4,
        decimal_places=2)

    def __str__(self):
        return self.choice_text



