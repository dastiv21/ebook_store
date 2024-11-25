# tests.py
# tests.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ebook_store.settings")
django.setup()


import pytest
from .models import Tag, Book, Transaction


@pytest.mark.django_db
def test_create_tag(db):
    tag = Tag.objects.create(name="Fiction")
    assert tag.pk is not None
    assert tag.slug == "fiction"
    assert Tag.objects.filter(slug="fiction").exists()


@pytest.mark.django_db
def test_create_book(db):
    tag = Tag.objects.create(name="Fiction")
    book = Book.objects.create(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        description="A classic novel about the Jazz Age.",
        price=19.99,
        stock=10,
    )
    book.tags.add(tag)
    assert book.pk is not None
    assert book.title == "The Great Gatsby"
    assert book.author == "F. Scott Fitzgerald"
    assert book.description == "A classic novel about the Jazz Age."
    assert book.price == 19.99
    assert book.stock == 10
    assert book.tags.filter(name="Fiction").exists()


@pytest.mark.django_db
def test_create_transaction(db):
    user = User.objects.create_user(username="testuser", password="password")
    book = Book.objects.create(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        description="A classic novel about the Jazz Age.",
        price=19.99,
        stock=10,
    )
    transaction = Transaction.objects.create(
        user=user,
        book=book,
        quantity=2,
        total_price=39.98,
        status="Completed",
    )
    assert transaction.pk is not None
    assert transaction.user == user
    assert transaction.book == book
    assert transaction.quantity == 2
    assert transaction.total_price == 39.98
    assert transaction.status == "Completed"
    assert Transaction.objects.filter(status="Completed").exists()