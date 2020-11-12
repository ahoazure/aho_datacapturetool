from django.contrib import admin
from parler.admin import TranslatableAdmin
from django.forms import TextInput,Textarea #for customizing textarea row and column size
from .models import (StgLocationLevel,StgEconomicZones,StgWorldbankIncomegroups,
    StgSpecialcategorization,StgLocation)
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom
from commoninfo.admin import OverideExport,OverideImportExport,OverideImport
from .resources import (LocationLevelResourceExport,IncomegroupsResourceExport,
    EconomicZoneResourceExport,SpecialcategorizationResourceExport,
    LocationResourceExport,LocationResourceImport)
from import_export.admin import (ExportMixin, ImportExportModelAdmin,
    ImportExportActionModelAdmin,)
from import_export import resources #This is required to limit the import/export fields 26/10/2018

#the following 3 functions are used to register global actions performed on the data. See actions listbox
def pending (modeladmin, request, queryset):
    queryset.update(comment = 'pending')
pending.short_description = "Mark selected as Pending"

def approved (modeladmin, request, queryset):
    queryset.update (comment = 'approved')
approved.short_description = "Mark selected as Approved"

def rejected (modeladmin, request, queryset):
    queryset.update (comment = 'rejected')
rejected.short_description = "Mark selected as Rejected"

@admin.register(StgLocationLevel)
class RegionAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    resource_class = LocationLevelResourceExport
    list_display=['name','code','type','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('code','translations__name','translations__type') #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)
    list_filter = (
        ('translations__name',DropdownFilter),
    )

@admin.register(StgEconomicZones)
class EconomicBlocksAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    resource_class = EconomicZoneResourceExport
    list_display=['name','code','shortname','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('translations__name','translations__shortname','code') #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code')


@admin.register(StgWorldbankIncomegroups)
class WBGroupsAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    resource_class = IncomegroupsResourceExport
    list_display=['name','code','shortname','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('code','translations__name','translations__shortname') #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


@admin.register(StgSpecialcategorization)
class SpecialStatesAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    resource_class = SpecialcategorizationResourceExport
    list_display=['name','code','shortname','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('translations__name','translations__shortname','code') #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code')


@admin.register(StgLocation)
class LocationAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(
            name__icontains='Admin' or request.user.location>=1):
            return qs #provide access to all instances of fact data indicators
        return qs.filter(location_id=request.user.location_id)

    """
    # #This function is for filtering location to display regional level only.
    The database field must be parentid for the dropdown list
    The superuser can access all levels and countries at level 2 in the database
    """
    def formfield_for_foreignkey(self, db_field, request =None, **kwargs): #to implement user filtering her
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

        if db_field.name == "locationlevel":
            if request.user.is_superuser or request.user.groups.filter(
                name__icontains='Admin' or request.user.location>=1):
                kwargs["queryset"] = StgLocationLevel.objects.all().order_by(
                    'translations__name',) #superuser can access all levels
            else:
                kwargs["queryset"] = StgLocationLevel.objects.filter(
                    locationlevel__locationlevel_id__gte=2).order_by(
                        'translations__name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        ('Location Details',{
                'fields': (
                    'locationlevel','name', 'iso_alpha','iso_number','description', )
            }),
            ('Geo-map Info', {
                'fields': ('parent','longitude','latitude', 'cordinate',),
            }),
            ('Socioeconomic Status', {
                'fields': ('wb_income','zone','special',),
            }),
        )
    resource_class = LocationResourceExport
    list_display=['name','code','parent','special','zone',]
    list_display_links = ('code', 'name',) #display as clickable link
    search_fields = ('translations__name','code',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)
    list_filter = (
        ('locationlevel',RelatedOnlyDropdownFilter),
        ('parent',RelatedOnlyDropdownFilter),
    )
