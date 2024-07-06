from django.urls import path
from .views.list_articles_view import ListArticlesView
from .views.list_categories import ListCategoriesView

urlpatterns = [
    path("categories/<category_name>/", ListArticlesView.as_view()),
    path("categories/", ListCategoriesView.as_view()),
]
