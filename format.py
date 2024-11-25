import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Tag, Book, Transaction


@pytest.mark.django_db
def test_book_list_view(db_connection):
    client = APIClient()
    response = client.get(reverse('book-list'))
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_book_create_view(db_connection):
    client = APIClient()
    response = client.post(reverse('book-list'),
                           {'title': 'Python for Beginners',
                            'author': 'John Doe',
                            'description': 'Learn Python from scratch.',
                            'price': 19.99,
                            'stock': 10})
    assert response.status_code == 201
    assert response.json() == {'id': 1,
                               'title': 'Python for Beginners',
                               'author': 'John Doe',
                               'description': 'Learn Python from scratch.',
                               'price': 19.99,
                               'stock': 10,
                               'created_at': response.json()['created_at'],
                               'tags': [],
                               'image': None}


@pytest.mark.django_db
def test_transaction_create_view(db_connection):
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='password')
    client.force_authenticate(user=user)
    book = Book.objects.create(title='Python for Beginners',
                               author='John Doe',
                               description='Learn Python from scratch.',
                               price=19.99,
                               stock=10)
    response = client.post(reverse('transaction-list'),
                           {'book_id': book.id, 'quantity': 2})
    assert response.status_code == 201
    assert response.json() == {'id': 1,
                               'user': 1,
                               'book': 1,
                               'quantity': 2,
                               'total_price': 39.98,
                               'transaction_date': response.json()['transaction_date'],
                               'status': 'Completed'}