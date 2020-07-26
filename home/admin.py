from django.contrib import admin
from parler.admin import TranslatableAdmin
from regions.models import StgLocation
from data_wizard.admin import ImportActionModelAdmin
from data_wizard.sources.models import FileSource,URLSource #customize import sourece
from django.forms import TextInput,Textarea #for customizing textarea row and column size
from commoninfo.admin import OverideImportExport, OverideExport
from .models import (StgCategoryParent,StgCategoryoption,StgMeasuremethod,
    StgValueDatatype,StgDatasource)
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom import


@admin.register(StgCategoryParent)
class DisaggregateCategoryAdmin(TranslatableAdmin,OverideExport):
    menu_title = "Disagregation Categories"
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    #resource_class = DisaggregateCategoryExport #for export only
    list_display=['name','code','shortname','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('name', 'shortname','code',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


@admin.register(StgCategoryoption)
class DisaggregationAdmin(TranslatableAdmin,OverideExport):
    menu_title = "Category Options"
    fieldsets = (
        ('Disaggregation Attributes', {
                'fields': ('category', 'name','shortname',)
            }),
            ('Detailed Description', {
                'fields': ('description',),
            }),
        )
    #resource_class = DisaggregateOptionExport #for export only
    list_display=['name','code','shortname','description','category',]
    list_display_links = ('code', 'name',)
    search_fields = ('name',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)
    list_filter = (
        ('category',RelatedOnlyDropdownFilter,), #must put this comma for inheritance
    )


@admin.register(StgValueDatatype)
class DatatypeAdmin(TranslatableAdmin,OverideExport):
    menu_title = "Data Types"
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    #resource_class = DataTypeExport
    list_display=['code','name','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('name','code',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)

@admin.register(StgDatasource)
class DatasourceAdmin(TranslatableAdmin,OverideExport):
    menu_title = "Data Sources"
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
        ('Data source Attributes', {
                'fields': ('name','shortname',)
            }),
            ('Detailed Description', {
                'fields': ('description',),
            }),
        )
    #resource_class = DataSourceExport #for export only
    list_display=['name','shortname','code','description']
    list_display_links = ('code', 'name',)
    search_fields = ('code','name',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)


@admin.register(StgMeasuremethod)
class MeasuredAdmin(TranslatableAdmin,OverideExport):
    menu_title = "Indicator Types"
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    #resource_class = MeasureTypeExport
    list_display=['code','name','measure_value','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('name',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)
