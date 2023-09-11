from django.contrib import admin
from .models import Article

# Register the Article model to make it available in the admin interface
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'url', 'image')  # Display these fields in the admin list view
    list_filter = ('author',)  # Add a filter for the 'author' field
    search_fields = ('title', 'author')  # Enable search by 'title' and 'author'
    ordering = ('-id',)  # Order articles by descending 'id' (or any other field)
