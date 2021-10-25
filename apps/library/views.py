from django.http import JsonResponse
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.library.book import Collection
from apps.library.serializers import SearchBookSerializer, BookDetailSerializer
from utils.auth import Authentication
from utils.custom_response.base_constant import CODE_METHOD_ERROR
from utils.custom_response.base_response import BaseResponse


class SearchBookViewSet(mixins.CreateModelMixin,
                        GenericViewSet):
    serializer_class = SearchBookSerializer
    authentication_classes = [Authentication, ]

    def create(self, request, *args, **kwargs):
        book = Collection()
        try:
            search_book = book.search_book(request.data)
        except Exception as e:
            return BaseResponse(code=CODE_METHOD_ERROR, message=str(e))
        return BaseResponse(data=search_book)


class BookDetailViewSet(mixins.CreateModelMixin,
                        GenericViewSet):
    serializer_class = BookDetailSerializer
    authentication_classes = [Authentication, ]

    def create(self, request, *args, **kwargs):
        book = Collection()
        try:
            book_detail = book.book_detail(request.data)
        except Exception as e:
            return BaseResponse(code=CODE_METHOD_ERROR, message=str(e))
        return BaseResponse(data=book_detail)
