from django.contrib import admin
from .models import Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    fields = (
        'title', 'slug', 'author', 'body',
        'publish', 'status', 'readtime', 'tag_list'
        )
    list_display = fields
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('status', 'created', 'publish', 'author', 'tags')
    date_hierarchy = ('created')
    raw_id_fields = ('author', )
    search_fields = ('title', 'body')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


admin.site.register(Post, PostAdmin)
