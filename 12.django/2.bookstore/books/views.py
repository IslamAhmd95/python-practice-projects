import os
import json

from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from pathlib import Path
from django.contrib import messages
from django.views.generic import ListView, DetailView

from books.models import Book, Review



class BookListView(ListView):
    def get_queryset(self):
        return Book.objects.all()


class BookDetailView(DetailView):
    def get_queryset(self):
        return Book.objects.prefetch_related(
            Prefetch('reviews',
            queryset=Review.objects.order_by('-created_at'),
            to_attr='ordered_reviews')
        ).all()
        

def create(request):
    return HttpResponse('create view')


def create_review(request, book_id):
    body = request.POST.get('body')
    book = get_object_or_404(Book, pk=book_id)
    try:
        Review.objects.create(body=body, book=book)
        messages.success(request, "Review successfully added!")
    except Exception as e:
        messages.error(request, f"Error adding review: {e}")
    return redirect('book_detail', pk=book_id)