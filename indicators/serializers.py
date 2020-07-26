from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField, DecimalField)

from indicators.models import (
    StgIndicatorReference, StgIndicator, StgIndicatorDomain,
    FactDataIndicator,)

class StgIndicatorReferenceSerializer(ModelSerializer):
    class Meta:
        model = StgIndicatorReference
        fields = ['reference_id', 'name', 'shortname', 'code', 'description']


class StgIndicatorSerializer(ModelSerializer):
    class Meta:
        model = StgIndicator
        fields = [
            'indicator_id', 'name', 'shortname', 'afrocode', 'gen_code',
            'definition','measuremethod','numerator_description',
            'denominator_description','preferred_datasources', 'reference',
        ]


class StgIndicatorDomainSerializer(ModelSerializer):
    class Meta:
        model = StgIndicatorDomain
        fields = [
            'domain_id', 'name', 'shortname', 'code', 'description',
            'parent', 'indicators']

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
            'fact_id', 'indicator', 'location', 'location_name', 'numerator_value',
            'categoryoption','datasource','valuetype','denominator_value','datasource',
            'value_received','min_value','max_value','target_value','start_period',
            'end_period', 'period','comment','string_value']

        data_wizard = {
            'header_row': 0,
            'start_row': 1,
            'show_in_list': True,
        }
