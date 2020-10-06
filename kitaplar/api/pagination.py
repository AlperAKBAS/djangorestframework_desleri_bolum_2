from rest_framework.pagination import PageNumberPagination


class SmallPagination(PageNumberPagination):
    page_size = 5


class LargePagination(PageNumberPagination):
    page_size = 25
    page_query_param = 'sayfa'
