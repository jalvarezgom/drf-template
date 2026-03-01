from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.response import Response


class QuerysetResponse:
    def __init__(self, viewset: viewsets.GenericViewSet, queryset: QuerySet, *args, **kwargs):
        self.viewset = viewset
        self.queryset = queryset
        self.args = args
        self.kwargs = kwargs

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.viewset.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {"request": self.viewset.request, "format": self.viewset.format_kwarg, "view": self.viewset}

    def response(self, *args, **kwargs) -> Response:
        try:
            response = Response(self.viewset.get_serializer(self.queryset).data, *args, **kwargs)
        except AttributeError:
            response = Response(self.get_serializer(self.queryset).data, *args, **kwargs)
        return response

    def many(self, *args, **kwargs) -> Response:
        try:
            serializer = self.viewset.get_serializer(self.queryset, many=True, *args, **kwargs)
        except AttributeError:
            serializer = self.get_serializer(self.queryset, many=True, *args, **kwargs)
        return Response(serializer.data)

    def paginated(self, *args, **kwargs) -> Response:
        page = self.viewset.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.viewset.get_serializer(page, many=True)
            return self.viewset.get_paginated_response(serializer.data)
        return self.many(*args, **kwargs)
