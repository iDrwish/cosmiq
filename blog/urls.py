from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    # path('search/<>')
    path('<slug:slug>', views.PostPage.as_view(), name='post_detail'),
    path(
        'tag/<slug:tag_slug>', views.PostList.as_view(),
        name='post_list_by_tag'),
]
