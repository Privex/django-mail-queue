from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^clear$', views.clear_sent_messages, name='clear_sent_messages'),
    re_path(r'^$', views.run_mail_job, name='run_mail_job'),
]
