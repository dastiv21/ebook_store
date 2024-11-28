# tests.py
# tests.py
import os
from decimal import Decimal

import django
from django.contrib.auth.models import User
from django.db import IntegrityError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ebook_store.settings")
django.setup()

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Tag, Book, Transaction

import pytest
from django.db import connections


@pytest.fixture(scope='session')
def db_connection():
    connection = connections['default']
    yield connection
    connection.close()


@pytest.fixture(scope='session', autouse=True)
def db_cleanup(db_connection):
    yield
    Book.objects.all().delete()
    Transaction.objects.all().delete()
