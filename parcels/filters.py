from django.contrib.gis.geos import GEOSGeometry
from rest_framework.filters import BaseFilterBackend
from rest_framework_gis.filterset import GeoFilterSet


class PolygonFilterBackend(BaseFilterBackend):
    """
    Enables filtering down to parcels that are within the user-posted polygon
    """
    def filter_queryset(self, request, queryset, view):
        polygon = request.data.get("polygon")
        if polygon is None:
            return queryset
        polygon = GEOSGeometry(polygon)
        return queryset.filter(boundary__intersects=polygon)


class ParcelFilter(GeoFilterSet):
    """
    Allows doing common filter operations directly on the attributes of the
    parcel in the database
    """
    class Meta:
        model = Parcel
        fields = {
            "parcel_id": ["icontains", "exact"]
            "address": ["icontains", "exact"],
            "average_income": ["exact"],
            "value": ["exact", "gt", "gte", "lt", "lte"],
        }
