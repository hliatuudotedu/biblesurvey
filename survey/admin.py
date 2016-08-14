from django.contrib import admin

from .models import (
    Provider,
    Survey,
    Category,
    Question,
    Choice,
    SurveyQuestion)

admin.site.register(Provider)
admin.site.register(Survey)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(SurveyQuestion)
