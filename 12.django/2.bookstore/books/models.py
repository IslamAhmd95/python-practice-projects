from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=256)
    page_count = models.IntegerField()
    thumbnail_url = models.CharField(max_length=256)
    short_description = models.CharField(max_length=256)
    long_description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books'


class Review(models.Model):
    body = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name= 'reviews')
    created_at = models.DateTimeField(auto_now=True)
    