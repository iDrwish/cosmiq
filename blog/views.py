from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.shortcuts import redirect
from taggit.models import Tag
from django.urls import reverse_lazy, reverse
from .models import Post, Comment
from .forms import CommentForm


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
    object = 'post'
    template_name = 'blog/Post/post_detail.html'

    def get(self, request, *args, **kwargs):
        """
        Rewrite of the get function to add the similar posts
        to the render function.

        Similar functions by Tag and ordered by Count and Date
        """
        self.object = self.get_object()
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
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm(initial={'post': self.object})
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
        """
        Get the context for this view.
        """
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




# class StudentEnrollCourseView(, FormView):
#     course = None
#     form_class = CourseEnrollForm

#     def form_valid(self, form):
#         self.course = form.cleaned_data['course']
#         self.course.students.add(self.request.user)
#         return super(StudentEnrollCourseView, self).form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy('post_detail', args=[self.course.id])
