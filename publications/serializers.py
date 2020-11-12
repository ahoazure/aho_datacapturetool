from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField)
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from publications.models import (StgResourceType,StgKnowledgeProduct,
    StgProductDomain)

class StgResourceTypeSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=StgResourceType)

    class Meta:
        model = StgResourceType
        fields = ['type_id','code','translations']


class StgKnowledgeDomainSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=StgProductDomain)

    class Meta:
        model = StgProductDomain
        fields = ['domain_id', 'code','parent','translations']


class StgKnowledgeProductSerializer(ModelSerializer):
    location_name = ReadOnlyField(source='location.name')
    class Meta:
        model = StgKnowledgeProduct
        fields = ['product_id','title','code','type','categorization',
        'location_name','description', 'abstract','author','year_published',
        'internal_url','external_url','cover_image','comment']
