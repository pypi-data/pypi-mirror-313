from typing import Union

from rest_framework.renderers import JSONRenderer

from .types import Response


class APIRenderer(JSONRenderer):
    pagination_result_field: str = 'results'
    errors_field: str = 'errors'

    def process(self, data, renderer_context):
        # request = renderer_context['request']
        response = renderer_context['response']
        success = not response.exception
        pagination = self.get_pagination(data)
        return Response(
            success=success,
            status_code=response.status_code,
            pagination=pagination,
            errors=self.get_errors(success, data, renderer_context),
            data=self.get_data(success, pagination, data, renderer_context),
            service_data=self.get_service_data(
                success, pagination, data, renderer_context,
            ),
        )

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = self.process(data, renderer_context)
        data = data.__dict__
        ret = super().render(data, accepted_media_type, renderer_context)
        return ret

    def get_errors(self, success: bool, data, renderer_context) -> list:
        if success:
            return []
        return data[self.errors_field]

    def get_pagination(self, data) -> Union[dict, None]:
        try:
            pagination_data = {
                k: v for k, v in data.items() if k != self.pagination_result_field
            }
        except AttributeError:
            pagination_data = {}
        if pagination_data.get('count') is not None:
            return pagination_data

    def get_data(
            self, success: bool, pagination, data, renderer_context,
    ) -> Union[dict, list, None]:
        if not success:
            return
        if not pagination:
            return data
        return data[self.pagination_result_field]

    def get_service_data(
            self, success: bool, pagination, data, renderer_context,
    ) -> Union[dict, list, None]:
        if not success:
            return
        return renderer_context.get('service')
