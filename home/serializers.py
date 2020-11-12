from rest_framework.serializers import ModelSerializer
from home.models import (StgDatasource, StgCategoryParent, StgCategoryoption)


class StgDisagregationCategorySerializer(ModelSerializer):
    class Meta:
        model = StgCategoryParent
        fields = ['category_id', 'name', 'shortname', 'code', 'description',]


class StgDisagregationOptionsSerializer(ModelSerializer):
    class Meta:
        model = StgCategoryoption
        fields = ['categoryoption_id', 'category','name', 'shortname', 'code',
                'description']

class StgDatasourceSerializer(ModelSerializer):
    class Meta:
        model = StgDatasource
        fields = ['datasource_id', 'name', 'shortname', 'code','description']
