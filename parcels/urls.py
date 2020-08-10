from django.urls import re_path
from parcels.views import ParcelListView

urlpatterns = [
    re_path(r'^parcels/$', ParcelListView.as_view(), name='list-parcels'),
]
