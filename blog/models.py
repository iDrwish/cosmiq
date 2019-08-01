from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
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
    body = models.TextField()
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


class Comment(models.Model):
    """
    Comment Section
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    name = models.CharField(max_length=100)
    email = models.EmailField()
