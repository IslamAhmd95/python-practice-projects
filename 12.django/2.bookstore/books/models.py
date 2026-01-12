from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=256)
    page_count = models.IntegerField()
    thumbnail_url = models.CharField(max_length=256)
    short_description = models.TextField()
    long_description = models.TextField()
    authors = models.ManyToManyField("Author")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books'


class Review(models.Model):
    body = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name= 'reviews')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'
    

class Author(models.Model):
    name = models.CharField(max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'authors'
