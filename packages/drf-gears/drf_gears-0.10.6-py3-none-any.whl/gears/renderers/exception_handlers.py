from copy import copy

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseNotFound
from gears.renderers.mapping import RESPONSE_ERROR_MAPPING
from gears.renderers.types import Error
from rest_framework import exceptions
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import set_rollback


class ExceptionHandler(object):
    default_code: str = 'unknown_error'
    default_description: str = 'Unknown error'
    default_status_code: str = status.HTTP_500_INTERNAL_SERVER_ERROR
    root_field_name: str = 'errors'

    def __init__(self, exc, context):
        self.exc = exc
        self.context = context
        self.status_code = None
        self.errors: list = []
        self.data = {}
        self.headers = {}

    def _super(self):
        exc = self.exc
        headers = {}
        if isinstance(exc, Http404):
            exc = HttpResponseNotFound()
        elif isinstance(exc, PermissionDenied):
            exc = exceptions.PermissionDenied()

        try:
            self.status_code = exc.status_code
        except AttributeError:
            self.status_code = self.default_status_code

        if isinstance(exc, exceptions.APIException):
            if getattr(exc, 'auth_header', None):
                headers['WWW-Authenticate'] = exc.auth_header
            if getattr(exc, 'wait', None):
                headers['Retry-After'] = '%d' % exc.wait
            set_rollback()

            self.data = exc.detail
        else:
            self.data = str(exc)
        self.headers = headers
        self.exc = exc

    def process_list(self, detail: list, location):
        for v in detail:
            self.process(v, location=location)

    def process_dict(self, detail: dict, location):
        for k, v in detail.items():
            self.process(v, location=k)

    def process_error(self, detail, location):
        if status.is_server_error(self.status_code):
            raise self.exc
        self.errors.append(
            Error(
                code=getattr(detail, 'code', self.default_code),
                location=location,
                description=str(detail) or self.default_description,
                detail=None,
            )
        )

    def process(self, detail, location: str = None):
        if isinstance(detail, list):
            return self.process_list(detail, location)
        if isinstance(detail, dict):
            return self.process_dict(detail, location)
        return self.process_error(detail, location)

    def response(self) -> list[dict]:
        def _build(e: Error):
            er = copy(RESPONSE_ERROR_MAPPING.get(e.code, e))
            for k in ('code', 'location', 'description', 'detail',):
                # set values from me or e
                setattr(er, k, getattr(er, k) or getattr(e, k))
            return er.__dict__
        return [_build(err) for err in self.errors]

    def handle(self):
        self._super()
        self.process(self.data)
        data = {
            self.root_field_name: self.response(),
        }

        return Response(
            data=data,
            headers=self.headers,
            status=self.status_code,
        )


def exception_handler(exc, context):
    return ExceptionHandler(exc, context).handle()
