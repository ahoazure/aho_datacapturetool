from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
# from rest_framework.serializers import (
#     ModelSerializer, ReadOnlyField)
from .models import (StgHealthFacility,StgFacilityType,
    StgFacilityOwnership)

class StgHealthFacilitySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=StgHealthFacility)
    class Meta:
        model = StgHealthFacility
        fields = ('owner','name',)
        data_wizard = {
        'header_row': 0,
        'start_row': 1,
        'show_in_list': True,
    }

# class StgResourceTypeSerializer(ModelSerializer):
#     class Meta:
#         model = StgResourceType
#         fields = ['type_id','name', 'code','description']
#
# class StgKnowledgeDomainSerializer(ModelSerializer):
#     class Meta:
#         model = StgProductDomain
#         fields = ['domain_id', 'name', 'shortname', 'code', 'description','parent',
#             'publications']
