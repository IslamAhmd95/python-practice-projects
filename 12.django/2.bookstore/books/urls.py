from django.urls import path

from . import views


urlpatterns = [
    path('', views.BookListView.as_view(), name='books_list'),
    path('create/', views.create, name='books_create'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('author/<str:name>/', views.BookListView.as_view(), name='author_books'),
    path('<int:book_id>/reviews/create/', views.create_review, name='review_create'),
]