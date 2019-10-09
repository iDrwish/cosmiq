from django.contrib import admin
from .models import Post, Comment
from markdownx.admin import AdminMarkdownxWidget

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fields = [
        'title', 'slug', 'author', 'body',
        'publish', 'status', 'tags'
        ]
    list_display = fields[:-1] + ['tag_list']
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('status', 'created', 'publish', 'author', 'tags')
    date_hierarchy = ('created')
    raw_id_fields = ('author', )
    search_fields = ('title', 'body')
    formfield_overrides = {'body': {'widget': AdminMarkdownxWidget}}

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        if obj.tags.all():
            return u", ".join(o.name for o in obj.tags.all())
        return None


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'comment', 'creation_date', 'last_edited', 'active']
    list_filter = ['name', 'email', 'active']
    date_hierarchy = ('creation_date')
    search_fields = ['name', 'email', 'comment']

# new staging test
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
