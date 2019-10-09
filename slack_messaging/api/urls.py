from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('update_message', views.UpdateMessage.as_view(), name='slack_update_message'),
]
