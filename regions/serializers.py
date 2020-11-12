from rest_framework.serializers import (
    ModelSerializer, HyperlinkedModelSerializer, HyperlinkedRelatedField)

from regions.models import (
    StgLocationLevel, StgEconomicZones, StgLocation)

class StgLocationLevelSerializer(ModelSerializer):
    class Meta:
        model = StgLocationLevel
        fields = ['locationlevel_id', 'type', 'name', 'code', 'description']


class StgEconomicZonesSerializer(ModelSerializer):
    class Meta:
        model = StgEconomicZones
        fields = ['economiczone_id', 'name', 'code', 'shortname', 'description']


class StgLocationSerializer(ModelSerializer):
    class Meta:
        model = StgLocation
        fields = [
            'location_id', 'locationlevel','name', 'iso_alpha','iso_number','code',
            'description', 'parent', 'latitude','longitude','cordinate','wb_income',
            'zone','special']
