from rest_framework.response import Response


class SummaryPaginationMixin:
    """
    This mixin for a DRF pagination class provides a mechanism to add some additional
    summary data. Use it with some standard pagination class like PageNumberPagination
    or LimitOffsetPagination. You should add the method named `get_pagination_summary`
    for ViewSet which returns a dictionary with needed information.
    """

    def get_summary(self, view, queryset, request):
        if view and hasattr(view, 'get_pagination_summary'):
            return view.get_pagination_summary(request, queryset)

    def paginate_queryset(self, queryset, request, view=None):
        self.summary = self.get_summary(view, queryset, request)
        return super().paginate_queryset(queryset=queryset, request=request, view=view)

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        data = response.data
        data['summary'] = self.summary
        return Response(data)
