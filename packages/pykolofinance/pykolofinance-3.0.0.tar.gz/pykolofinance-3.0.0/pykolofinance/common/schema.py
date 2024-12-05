from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

header = extend_schema(
    parameters=[OpenApiParameter(
        "X-Api-Key", OpenApiTypes.STR,
        OpenApiParameter.HEADER, required=True)
    ])
