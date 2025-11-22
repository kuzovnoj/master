from drf_spectacular.utils import OpenApiParameter, OpenApiTypes
from ..kuzmaster import settings


PRODUCT_PARAM_EXAMPLE = [
    OpenApiParameter(
        name="page",
        description=f"The amount of item per page you want to display. Defaults to {settings.REST_FRAMEWORK['PAGE_SIZE']}",
        required=False,
        type=OpenApiTypes.INT,
    ),
]