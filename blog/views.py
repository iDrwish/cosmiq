from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from .models import Post


# Create your views here.
class PostList(ListView):
    model = Post
    # queryset = Post.published.all()
    context_object_name = 'blog_posts'
    template_name = 'blog/Post/post_list.html'

    def get_queryset(self):
        if self.kwargs.get('tag_slug', None):
            self.tags = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            return Post.published.filter(tags__in=[self.tags])
        return Post.published.all()


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/Post/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        # TODO: Add Similar Posts via tags
        # Add Comments
        return context
