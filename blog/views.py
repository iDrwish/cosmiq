from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Count
from taggit.models import Tag
from .models import Post


# Create your views here.
class PostList(ListView):
    model = Post
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

    def get(self, request, *args, **kwargs):
        """
        Rewrite of the get function to add the similar posts
        to the render function.

        Similar functions by Tag and ordered by Count and Date
        """
        self.object = self.get_object()
        post_tags = self.object.tags.values_list('id', flat=True)
        similar_posts = (
            Post.published
            .filter(tags__in=post_tags)
            .exclude(id=self.object.id))
        similar_posts = (
            similar_posts
            .annotate(same_tags=Count('tags'))
            .order_by('-same_tags', '-publish'))[:4]
        return self.render_to_response({
            'post': self.object,
            'similar_posts': similar_posts
        })
