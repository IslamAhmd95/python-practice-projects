import os
import json

from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from pathlib import Path
from django.contrib import messages

from books.models import Book, Review


books_file_path = os.path.join(Path(__file__).resolve().parent.parent, 'books.json')
with open(books_file_path, 'r', encoding='utf-8') as f:
    books = json.load(f)


# Create your views here.
def index(request):
    books = Book.objects.all()
    return render(request, 'books/index.html', {'books': books})


def show(request, pk):
    # book = next((book for book in books if str(book['id']) == str(id)), None)

    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/show.html', {'book': book})


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