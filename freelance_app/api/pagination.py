"""Pagination for API responses."""

from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    """Pagination for Offer API list responses."""
    
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100