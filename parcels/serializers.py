from rest_framework_gis.serializers import GeoFeatureModelSerializer

from parcels.model import Parcel


class ParcelSerializer(GeoFeatureModelSerializer):
    """
    Boilerplate for converting parcels -> json.
    """

    class Meta:
        model = Parcel
        geo_field = "boundary"
        fields = (
            "parcel_id",
            "address",
            "average_income",
            "value"
        )
