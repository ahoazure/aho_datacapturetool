from import_export import resources
from import_export.fields import Field
from .models import StgKnowledgeProduct
from import_export.widgets import ForeignKeyWidget
from .models import StgProductDomain
from home.models import StgDatasource
from regions.models import StgLocation

#Davy's Skype 26/10/2018 suggestions - limit fields to be imported/exported here using ModelResource. This also applies to
class StgKnowledgeProductResourceExport (resources.ModelResource):
    code = Field(attribute='code', column_name='Product Code')
    title = Field(attribute='title', column_name='Product Name')
    type = Field(attribute='type', column_name='Product Type')
    domain = Field(attribute='domain__name', column_name='Product Domain')
    location = Field(attribute='location_name', column_name='Country/Regional Office')
    repository = Field(attribute='datasource__name', column_name='Source Repositoy')
    abstract = Field(attribute='abstract', column_name='Abstract')
    author = Field(attribute='author', column_name='Author')
    year_published = Field(attribute='year_published', column_name='Year Published')
    external_url = Field(attribute='external_url', column_name='Hyperlink (URL)')


    class Meta:
        model = StgKnowledgeProduct
        skip_unchanged = False
        report_skipped = False
        fields = ('code','title','type','domain','location','repository', 'abstract','author',
            'year_published','external_url',)


class StgKnowledgeProductResourceImport (resources.ModelResource):
    def before_save_instance(
        self, instance, using_transactions, dry_run):

        save_instance( # Called with dry_run=True to ensure no records are saved
            instance, using_transactions=True, dry_run=True)

    def get_instance(self, instance_loader, row):
        return False  # To override the need for the id in the import file

    # Called when you click confirm to the interface
    def save_instance(self, instance, using_transactions=True, dry_run=False):
        if dry_run:
            pass
        else:
            #import pdb; pdb.set_trace()
            instance.save()

    code = Field( column_name='Product Code', attribute='code',)
    title = Field(column_name='Title', attribute='title')
    type = Field(column_name='Product Type', attribute='type')
    domain = Field(column_name='Domain Code',attribute='domain',
        widget=ForeignKeyWidget(StgProductDomain, 'code'))

    location_code = Field(column_name='Country Code',attribute='location_code',
        widget=ForeignKeyWidget(StgLocation, 'code'))

    location_name = Field( # Define the location name but exclude it in processing the file
        column_name='Country Name',
        attribute='location',
        widget=ForeignKeyWidget(StgLocation, 'name'))

    repository = Field(
        column_name='Source Repository',
        attribute='repository',
        widget=ForeignKeyWidget(StgDatasource, 'code'))
    description = Field(
        column_name='Description', attribute='description')
    abstract = Field(column_name='Abstract', attribute='abstract')
    author = Field(column_name='Author(s)', attribute='author')
    year_published = Field(column_name='Year', attribute='year_published')
    external_url = Field(column_name='External Link', attribute='external_url')

    class Meta:
        exclude = ('location_name',)
        model = StgKnowledgeProduct
        skip_unchanged = False
        report_skipped = False
        fields = ('code','title', 'type','domain','location_code','repository',
            'description','abstract', 'author','year_published','external_url', )
