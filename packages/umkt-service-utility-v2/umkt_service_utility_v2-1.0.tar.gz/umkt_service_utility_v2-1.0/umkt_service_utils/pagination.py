from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UMKTPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 10

    def get_paginated_response(self, data):
        if self.page_size_query_param:
            self.page_size = self.get_page_size(self.request)
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'per_page': self.page_size,
            "total_pages": self.page.paginator.num_pages,
            'results': data
        })
