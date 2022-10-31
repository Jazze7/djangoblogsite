from web import views
from django.urls import path, include


app_name = "web"


urlpatterns = [
    path('', views.index, name="index"),

]
