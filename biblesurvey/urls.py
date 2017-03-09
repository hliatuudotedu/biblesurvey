"""eyeballsurvey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from survey.views import main_function, survey_processing, import_questions_choices, import_bible_verses

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', main_function, name="main"),
    url(r'^import_question_choices/$', import_questions_choices, name="import"),
    url(r'^import_bible_verses', import_bible_verses, name="import_bible_verses"),

    # ex: /provider/mingwang/survey1/
    url(r'^provider/(?P<provider_name>[a-zA-Z]+[a-zA-Z0-9]*)/' +\
        '(?P<survey_name>[a-zA-Z]+[a-zA-Z0-9]*)/$',
        survey_processing, name='survey_processing')
]
