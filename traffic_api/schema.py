from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import build_basic_type
from django.contrib.gis.db.models import LineStringField

class CustomGeoSchema(AutoSchema):
    def _map_model_field(self, field, direction):
        if isinstance(field, LineStringField):
            return build_basic_type('object')  # ou 'string' se preferir simplificar
        return super()._map_model_field(field, direction)
