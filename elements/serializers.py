from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField, Serializer,DecimalField)

from elements.models import (StgDataElement, FactDataElement)



class StgDataElementSerializer(ModelSerializer):
    class Meta:
        model = StgDataElement
        fields = ['dataelement_id','name','shortname', 'code','measuremethod',
            'description', 'aggregation_type']


# This clas overrides the decimal field in order to
# round off the decimal places.
class RoundedDecimalField(DecimalField):
    def validate_precision(self, value):
        return value

# Force import wizard to ignore the decimal places and required validation to allow null
class FactDataElementSerializer(ModelSerializer):
    value = RoundedDecimalField(
        max_digits=20, decimal_places=3,required=True,allow_null=False)
    target_value = RoundedDecimalField(
        max_digits=20,decimal_places=3,required=False,allow_null=True)

    class Meta:
        model = FactDataElement
        fields = [
            'fact_id', 'dataelement', 'location', 'categoryoption','datasource',
            'valuetype','value', 'target_value', 'start_year', 'end_year', 'period',
            'comment']
