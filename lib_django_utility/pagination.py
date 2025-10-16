from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def get_paginated_response(*, pagination_class, serializer_class, queryset, request, view):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return Response(data=serializer.data)


class BasePagination(PageNumberPagination):
    def get_paginated_response(self, data):
        if self.request.query_params.get("page_size"):
            self.page_size = int(self.request.query_params.get("page_size"))

        return Response(
            {
                "current": self.page.number,
                "page_count": self.page.paginator.num_pages,
                "page_size": self.page_size,
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            },
        )
