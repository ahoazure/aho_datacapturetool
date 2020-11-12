from django.contrib import admin
from parler.admin import TranslatableAdmin
from django.utils.translation import gettext_lazy as _ #For translating imported verbose_name
from regions.models import StgLocation
from data_wizard.admin import ImportActionModelAdmin
from data_wizard.sources.models import FileSource,URLSource #customize import sourece
from django.forms import TextInput,Textarea #for customizing textarea row and column size
from commoninfo.admin import OverideImportExport, OverideExport
from .models import (StgCategoryParent,StgCategoryoption,StgMeasuremethod,
    StgValueDatatype,StgDatasource)
from .resources import(DisaggregateCategoryExport,DataSourceExport,
    DisaggregateOptionExport,MeasureTypeExport,DataTypeExport)
from import_export.admin import (ImportExportModelAdmin,
    ImportExportActionModelAdmin,)
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom import


@admin.register(StgCategoryParent)
class DisaggregateCategoryAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    resource_class = DisaggregateCategoryExport #for export only
    list_display=['name','code','shortname','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('translations__name', 'translations__shortname','code',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


@admin.register(StgCategoryoption)
class DisaggregationAdmin(TranslatableAdmin,OverideExport):
    fieldsets = (
        ('Disaggregation Attributes', {
                'fields': ('name','shortname','category',)
            }),
            ('Detailed Description', {
                'fields': ('description',),
            }),
        )
    resource_class = DisaggregateOptionExport #for export only
    list_display=['name','code','shortname','description','category',]
    list_display_links = ('code', 'name',)
    search_fields = ('translations__name', 'translations__shortname',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)
    list_filter = (
        ('category',RelatedOnlyDropdownFilter,), #must put this comma for inheritance
    )


@admin.register(StgValueDatatype)
class DatatypeAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    resource_class = DataTypeExport
    list_display=['name','code','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('translations__name', 'translations__shortname','code',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)

@admin.register(StgDatasource)
class DatasourceAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
        ('Data source Attributes', {
                'fields': ('name','shortname','level',)
            }),
            ('Detailed Description', {
                'fields': ('description',),
            }),
        )
    resource_class = DataSourceExport #for export only
    list_display=['name','shortname','code','description','level']
    list_display_links = ('code', 'name',)
    search_fields = ('translations__name', 'translations__shortname',
        'code','translations__level') #display search field
    list_per_page = 50 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)


@admin.register(StgMeasuremethod)
class MeasuredAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    resource_class = MeasureTypeExport
    list_display=['name','code','measure_value','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('translations__name','code',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)

# ------------------------------------------------------------------------------------------
# The following two admin classes are used to customize the Data_Wizard page.
# The classes overrides admin.py in site-packages/data_wizard/sources/
# ------------------------------------------------------------------------------------------
class FileSourceAdmin(ImportActionModelAdmin):
    menu_title = _("Import Data File... ")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(
            name__icontains='Admin' or request.user.location>=1):
            return qs #provide access to all instances of fact data indicators
        return qs.filter(location=request.user.location)

    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        if db_field.name == "location":
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocation.objects.filter(
                # Looks up for the traslated location level name in related table
                locationlevel__locationlevel_id__gte=1).order_by(
                    'locationlevel', 'location_id') #superuser can access all countries at level 2 in the database
            elif request.user.groups.filter(
                name__icontains='Admin' or request.user.location>=1):
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__locationlevel_id__gte=1,
                locationlevel__locationlevel_id__lte=2).order_by(
                    'locationlevel', 'location_id')
            else:
                kwargs["queryset"] = StgLocation.objects.filter(
                location_id=request.user.location_id) #permissions to user country only
        return super().formfield_for_foreignkey(db_field, request,**kwargs)

    fields = ('location','name','file',)
    list_display=['name','location','date']
admin.site.register(FileSource, FileSourceAdmin)


# This class admin class is used to customize change page for the URL data source
class URLSourceAdmin(ImportActionModelAdmin):
    menu_title = _("Import via URL...")
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(
            name__icontains='Admin' or request.user.location>=1):
            return qs #provide access to all instances of fact data indicators
        return qs.filter(location=request.user.location)

    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        if db_field.name == "location":
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocation.objects.filter(
                # Looks up for the traslated location level name in related table
                locationlevel__locationlevel_id__gte=1).order_by(
                    'locationlevel', 'location_id') #superuser can access all countries at level 2 in the database
            elif request.user.groups.filter(
                name__icontains='Admin' or request.user.location>=1):
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__locationlevel_id__gte=1,
                locationlevel__locationlevel_id__lte=2).order_by(
                    'locationlevel', 'location_id')
            else:
                kwargs["queryset"] = StgLocation.objects.filter(
                location_id=request.user.location_id) #permissions to user country only
        return super().formfield_for_foreignkey(db_field, request,**kwargs)
        
    fields = ('location','name','url',)
    list_display=['name','location','url','date']
admin.site.register(URLSource,URLSourceAdmin)
