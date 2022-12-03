from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from main.functions import paginate_instances
from django.contrib.postgres.search import SearchVector

from posts.models import Post, Category, Author
# Create your views here.


def index(request):
    posts = Post.objects.filter(is_deleted=False, is_draft=False)
    search_author = request.GET.getlist("author")
    if search_author:
        posts = Post.objects.filter(author__in=search_author)

    search_categories = request.GET.getlist("category")
    if search_categories:
        posts = Post.objects.filter(
            categories__in=search_categories).distinct()
    categories = Category.objects.all()[:5]
    authors = Author.objects.all()

    q = request.GET.get('q')
    if q:
        posts=posts.annotate(search=SearchVector("title","author__name","categories__title").filter(search=q))
        posts = posts.filter(title__search=q)

    search_author = request.GET.getlist("author")
    if search_author:
        posts = Post.objects.filter(author__in=search_author)

    search_categories = request.GET.getlist("category")
    if search_categories:
        posts = Post.objects.filter(
            categories__in=search_categories).distinct()

    sort = request.GET.get("sort")
    if sort:
        if sort == "title-asc":
            posts = posts.order_by("title")
        elif sort == "title-desc":
            posts = posts.order_by("-title")
        elif sort == "date-asc":
            posts = posts.order_by("published_date")
        elif sort == "date-desc":
            posts = posts.order_by("-published_date")

    instances = paginate_instances(request, posts)

    context = {
        "title": "HOME",
        'instances': instances,
        "categories": categories,
        "authors": authors,
    }
    return render(request, 'web/home.html', context=context)


def post(request, id):
    instances = get_object_or_404(Post.objects.filter(id=id))
    context = {
        "instances": instances
    }
    return render(request, 'web/post.html', context=context)
