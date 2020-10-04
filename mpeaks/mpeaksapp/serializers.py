# from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Peak


class PeakSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Peak
        geo_field = 'location'
        fields = ('location', 'altitude', 'name')
