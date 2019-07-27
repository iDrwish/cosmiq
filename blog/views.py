from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.
class PostList(ListView):
    model = Post
    queryset = Post.published.all()
    template_name = 'blog/Post/post_list.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/Post/post_detail.html'
