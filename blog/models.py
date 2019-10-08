from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.sites.models import Site
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
import readtime


class PublishManager(models.Manager):
    def get_queryset(self):
        return (
            super(PublishManager, self)
            .get_queryset()
            .filter(status='published')
            )


# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published')
    ]

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        allow_unicode=True,
        unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = MarkdownxField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft')
    readtime = models.IntegerField(editable=False)
    objects = models.Manager()
    published = PublishManager()
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.readtime = readtime.of_text(self.body).minutes
        super(Post, self).save(*args, **kwargs)  # Call the real save() method

    @property
    def formatted_markdown(self):
        return markdownify(self.body)


class Comment(models.Model):
    """
    Comment Section
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField(blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ('-creation_date',)

    def __str__(self):
        return 'Comment by {}: {}'.format(self.name, self.comment)


class Like(models.Model):
    user = models.ForeignKey(User, related_name='action', db_index=True,
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True)

# TODO Create the Author Model
# TODO Add Cookies to the website


# TODO Handle the same DB for different sites

# DONE
# TODO Add cahcing for web views counts
# TODO Add Cahching for web views
# TODO Add Text search
# TODO Migrate to Postgres
