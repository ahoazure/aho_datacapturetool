from django.contrib import admin
from parler.admin import TranslatableAdmin
from django.utils.html import format_html
from django.forms import BaseInlineFormSet
from django import forms
import data_wizard # Solution to data import madness that had refused to go
from django.forms import TextInput,Textarea #customize textarea row and column size
from import_export.formats import base_formats
from .models import (StgFacilityType,StgFacilityInfrastructure,
    StgFacilityOwnership,StgHealthFacility,StgServiceDomain,
    FacilityServiceAvilability,FacilityServiceAvailabilityProxy)
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

# class LimitModelFormset(BaseInlineFormSet):
#     ''' Base Inline formset to limit inline Model records'''
#     def __init__(self, *args, **kwargs):
#         super(LimitModelFormset, self).__init__(*args, **kwargs)
#         instance = kwargs["instance"]
#         self.queryset = FacilityServiceAvilability.objects.filter(
#             availabilit_id=instance).order_by('-date_created')[:5]


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
class FacilityOwnership (TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    list_display=['name','code','shortname','description',]
    list_display_links =('code', 'name',)
    search_fields = ('code','translations__name','translations__shortname',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


class FacilityServiceAvilabilityInline(admin.TabularInline):
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # import pdb; pdb.set_trace()
        # print (qs)
        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')

    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        db_sevicedomains = StgServiceDomain.objects.all().order_by('domain_id')
        db_sevicesubdomains=db_sevicedomains.exclude(parent_id__isnull=True)

        if request.user.is_superuser:
            if db_field.name == "domain":
                kwargs["queryset"]=db_sevicesubdomains.distinct()

        # if db_field.name == "user":
        #         kwargs["queryset"] = CustomUser.objects.filter(
        #             email=request.user)
        return super().formfield_for_foreignkey(db_field, request,**kwargs)

    # form = IndicatorProxyForm #overrides the default django form
    model = FacilityServiceAvilability
    # formset = LimitModelFormset
    extra = 2 # Used to control  number of empty rows displayed.
    fields = ('domain','facility','intervention','service','provided','specialunit',
        'staff','infrastructure','supplies','start_period','end_period',)



@admin.register(StgServiceDomain)
class ServiceDomainAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    fieldsets = (
        ('Service Domain Attributes', {
                'fields':('name','shortname','description','parent','level') #afrocode may be null
            }),
        )

    list_display=['name','code','shortname','description','level']
    list_display_links =('code', 'name','shortname',)
    search_fields = ('translations__name','translations__shortname','code',) #display search field
    exclude = ('date_created','date_lastupdated','code',)
    list_per_page = 30 #limit records displayed on admin site to 15
    list_filter = (
        ('parent',RelatedOnlyDropdownFilter),
        ('level',DropdownFilter,),# Added 16/12/2019 for M2M lookup
    )


data_wizard.register(StgHealthFacility)
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
                    'locationlevel','location_id')
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
                'fields':('name','shortname','type','description','owner',
                'location','admin_location','status') #afrocode may be null
            }),
            ('Geolocation and Contact Details', {
                'fields': ('latitude','longitude','altitude','geosource',
                'address','email','phone_code','phone_part','url',),
            }),

        )
    # To display the choice field values use the helper method get_foo_display
    list_display=['name','code','type','owner','location','admin_location',
    'latitude','longitude','geosource','status','phone_number']
    list_display_links = ['code','name',]
    search_fields = ('name','type__name','location__name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
    exclude = ('date_created','date_lastupdated','code',)
    list_filter = (
        ('location',RelatedOnlyDropdownFilter),
        ('type',RelatedOnlyDropdownFilter),
    )


@admin.register(FacilityServiceAvailabilityProxy)
class FacilityServiceAvailabilityAdmin(OverideExport):
    inlines = [FacilityServiceAvilabilityInline] #try tabular form
    #This method removes the add button on the admin interface
    """
   Serge requested that a user does not see other users or groups data.
    This method filters logged in users depending on group roles and permissions.
    Only the superuser can see all users and locations data while a users
    can only see data from registered location within his/her group/system role.
    If a user is not assigned to a group, he/she can only own data - 01/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # import pdb; pdb.set_trace()
        # print (qs)
        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')

        db_sevicedomains = FacilityServiceAvilability.objects.all().order_by('domain_id')
        db_sevicesubdomains=db_sevicedomains.exclude(domain__parent_id__isnull=True)

        list_sevicesubdomains= list(
            db_sevicesubdomains.values_list('domain__parent_id', flat=True))

        # import pdb; pdb.set_trace()

        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            return qs
        # returns data for AFRO and member countries
        elif user in groups and user_location==1:
            qs_admin=db_locations.filter(locationlevel__locationlevel_id__gte=1,
                locationlevel__locationlevel_id__lte=2)
        # return data based on the location of the user logged/request location
        elif user in groups and user_location>1:
            qs=qs.filter(location=user_location)
        else: # return own data if not member of a group
            qs=qs.filter(user=request.user).distinct()
        return qs

    """
    Serge requested that the form for data input be restricted to user's country.
    Thus, this function is for filtering location to display country level.
    The location is used to filter the dropdownlist based on the request
    object's USER, If the user has superuser privileges or is a member of
    AFRO-DataAdmins, he/she can enter data for all the AFRO member countries
    otherwise, can only enter data for his/her country.=== modified 02/02/2021
    """
    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):


        if request.user.is_superuser:
            if db_field.name == "domain":
                kwargs["queryset"] = list_sevicesubdomains.filter(domain__parent_id__gt=1)

        # if db_field.name == "user":
        #         kwargs["queryset"] = CustomUser.objects.filter(
        #             email=request.user)
        return super().formfield_for_foreignkey(db_field, request,**kwargs)

    def has_add_permission(self, request, obj=None):
        return False

    def get_import_formats(self):  #This function limits the export format to only 3 types -CSV, XML and XLSX
        """
        This function returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        """
        This function returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    fields = ('name','type','location','admin_location','owner')
    readonly_fields = ('name','type','location','admin_location','owner')
    list_display=['name','type','location','admin_location',]
