# python manage.py load_books

import json
import os
from django.core.management.base import BaseCommand
from django.db import models
from books.models import Book


class Command(BaseCommand):
    help = 'Load books data from books.json into the database'

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        json_file_path = os.path.join(base_dir, 'books.json')

        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(
                f'File {json_file_path} not found'))
            return

        with open(json_file_path, 'r', encoding='utf-8') as f:
            books_data = json.load(f)

        model_fields = {f.name for f in Book._meta.get_fields()
                        if not f.primary_key}
        field_types = {f.name: type(
            f) for f in Book._meta.get_fields() if not f.primary_key}

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for book_data in books_data:
            filtered_data = {}
            for field_name in model_fields:
                if field_name in book_data:
                    value = book_data[field_name]
                    if value is not None:
                        filtered_data[field_name] = value
                elif field_name in field_types:
                    field_type = field_types[field_name]
                    if issubclass(field_type, (models.CharField, models.TextField)):
                        filtered_data[field_name] = ''
                    elif issubclass(field_type, models.IntegerField):
                        filtered_data[field_name] = 0

            if not filtered_data:
                skipped_count += 1
                continue

            book_id = book_data.get('id')
            if book_id:
                book, created = Book.objects.update_or_create(
                    id=book_id,
                    defaults=filtered_data
                )
            else:
                book = Book.objects.create(**filtered_data)
                created = True

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded books: {created_count} created, {updated_count} updated, {skipped_count} skipped'
            )
        )
