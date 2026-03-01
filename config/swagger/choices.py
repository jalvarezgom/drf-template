from drf_spectacular.utils import extend_schema, extend_schema_view

from config.swagger import SwaggerTagEnum

choices_viewset_swagger = extend_schema_view(
    card_param_types=extend_schema(summary="Get choice data", description="Retrieve a choice data", tags=[SwaggerTagEnum.CHOICES]),
    card_section_modes=extend_schema(summary="Get choice data", description="Retrieve a choice data", tags=[SwaggerTagEnum.CHOICES]),
    card_section_types=extend_schema(summary="Get choice data", description="Retrieve a choice data", tags=[SwaggerTagEnum.CHOICES]),
    card_status=extend_schema(summary="Get choice data", description="Retrieve a choice data", tags=[SwaggerTagEnum.CHOICES]),
    draft_status=extend_schema(summary="Get choice data", description="Retrieve a choice data", tags=[SwaggerTagEnum.CHOICES]),
    how_know_web=extend_schema(summary="Get choice data", description="Retrieve a choice data", tags=[SwaggerTagEnum.CHOICES]),
    languages=extend_schema(summary="Get choice data", description="Retrieve a choice data", tags=[SwaggerTagEnum.CHOICES]),
)
