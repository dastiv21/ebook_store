# tests.py
# tests.py
import os
from decimal import Decimal

import django
from django.contrib.auth.models import User
from django.db import IntegrityError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ebook_store.settings")
django.setup()


# tests.py

import pytest
from django.contrib.auth.models import User
from .models import Tag, Book, Transaction
from django.core.exceptions import ValidationError


# Fixtures
@pytest.fixture
def tag(db):
    return Tag.objects.create(name="Fiction")


@pytest.fixture
def book(db, tag):
    book = Book.objects.create(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        description="A classic novel about the Jazz Age.",
        price=19.99,
        stock=10,
    )
    book.tags.add(tag)
    return book


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password")


@pytest.fixture
def transaction(db, user, book):
    return Transaction.objects.create(
        user=user,
        book=book,
        quantity=2,
        total_price=39.98,
        status="Completed",
    )


# Test cases
@pytest.mark.django_db
def test_create_tag(tag):
    assert tag.pk is not None
    assert tag.slug == "fiction"
    assert Tag.objects.filter(slug="fiction").exists()


@pytest.mark.django_db
def test_create_book(book, tag):
    assert book.pk is not None
    assert book.title == "The Great Gatsby"
    assert book.author == "F. Scott Fitzgerald"
    assert book.description == "A classic novel about the Jazz Age."
    assert book.price == 19.99
    assert book.stock == 10
    assert book.tags.filter(name="Fiction").exists()


@pytest.mark.django_db
def test_create_transaction(transaction, user, book):
    assert transaction.pk is not None
    assert transaction.user == user
    assert transaction.book == book
    assert transaction.quantity == 2
    assert transaction.total_price == 39.98
    assert transaction.status == "Completed"
    assert Transaction.objects.filter(status="Completed").exists()


@pytest.mark.django_db
def test_update_book_price(book):
    book.price = 24.99
    book.save()
    updated_book = Book.objects.get(pk=book.pk)
    assert updated_book.price == round(Decimal(24.99), 2)


@pytest.mark.django_db
def test_delete_book(book):
    book_id = book.pk
    book.delete()
    with pytest.raises(Book.DoesNotExist):
        Book.objects.get(pk=book_id)
    assert not Book.objects.filter(pk=book_id).exists()


@pytest.mark.django_db
def test_verify_related_name(tag, book):
    assert book in tag.articles.all()


@pytest.mark.django_db
def test_delete_transaction(transaction):
    transaction_id = transaction.pk
    transaction.delete()
    with pytest.raises(Transaction.DoesNotExist):
        Transaction.objects.get(pk=transaction_id)


@pytest.mark.django_db
def test_transaction_quantity_exceeds_stock(book):
    with pytest.raises(ValidationError):
        Transaction.objects.create(
            user=User.objects.create_user(username="testuser", password="password"),
            book=book,
            quantity=book.stock + 1,
            total_price=book.price * (book.stock + 1),
            status="Completed",
        )


@pytest.mark.django_db
def test_update_book_tags(book, tag):
    new_tag = Tag.objects.create(name="Classic")
    book.tags.set([new_tag])
    assert book.tags.count() == 1
    assert book.tags.filter(name="Classic").exists()
    assert not book.tags.filter(name="Fiction").exists()


@pytest.mark.django_db
def test_unique_slug(tag):
    with pytest.raises(IntegrityError):
        Tag.objects.create(name="fiction")


@pytest.mark.django_db
def test_full_workflow():
    tag = Tag.objects.create(name="Fiction")
    book = Book.objects.create(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        description="A classic novel about the Jazz Age.",
        price=19.99,
        stock=10,
    )
    book.tags.add(tag)
    user = User.objects.create_user(username="testuser", password="password")
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