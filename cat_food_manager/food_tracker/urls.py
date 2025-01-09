from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='index'),  # Главная страница
    path('add/', views.add_food, name='add_food'),  # Без параметра
    path('feed/', views.feed_cat, name='feed_cat'),  # Без параметра
]