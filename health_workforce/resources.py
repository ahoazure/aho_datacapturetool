from import_export import resources
from import_export.fields import Field
from .models import (FactDataIndicator, StgIndicator, StgIndicatorDomain,
    aho_factsindicator_archive,)
from home.models import StgCategoryoption,StgDatasource,StgValueDatatype
from regions.models import StgLocation
from import_export.widgets import ForeignKeyWidget, DateWidget

# This class requires the methods for saving the instance to be overriden
class IndicatorResourceImport(resources.ModelResource):
    def before_save_instance(
        self, instance, using_transactions, dry_run):
        # Called with dry_run=True to ensure no records are saved
        save_instance(
            instance, using_transactions=True, dry_run=True)

    def get_instance(self, instance_loader, row):
        return False  # To override the need for the id in the import file

    def save_instance(self, instance, using_transactions=True, dry_run=False):
            if dry_run:
                pass
            else:
                instance.save()
    indicator_code = Field(column_name='Indicator Code',attribute='indicator',
        widget=ForeignKeyWidget(StgIndicator, 'afrocode'))
    indicator_name = Field(column_name='Indicator Name',attribute='indicator',
        widget=ForeignKeyWidget(StgIndicator, 'name'))
    location_code = Field(column_name='Location Code',attribute='location',
        widget=ForeignKeyWidget(StgLocation, 'code'))
    location_name = Field(column_name='Location Name',attribute='location__name',
        widget=ForeignKeyWidget(StgLocation, 'name'))
    categoryoption_code = Field( column_name='Disaggregaton Code',
        attribute='categoryoption',widget=ForeignKeyWidget(StgCategoryoption, 'code'))
    categoryoption_name = Field(column_name='Disaggregation Option',
        attribute='categoryoption__name',widget=ForeignKeyWidget(StgCategoryoption,'name'))
    datasource = Field( column_name='Data Source',attribute='datasource',
        widget=ForeignKeyWidget(StgDatasource, 'code'))
    valuetype = Field( column_name='Data Value Type',attribute='valuetype',
        widget=ForeignKeyWidget(StgValueDatatype, 'code'))
    start_period = Field(column_name='Start Period', attribute='start_period',)
    end_period = Field(column_name='End Period', attribute='end_period',)
    value_received = Field(column_name='Value',attribute='value_received',)
    target_value = Field(column_name='Target Value',attribute='target_value',)
    string_value = Field(column_name='String Value',attribute='string_value',)
    comment = Field(column_name='Special Remarks',attribute='comment',)

    class Meta:
        model = FactDataIndicator
        skip_unchanged = False
        report_skipped = False
        fields = ('indicator_code', 'location_code', 'categoryoption_code',
            'datasource','valuetype','start_period','end_period',
            'value_received','target_value','string_value','comment',)


class IndicatorResourceExport(resources.ModelResource):
    location__name = Field(attribute='location__name', column_name='Location')
    location__code = Field(attribute='location__code', column_name='Location Code')
    indicator__name = Field(attribute='indicator__name', column_name='Indicator Name')
    indicator__afrocode = Field(attribute='indicator__afrocode', column_name='Code')
    categoryoption__code = Field(attribute='categoryoption__code', column_name='Disaggregation Code')
    categoryoption__name = Field(attribute='categoryoption__name', column_name='Disaggregation Type')
    period = Field(attribute='period', column_name='Period')
    value_received = Field(attribute='value_received', column_name='Value')
    target_value = Field(attribute='target_value', column_name='Target Measure')
    datasource = Field(attribute='datasource', column_name='Data Source')
    valuetype = Field(attribute='valuetype', column_name='Data Type')
    string_value = Field(attribute='string_value', column_name='String Value [Remarks]')
    comment = Field(attribute='comment', column_name='Approval Status')

    class Meta:
        model = FactDataIndicator
        skip_unchanged = False
        report_skipped = False
        fields = ('location__name','location__code','indicator__name',
            'indicator__afrocode','categoryoption__code','categoryoption__name',
            'period','value_received','comment','string_value',)
