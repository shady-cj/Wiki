from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>",views.TITLE, name="TITLE"),
    path("NewPage", views.NewPage, name="NewPage"),
    path("EditPage/<str:name>",views.EditPage, name="EditPage"),
    path("Random", views.Random, name="Random"),
    path("search",views.search,name="search")
]