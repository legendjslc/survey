"""pollproject URL Configuration

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
from polls.views import *

admin.site.site_title = 'Survey Administration'
admin.site.index_title = 'Manage Your Surveys'
admin.site.site_header = 'Survey Administration'
admin.site.index_template = 'admin/custom-index.html'

visitors = Visitor.objects.all().order_by('-filled')

urlpatterns = [
    url(r'^admin/',
        admin.site.urls,
        {'extra_context': {'visitors': visitors}}),
    # url(r'^$', index, name="index"),
    url(r'^(?P<survey_id>[0-9]+)/survey/$', build_survey, name='build_survey'),
    url(r'^thankyou/', thankyou, name="thankyou"),
    url(r'^build/', build_fixture, name="build"),
    # url(r'^report/', report, name="report"),
    url(r'^details/', details, name="details"),

]
