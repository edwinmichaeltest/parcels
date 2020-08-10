from django.contrib.gis.db import models


class Parcel(models.Model):

    class Meta:
        required_db_features = ["gis_enabled"]

    parcel_id = models.CharField(
        "Parcel ID", max_length=100, null=True, db_index=True
    )
    address = models.CharField("Parcel Address", max_length=256)
    average_income = models.FloatField(
        "Average income for the local census tract")
    value = models.FloatField("Last sale price of this parcel")
    boundary = models.PolygonField(srid=4326)

    def __str__(self):
        return self.address

    @property
    def __geo_interface__(self):
        return {
            "geometry": {"type": "Polygon", "coordinates": self.boundary},
            "properties": {"customer_class": self.customer_class},
        }
