from django.conf import settings

from .types import Error

DEFAULT_MAPPING = dict(
    required=Error(code='value_required'),
    unique=Error(code='not_unique_value'),
    method_not_allowed=Error(location='http'),
)

RESPONSE_ERROR_MAPPING = getattr(settings, 'RESPONSE_ERROR_MAPPING', None) or DEFAULT_MAPPING
