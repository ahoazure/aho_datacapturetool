from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField)

from publications.models import (StgResourceType,StgKnowledgeProduct,
    StgProductDomain)

class StgResourceTypeSerializer(ModelSerializer):
    class Meta:
        model = StgResourceType
        fields = ['type_id','name', 'code','description']


class StgKnowledgeProductSerializer(ModelSerializer):
    location_name = ReadOnlyField(source='location.name')
    class Meta:
        model = StgKnowledgeProduct
        fields = ['product_id','title','code','type','categorization',
        'location_name','description', 'abstract','author','year_published',
        'internal_url','external_url','cover_image','comment']


class StgKnowledgeDomainSerializer(ModelSerializer):
    class Meta:
        model = StgProductDomain
        fields = ['domain_id', 'name', 'shortname', 'code', 'description','parent',
            'publications']
