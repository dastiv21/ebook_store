from rest_framework.pagination import PageNumberPagination

class BookPagination(PageNumberPagination):
    page_size = 5  # Set custom page size
    page_size_query_param = 'page_size'  # Allow client to override
    max_page_size = 20  # Maximum number of items per page
