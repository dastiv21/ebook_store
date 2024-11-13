from django.contrib import admin

from store.models import Book, Transaction

# Register your models here.
admin.site.register(Book)
admin.site.register(Transaction)