from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.shortcuts import redirect
from django.core.cache import cache
from taggit.models import Tag
from django.urls import reverse_lazy, reverse
from .models import Post, Comment
from .forms import CommentForm, PostQueryForm


# Create your views here.
class PostList(ListView):
    model = Post
    context_object_name = 'blog_posts'
    form_class = PostQueryForm
    success_url = 'blog/Post/post_list.html'
    template_name = 'blog/Post/post_list.html'
    query = None # I overwrite it in get_queryset

    def get_queryset(self):
        if self.kwargs.get('tag_slug', None):
            self.tags = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            return Post.published.filter(tags__in=[self.tags])
        form = self.form_class(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            self.query = query
            # Try Postgres SearchVector over Body and Title
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = (Post.published.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query))
                .filter(search=search_query).order_by('-rank'))
            if results:
                return results
                # Fallback to TrigramSimilarity if there was no results
            return (Post.published.annotate(
                similarity=TrigramSimilarity('title', query)
                )#.filter(similarity__gt=0.01)
                .order_by('-similarity'))
        return Post.published.all()
    
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['query'] = self.query
        context['query_form'] = self.form_class(initial={'query': self.query})
        return context

class PostDetail(DetailView):
    model = Post
    object = 'post'
    template_name = 'blog/Post/post_detail.html'
    form_class = PostQueryForm

    def get(self, request, *args, **kwargs):
        """
        Rewrite of the get function to add the similar posts
        to the render function.
        Similar functions by Tag and ordered by Count and Date
        """
        # Check to see if the search query is being called
        form = self.form_class(self.request.GET)
        if form.is_valid():
            form_sub = '&'.join(map(lambda x: '='.join(x), self.request.GET.items()))
            redirect_url = reverse('post_list') + '?' + form_sub
            return redirect(redirect_url)
        self.object = self.get_object()
        # Get the views and increment, if not available create it
        post_cache_key = 'blog-post-{}'.format(self.object.id)
        post_views_count = cache.get(post_cache_key)
        if post_views_count:
            cache.incr(post_cache_key, 1)
        else:
            post_views_count = 1
            cache.add(post_cache_key, post_views_count)
        # get post tags
        post_tags = self.object.tags.values_list('id', flat=True)
        # get similar posts by tag
        similar_posts = (Post.published.filter(tags__in=post_tags)
            .exclude(id=self.object.id))
        similar_posts = (similar_posts.annotate(same_tags=Count('tags'))
            .order_by('-same_tags', '-publish'))[:4]
        post_comments = Comment.objects.filter(post=self.object)
        context = self.get_context_data(object=self.object)
        context['post_comments'] = post_comments
        context['similar_posts'] = similar_posts
        context['post_views_count'] = post_views_count
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm(initial={'post': self.object})
        context['query_form'] = PostQueryForm()
        context['query_url'] = reverse('post_list')
        return context


class CommentFormView(SingleObjectMixin, FormView):
    form_class = CommentForm
    model = Post
    template_name = 'blog/Post/post_detail.html'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.post = self.object
        form.save()
        return super(CommentFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['comment_form'] = kwargs.pop('form')
        return super(CommentFormView, self).get_context_data(**kwargs)


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        return super().post(request, *args, **kwargs)


class PostPage(View):
    def get(self, request, *args, **kwargs):
        view = PostDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentFormView.as_view()
        return view(request, *args, **kwargs)


def adjust_testing_view(request):
    return render(request, 'blog/Post/adjust_testing.html')