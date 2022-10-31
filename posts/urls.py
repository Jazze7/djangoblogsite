from posts import views
from django.urls import path


app_name = "posts"
urlpatterns = [
    path('create/', views.create_post, name="create_post"),
]
