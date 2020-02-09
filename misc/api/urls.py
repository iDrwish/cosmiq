from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('slack/update_message', views.UpdateMessage.as_view(),
         name='slack_update_message'),
    path('halan', views.getOS, name='get_os'),
    path('getparameters', views.adjustParameters, name='adjust_parameters'),
    path('forwardparameters', views.adjustForwardParameters, name='adjust_forward')
]
