from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Book, Transaction
from .pagination import BookPagination
from .serializers import BookSerializer, TransactionSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author']
    pagination_class = BookPagination


class TransactionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity')

        try:
            book = Book.objects.get(id=book_id)
            if book.stock < quantity:
                return Response({"error": "Not enough stock"},
                                status=status.HTTP_400_BAD_REQUEST)

            total_price = book.price * quantity
            transaction = Transaction.objects.create(
                user=user, book=book, quantity=quantity,
                total_price=total_price
            )

            # Update book stock
            book.stock -= quantity
            book.save()

            return Response(TransactionSerializer(transaction).data,
                            status=status.HTTP_201_CREATED)

        except Book.DoesNotExist:
            return Response({"error": "Book not found"},
                            status=status.HTTP_404_NOT_FOUND)
