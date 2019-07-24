from django.contrib import admin
from .models import Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    fields = (
        'title', 'slug', 'author', 'body',
        'publish', 'status', 'readtime'
        )
    list_display = fields
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('status', 'created', 'publish', 'author')
    date_hierarchy = ('created')
    raw_id_fields = ('author', )
    search_fields = ('title', 'body')


admin.site.register(Post, PostAdmin)
