from django.contrib import admin
from posts.models import Author, Category, Post


# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')


admin.site.register(Author, AuthorAdmin)

admin.site.register(Category)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'published_date')


admin.site.register(Post, PostAdmin)
