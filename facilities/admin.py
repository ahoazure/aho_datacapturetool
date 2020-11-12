from django.contrib import admin
from parler.admin import TranslatableAdmin
from django.utils.html import format_html
import data_wizard # Solution to data import madness that had refused to go
from django.forms import TextInput,Textarea #customize textarea row and column size
from import_export.formats import base_formats
from .models import (StgFacilityType,StgFacilityInfrastructure,
    StgFacilityOwnership,StgHealthFacility,StgServiceDomain)
from commoninfo.admin import OverideImportExport,OverideExport,OverideImport
# from publications.serializers import StgKnowledgeProductSerializer
from .resources import (StgFacilityResourceExport,)
from regions.models import StgLocation
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom
from import_export.admin import (ImportExportModelAdmin, ExportMixin,
    ImportExportActionModelAdmin)

#Methods used to register global actions performed on data. See actions listbox
def transition_to_pending (modeladmin, request, queryset):
    queryset.update(comment = 'pending')
transition_to_pending.short_description = "Mark selected as Pending"

def transition_to_approved (modeladmin, request, queryset):
    queryset.update (comment = 'approved')
transition_to_approved.short_description = "Mark selected as Approved"

def transition_to_rejected (modeladmin, request, queryset):
    queryset.update (comment = 'rejected')
transition_to_rejected.short_description = "Mark selected as Rejected"

@admin.register(StgFacilityType)
class FacilityTypeAdmin(TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    list_display=['name','code','shortname','description']
    list_display_links =('code', 'name',)
    search_fields = ('code','translations__name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


@admin.register(StgFacilityInfrastructure)
class FacilityInfrastructure (TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    list_display=['name','code','shortname','description']
    list_display_links =('code', 'name',)
    search_fields = ('code','translations__name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


@admin.register(StgFacilityOwnership)
class FacilityOwdership (TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    list_display=['name','code','location','shortname','description',]
    list_display_links =('code', 'name',)
    search_fields = ('code','translations__name','translations__shortname',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


@admin.register(StgServiceDomain)
class ServiceDomainAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    fieldsets = (
        ('Service Domain Attributes', {
                'fields':('name','shortname','description','parent',) #afrocode may be null
            }),
        ('Service Domain Facilities', {
                'fields':('facilities','level') #afrocode may be null
            }),
        )

    list_display=['name','code','shortname','description','level']
    list_display_links =('code', 'name','shortname',)
    search_fields = ('translations__name','translations__shortname','code',) #display search field

    filter_horizontal = ('facilities',) # this should display an inline with multiselect
    exclude = ('date_created','date_lastupdated','code',)
    list_per_page = 30 #limit records displayed on admin site to 15
    list_filter = (
        ('parent',RelatedOnlyDropdownFilter),
        ('facilities',RelatedOnlyDropdownFilter,),# Added 16/12/2019 for M2M lookup
    )


@admin.register(StgHealthFacility)
class FacilityAdmin(TranslatableAdmin,ImportExportModelAdmin,OverideImport,
        ImportExportActionModelAdmin):
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

    """
    Returns available export formats.
    """
    def get_import_formats(self):
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        """
        Returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

    #resource_class = StgFacilityResourceExport
    fieldsets = (
        ('Facility Attributes', {
                'fields':('name','shortname','type','description','owner') #afrocode may be null
            }),
            ('Infrastructure and Location', {
                'fields': ('location', 'infrastructure','year_established'),
            }),
            ('Contact & Access Details', {
                'fields': ('latitude','longitude','address','email','phone_number','url',),
            }),
        )
    filter_horizontal = ['infrastructure'] # this should display an inline with multisele
    # To display the choice field values use the helper method get_foo_display where foo is the field name
    list_display=['name','code','year_established','owner','type','url','address',
        'email','phone_number']
    list_display_links = ['code','name',]
    search_fields = ('translations__name','type__translations__name',
    'location__translations__name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
    exclude = ('date_created','date_lastupdated','code',)
    list_filter = (
        ('location',RelatedOnlyDropdownFilter),
        ('type',RelatedOnlyDropdownFilter),
    )
