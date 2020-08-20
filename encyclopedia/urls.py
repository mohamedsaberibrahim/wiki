from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("searchresults", views.search, name="search"),
    path("add", views.add, name="add"),
    path("random", views.randomPage, name="random"),
    path("<str:title>/edit", views.editPage, name="edit"),
    path("<str:title>", views.entryPage, name="entry"),
]
