from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='books_list'),
    path('create/', views.create, name='books_create'),
    path('<int:pk>/', views.show, name='book_detail'),
    path('<int:book_id>/reviews/create/', views.create_review, name='review_create'),
]