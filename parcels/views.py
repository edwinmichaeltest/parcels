from parcels.model import Parcel
from parcels.serializer import ParcelSerializer
from rest_framework_gis.filters import InBBoxFilter
from parcel.filters import PolygonFilterBackend, ParcelFilter

class ParcelList(ListAPIView):
    """
    API Views for fetching parcels and parcel information
    """
    serializer_class = ParcelSerializer
    queryset = Parcel.objects.all()
    model = Parcel
    ordering = "id"
    bbox_filter_field = "boundary"
    bbox_filter_include_overlapping = True
    filter_backends = (
        InBBoxFilter,
        PolygonFilterBackend,
    )
    filter_class = ParcelFilter

    @property
    def average_value(self):
        """
        Checks whether or not the user wants to get the average value
        of a list of parcels instead of the parcels themselves.
        """
        params = self.request.query_params
        return params.get("average_value", False) == "true"

    def get_average_value(self):
        """
        Gets the average value of the currently-filtered parcels.
        """
        queryset = self.filter_queryset(self.get_queryset())
        average_value = queryset.value.aggregate(
            Avg('value')).values()[0]
        return Response(average_value)

    def list(self, request, *args, **kwargs):
        """
        Lists all the parcels that fit the given filter criteria
        (e.g. are within the current bounding box, have an income gte X)
        """
        if self.average_value:
            return self.get_average_value()
        return super(ParcelList, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Takes a user-provided polygon and returns all the parcels that
        intersect that polygon
        """
        if self.class_counts:
            return self.get_average_value()
        queryset = self.filter_queryset(self.get_queryset())
        context = {"request": request}
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context=context, many=True)
        response_content = serializer.data
        return Response(response_content)
