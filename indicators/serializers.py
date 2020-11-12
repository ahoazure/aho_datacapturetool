from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField, DecimalField)
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from indicators.models import (
    StgIndicatorReference, StgIndicator, StgIndicatorDomain,
    FactDataIndicator,)

class StgIndicatorReferenceSerializer(ModelSerializer):
    translations = TranslatedFieldsField(shared_model=StgIndicatorReference)

    class Meta:
        model = StgIndicatorReference
        fields = ['reference_id','code', 'translations']


class StgIndicatorSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=StgIndicator)

    class Meta:
        model = StgIndicator
        fields = [
            'uuid','indicator_id','afrocode', 'gen_code','reference',
            'translations'
        ]


class StgIndicatorDomainSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=StgIndicatorDomain)

    class Meta:
        model = StgIndicatorDomain
        fields = ['domain_id', 'code','parent','translations']

# This clas overrides the decimal field in order to
# round off the decimal places.
class RoundedDecimalField(DecimalField):
    def validate_precision(self, value):
        return value

# Force import wizard to ignore the decimal places and required validation to allow null
class FactDataIndicatorSerializer(ModelSerializer):
    location_name = ReadOnlyField(source='location.name')
    numerator_value = RoundedDecimalField(
        max_digits=20,decimal_places=3,required=False,allow_null=True)
    denominator_value = RoundedDecimalField(
        max_digits=20, decimal_places=3,required=False,allow_null=True)
    value_received = RoundedDecimalField(
        max_digits=20, decimal_places=3,required=True,allow_null=False)
    min_value = RoundedDecimalField(
        max_digits=20,decimal_places=3,required=False,allow_null=True)
    max_value = RoundedDecimalField(
        max_digits=20, decimal_places=3,required=False,allow_null=True)
    target_value = RoundedDecimalField(
        max_digits=20, decimal_places=3,required=False,allow_null=True)

    class Meta:
        model = FactDataIndicator
        fields = [
            'fact_id','indicator', 'location','location_name','categoryoption',
            'datasource','measuremethod','numerator_value','denominator_value',
            'value_received','min_value','max_value','target_value','string_value',
            'start_period','end_period','period','comment']

        data_wizard = {
            'header_row': 0,
            'start_row': 1,
            'show_in_list': True,
        }
