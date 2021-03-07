from django.contrib import admin
from parler.admin import TranslatableAdmin
from django.utils.html import format_html
from django.forms import BaseInlineFormSet
from django.shortcuts import redirect
from django import forms
import data_wizard # Solution to data import madness that had refused to go
from django.forms import TextInput,Textarea #customize textarea row and column size
from import_export.formats import base_formats
from .models import (StgFacilityType,StgFacilityServiceMeasureUnits,
    StgFacilityOwnership,StgHealthFacility,StgServiceDomain,StgLocationCodes,
    FacilityServiceAvailability,FacilityServiceAvailabilityProxy,
    FacilityServiceProvision,StgFacilityServiceIntervention,
    FacilityServiceReadiness,StgFacilityServiceAreas,
    FacilityServiceProvisionProxy,FacilityServiceReadinesProxy)
from commoninfo.admin import OverideImportExport,OverideExport,OverideImport
# from publications.serializers import StgKnowledgeProductSerializer
from .resources import (StgFacilityResourceExport,)
from regions.models import StgLocation,StgLocationCodes
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom
from import_export.admin import (ImportExportModelAdmin, ExportMixin,
    ImportExportActionModelAdmin)
from authentication.models import CustomUser, CustomGroup
from bootstrap_datepicker_plus import DatePickerInput # Nice date picker 06/03

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

    """
    Serge requested that a user does not see other users or groups data.
    This method filters logged in users depending on group roles and permissions.
    Only the superuser can see all users and locations data while a users
    can only see data from registered location within his/her group/system role.
    If a user is not assigned to a group, he/she can only own data - 01/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')
        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            qs
        # returns data for AFRO and member countries
        elif user in groups and user_location==1:
            qs_admin=db_locations.filter(
                locationlevel__locationlevel_id__gte=1,
                locationlevel__locationlevel_id__lte=2)
        return qs

    fieldsets = (
        ('Health Facility Type', {
                'fields':('name','shortname','description',) #afrocode may be null
            }),
        )

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

    """
    Serge requested that a user does not see other users or groups data.
    This method filters logged in users depending on group roles and permissions.
    Only the superuser can see all users and locations data while a users
    can only see data from registered location within his/her group/system role.
    If a user is not assigned to a group, he/she can only own data - 01/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')
        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            qs
        # returns data for AFRO and member countries
        elif user in groups and user_location==1:
            qs_admin=db_locations.filter(
                locationlevel__locationlevel_id__gte=1,
                locationlevel__locationlevel_id__lte=2)
        return qs

    fieldsets = (
        ('Facility Ownership Details', {
                'fields':('name','shortname','description',) #afrocode may be null
            }),
        )
    list_display=['name','code','shortname','description',]
    list_display_links =('code', 'name',)
    search_fields = ('code','translations__name','translations__shortname',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


class FacilityServiceAvailabilityProxyForm(forms.ModelForm):
    class Meta:
        model = FacilityServiceAvailability
        fields = ('facility','domain','intervention','service','provided',
        'specialunit','staff','infrastructure','supplies','date_assessed',)
        widgets = {
            'date_assessed': DatePickerInput(), # # default date-format %m/%d/%Y will be used
        }


class FacilityServiceAvailabilityInline(admin.TabularInline):
    """
    Serge requested that a user does not see other users or groups data.
    This method filters logged in users depending on group roles and permissions.
    Only the superuser can see all users and locations data while a users
    can only see data from registered location within his/her group/system role.
    If a user is not assigned to a group, he/she can only own data - 01/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')
        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            qs
        # returns data for AFRO and member countries
        elif user in groups and user_location==1:
            qs_admin=db_locations.filter(
                locationlevel__locationlevel_id__gte=1,
                locationlevel__locationlevel_id__lte=2)
        # return data based on the location of the user logged/request location
        elif user in groups and user_location>1:
            qs=qs.filter(location=user_location)
        return qs

    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        qs = super().get_queryset(request)
        db_sevicedomains = StgServiceDomain.objects.all()
        db_sevicesubdomains=db_sevicedomains.exclude(
            parent_id__isnull=True).filter(category=1)

        db_seviceareas = StgFacilityServiceAreas.objects.select_related(
            'intervention__domain').distinct() #good
        db_interventions=StgFacilityServiceIntervention.objects.select_related(
            'domain').distinct()

        # import pdb; pdb.set_trace()

        if db_field.name == "domain":
            kwargs["queryset"]=db_sevicesubdomains

        if db_field.name == "intervention":
            kwargs["queryset"]=db_interventions

        if db_field.name == "service":
                kwargs["queryset"]=db_seviceareas
        return super().formfield_for_foreignkey(db_field, request,**kwargs)

    # form = FacilityServiceAvailabilityProxyForm #overrides the default model form
    model = FacilityServiceAvailability
    # formset = LimitModelFormset
    extra = 1 # Used to control  number of empty rows displayed.

    fields = ('facility','domain','intervention','service','provided',
        'specialunit','staff','infrastructure','supplies','date_assessed',)


class FacilityServiceCapacityInline(admin.TabularInline):
    """
    Serge requested that a user does not see other users or groups data.
    This method filters logged in users depending on group roles and permissions.
    Only the superuser can see all users and locations data while a users
    can only see data from registered location within his/her group/system role.
    If a user is not assigned to a group, he/she can only own data - 01/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')
        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            qs
        # returns data for AFRO and member countries
        elif user in groups and user_location==1:
            qs_admin=db_locations.filter(
                locationlevel__locationlevel_id__gte=1,
                locationlevel__locationlevel_id__lte=2)
        return qs

    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        db_sevicedomains = StgServiceDomain.objects.all()
        db_sevicesubdomains=db_sevicedomains.exclude(
            parent_id__isnull=True).filter(category=2).filter(level='Level 2')

        db_provisionunits = StgFacilityServiceMeasureUnits.objects.select_related(
            'domain') #good

        if db_field.name == "domain":
            kwargs["queryset"]=db_sevicesubdomains

        if db_field.name == "units":
            kwargs["queryset"]=db_provisionunits.exclude(domain__parent_id=5) # very sgood
        return super().formfield_for_foreignkey(db_field, request,**kwargs)

    model = FacilityServiceProvision
    # formset = LimitModelFormset
    extra = 1 # Used to control  number of empty rows displayed.

    fields = ('facility','domain','units','available','functional',
            'date_assessed',)


class FacilityServiceReadinessInline(admin.TabularInline):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')
        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            qs
        # returns data for AFRO and member countries
        elif user in groups and user_location<=2:
            qs_admin=db_locations.filter(
                locationlevel__locationlevel_id__gt=2,
                locationlevel__locationlevel_id__lte=3)
        return qs

        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')

    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        db_sevicedomains = StgServiceDomain.objects.all()
        db_sevicesubdomains=db_sevicedomains.exclude(
            parent_id__isnull=True).filter(category=3).filter(level='level 1')

        db_provisionunits = StgFacilityServiceMeasureUnits.objects.select_related(
            'domain')


        if db_field.name == "domain":
            kwargs["queryset"]=db_sevicesubdomains

        if db_field.name == "units":
            kwargs["queryset"]=db_provisionunits.filter(domain__parent_id=5) #good!
        return super().formfield_for_foreignkey(db_field, request,**kwargs)

    model = FacilityServiceReadiness
    # formset = LimitModelFormset
    extra = 1 # Used to control  number of empty rows displayed.

    fields = ('facility','domain','units','available','require','date_assessed',)


@admin.register(StgServiceDomain)
class ServiceDomainAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    """
    This method filters logged in users depending on group roles and permissions.
    Only the superuser can see all users and locations data while a users
    can only see data from registered location within his/her group/system role.
    If a user is not assigned to a group, he/she can only own data - 01/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')
        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            qs
        # returns data for AFRO and member countries
        elif user in groups and user_location<=2:
            qs_admin=db_locations.filter(
                locationlevel__locationlevel_id__gt=2,
                locationlevel__locationlevel_id__lte=3)
        return qs

    fieldsets = (
        ('Service Domain Attributes', {
                'fields':('name','shortname','description','parent','category',
                'level') #afrocode may be null
            }),
        )
    list_display=('name','code','shortname','parent','category','level',)
    list_select_related = ('parent',)
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
    """
    This method filters logged in users depending on group roles and permissions.
    Only the superuser can see all users and locations data while a users
    can only see data from registered location within his/her group/system role.
    If a user is not assigned to a group, he/she can only own data - 01/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')
        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            qs
        # returns data for AFRO and member countries
        elif user in groups and user_location<=2:
            qs_admin=db_locations.filter(
                locationlevel__locationlevel_id__gt=2,
                locationlevel__locationlevel_id__lte=3)
        # return data based on the location of the user logged/request location
        elif user in groups and user_location>1:
            qs=qs.filter(location=user_location)
        else: # return own data if not member of a group
            qs=qs.filter(user=request.user).distinct()
        return qs

    """
    Serge requested that the form for data input be restricted to user's location.
    Thus, this function is for filtering location to display country level.
    The location is used to filter the dropdownlist based on the request
    object's USER, If the user has superuser privileges or is a member of
    AFRO-DataAdmins, he/she can enter data for all the AFRO member countries
    otherwise, can only enter data for his/her country.===modified 02/02/2021
    """
    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        qs = super().get_queryset(request)
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        # This queryset is used to load country phone code as a list
        countrycodes=StgLocationCodes.objects.values_list(
            'country_code',flat=True)
        # This queryset is used to load specific phone code for logged in user
        country_code = countrycodes.filter(location=request.user.location)


        if db_field.name == "location":
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocationCodes.objects.all().order_by(
                'location_id')
                # Looks up for the location level upto the country level
            else:
                kwargs["queryset"] = StgLocationCodes.objects.filter(
                location_id=request.user.location_id).order_by(
                'location_id')

        if db_field.name == "phone_code":
            kwargs["queryset"]=country_code # very sgood
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
    list_display=('name','code','type','owner','location','admin_location',
    'latitude','longitude','geosource','status','phone_number')
    # make a 1 query join instead of multiple individual queries
    list_select_related = ('type','owner','location',)
    list_display_links = ['code','name',]
    search_fields = ('name','type__translations__name','status','shortname',
        'code',   'code','location__location__translations__name',
        'owner__translations__name')
    list_per_page = 50 #limit records displayed on admin site to 50
    exclude = ('date_created','date_lastupdated','code',)
    readonly_fields = ('phone_code',)
    list_filter = (
        ('location',RelatedOnlyDropdownFilter),
        ('type',RelatedOnlyDropdownFilter),
        ('owner',RelatedOnlyDropdownFilter),
        ('status',DropdownFilter),
    )


@admin.register(FacilityServiceAvailabilityProxy)
class FacilityServiceAvailabilityAdmin(OverideExport):

    change_form_template = "admin/change_form_availability.html"
    def response_change(self, request, obj):
        if "_capacity-form" in request.POST:
            pass # to be omplemented later to load service capacity form
        if "_readiness-form" in request.POST:
            pass #to be omplemented later to load servicereadiness form
        return super().response_change(request, obj)


    # This method removes the add button on the admin interface
    """
   Serge requested that a user does not see other users or groups data.
    This method filters logged in users depending on group roles and permissions.
    Only the superuser can see all users and locations data while a users
    can only see data from registered location within his/her group/system role.
    If a user is not assigned to a group, he/she can only own data - 01/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')

        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            return qs
        # returns data for AFRO and member countries
        elif user in groups and user_location==1:
            qs_admin=db_locations.filter(
                locationlevel__locationlevel_id__gte=1,
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
        db_sevicedomains = StgServiceDomain.objects.all()
        db_sevicesubdomains=db_sevicedomains.exclude(
            parent_id__isnull=True).filter(category=1)

        if db_field.name == "domain":
            kwargs["queryset"]=db_sevicesubdomains

        if db_field.name == "user":
                kwargs["queryset"] = CustomUser.objects.filter(
                    email=request.user)
        return super().formfield_for_foreignkey(db_field, request,**kwargs)

    def has_add_permission(self, request, obj=None):
        return False

    #This function limits the import format to CSV, XML and XLSX
    def get_import_formats(self):
        """
        This function returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    # This function limits the export format to CSV, XML and XLSX
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

    fieldsets = (
        ('FACILITY DETAILS', {
                'fields':('name','type','location','admin_location','owner',) #afrocode may be null
            }),
        )
    inlines = [FacilityServiceAvailabilityInline] # Displays tabular subform
    list_display=('name','type','location','admin_location','owner',)
    list_select_related = ('type','owner','location','owner',)
    search_fields = ('name','type__translations__name','status','shortname',
    'code','location__location__translations__name','owner__translations__name')
    readonly_fields = ('name','type','location','admin_location','owner','user')
    list_per_page = 50 #limit records displayed on admin site to 50
    list_filter = (
        ('location',RelatedOnlyDropdownFilter),
        ('type',RelatedOnlyDropdownFilter),
        ('owner',RelatedOnlyDropdownFilter),
        ('status',DropdownFilter),
    )



@admin.register(FacilityServiceProvisionProxy)
class FacilityServiceProvisionAdmin(OverideExport):
    change_form_template = "admin/change_form_capacity.html"
    def response_change(self, request, obj):
        if "_capacity-availability" in request.POST:
            pass # to be omplemented later to load service capacity form
        if "_readiness-form" in request.POST:
            pass #to be omplemented later to load servicereadiness form
        return super().response_change(request, obj)

    #This method removes the add button on the admin interface
    def has_add_permission(self, request, obj=None):
        return False

    def get_import_formats(self):  #This method limits import to CSV, XML and XLSX
        """
        This function returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self): #This function returns available export formats.

        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

    # This method removes the add button on the admin interface
    """
   Serge requested that a user does not see other users or groups data.
    This method filters logged in users depending on group roles and permissions.
    Only the superuser can see all users and locations data while a users
    can only see data from registered location within his/her group/system role.
    If a user is not assigned to a group, he/she can only own data - 01/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')

        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            return qs
        # returns data for AFRO and member countries
        elif user in groups and user_location==1:
            qs_admin=db_locations.filter(
                locationlevel__locationlevel_id__gte=1,
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
        db_sevicedomains = StgServiceDomain.objects.all()
        db_sevicesubdomains=db_sevicedomains.exclude(
            parent_id__isnull=True).filter(category=1)

        if db_field.name == "domain":
            kwargs["queryset"]=db_sevicesubdomains

        if db_field.name == "user":
                kwargs["queryset"] = CustomUser.objects.filter(
                    email=request.user)
        return super().formfield_for_foreignkey(db_field, request,**kwargs)

    fieldsets = (
        ('FACILITY DETAILS', {
                'fields':('name','type','location','admin_location','owner',) #afrocode may be null
            }),
        )
    inlines = [FacilityServiceCapacityInline]
    list_display=('name','type','location','admin_location','owner',)
    list_select_related = ('type','owner','location','owner',)
    readonly_fields = ('name','type','location','admin_location','owner')
    search_fields = ('name','type__translations__name','status','shortname',
        'code',   'code','location__location__translations__name',
        'owner__translations__name')
    list_per_page = 50 #limit records displayed on admin site to 50
    list_filter = (
        ('location',RelatedOnlyDropdownFilter),
        ('type',RelatedOnlyDropdownFilter),
        ('owner',RelatedOnlyDropdownFilter),
        ('status',DropdownFilter),
    )



@admin.register(FacilityServiceReadinesProxy)
class FacilityServiceReadinessAdmin(OverideExport):
    # This method adds custom change buttons
    change_form_template = "admin/change_form_readiness.html"
    def response_change(self, request, obj):
        if "_capacity-availability" in request.POST:
            pass # to be omplemented later to load service capacity form
        if "_readiness-form" in request.POST:
            pass #to be omplemented later to load servicereadiness form
        return super().response_change(request, obj)
    # This method removes the add button on the admin interface

    """
   Serge requested that a user does not see other users or groups data.
    This method filters logged in users depending on group roles and permissions.
    Only the superuser can see all users and locations data while a users
    can only see data from registered location within his/her group/system role.
    If a user is not assigned to a group, he/she can only own data - 01/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')

        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            return qs
        # returns data for AFRO and member countries
        elif user in groups and user_location==1:
            qs_admin=db_locations.filter(
                locationlevel__locationlevel_id__gte=1,
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
        db_sevicedomains = StgServiceDomain.objects.all()
        db_sevicesubdomains=db_sevicedomains.exclude(
            parent_id__isnull=True).filter(category=1)

        if request.user.is_superuser:
            if db_field.name == "domain":
                kwargs["queryset"]=db_sevicesubdomains

        if db_field.name == "user":
                kwargs["queryset"] = CustomUser.objects.filter(
                    email=request.user)
        return super().formfield_for_foreignkey(db_field, request,**kwargs)

    #This method removes the add button on the admin interface
    def has_add_permission(self, request, obj=None):
        return False

    def get_import_formats(self):  #This method limits import to CSV, XML and XLSX
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self): #This function returns available export formats.
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

    fieldsets = (
        ('FACILITY DETAILS', {
                'fields':('name','type','location','admin_location','owner',) #afrocode may be null
            }),
        )
    inlines = [FacilityServiceReadinessInline]
    list_display=('name','type','location','admin_location','owner',)
    list_select_related = ('type','owner','location','owner',)
    search_fields = ('name','type__translations__name','status','shortname',
        'code',   'code','location__location__translations__name',
        'owner__translations__name')
    readonly_fields = ('name','type','location','admin_location','owner','user',)
    list_per_page = 50 #limit records displayed on admin site to 50
    list_filter = (
        ('location',RelatedOnlyDropdownFilter),
        ('type',RelatedOnlyDropdownFilter),
        ('owner',RelatedOnlyDropdownFilter),
        ('status',DropdownFilter),
    )



@admin.register(StgFacilityServiceMeasureUnits)
class FacilityServiceProvisionUnitsAdmin (TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    # This method removes the add button on the admin interface
    """
   Serge requested that a user does not see other users or groups data.
    This method filters logged in users depending on group roles and permissions.
    Only the superuser can see all users and locations data while a users
    can only see data from registered location within his/her group/system role.
    If a user is not assigned to a group, he/she can only own data - 01/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')

        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            return qs
        # returns data for AFRO and member countries
        elif user in groups and user_location==1:
            qs_admin=db_locations.filter(
                locationlevel__locationlevel_id__gte=1,
                locationlevel__locationlevel_id__lte=2)
        # return data based on the location of the user logged/request location
        elif user in groups and user_location>1:
            qs=qs.filter(location=user_location)
        return qs
    fieldsets = (
        ('Unit of Service provision', {
                'fields':('name','shortname','description','domain',) #afrocode may be null
            }),
        )
    list_display=('name','code','shortname','domain','description')
    list_select_related = ('domain',)
    list_display_links =('code', 'name',)
    search_fields = ('code','translations__name',) #display search field
    list_per_page = 50 #limit records displayed on admin site to 50
    exclude = ('date_created','date_lastupdated','code',)
    list_filter = (
        ('domain',RelatedOnlyDropdownFilter),
    )



@admin.register(StgFacilityServiceIntervention)
class FacilityServiceInterventionAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    # This method removes the add button on the admin interface
    """
   Serge requested that a user does not see other users or groups data.
    This method filters logged in users depending on group roles and permissions.
    Only the superuser can see all users and locations data while a users
    can only see data from registered location within his/her group/system role.
    If a user is not assigned to a group, he/she can only own data - 01/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')

        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            return qs
        # returns data for AFRO and member countries
        elif user in groups and user_location==1:
            qs_admin=db_locations.filter(
                locationlevel__locationlevel_id__gte=1,
                locationlevel__locationlevel_id__lte=2)
        # return data based on the location of the user logged/request location
        elif user in groups and user_location>1:
            qs=qs.filter(location=user_location)
        return qs
    fieldsets = (
        ('Service Interventions Details', {
                'fields':('name','shortname','description','domain',) #afrocode may be null
            }),
        )
    list_display=('name','code','shortname','description','domain',)
    list_select_related = ('domain',)
    list_display_links =('code', 'name','shortname',)
    search_fields = ('translations__name','translations__shortname','code',) #display search field
    exclude = ('date_created','date_lastupdated','code',)
    list_per_page = 30 #limit records displayed on admin site to 15
    list_filter = (
        ('domain',RelatedOnlyDropdownFilter),
    )


@admin.register(StgFacilityServiceAreas)
class FacilityServiceAreasAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    # This method removes the add button on the admin interface
    """
   Serge requested that a user does not see other users or groups data.
    This method filters logged in users depending on group roles and permissions.
    Only the superuser can see all users and locations data while a users
    can only see data from registered location within his/her group/system role.
    If a user is not assigned to a group, he/she can only own data - 01/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')

        # Returns data for all the locations to the lowest location level
        if request.user.is_superuser:
            return qs
        # returns data for AFRO and member countries
        elif user in groups and user_location==1:
            qs_admin=db_locations.filter(
                locationlevel__locationlevel_id__gte=1,
                locationlevel__locationlevel_id__lte=2)
        # return data based on the location of the user logged/request location
        elif user in groups and user_location>1:
            qs=qs.filter(location=user_location)
        return qs
    fieldsets = (
        ('Service Domain Areas', {
                'fields':('name','shortname','description','intervention',) #afrocode may be null
            }),
        )

    list_display=('name','code','shortname','description','intervention',)
    list_select_related = ('intervention',)
    list_display_links =('code', 'name','shortname',)
    search_fields = ('translations__name','translations__shortname','code',) #display search field
    exclude = ('date_created','date_lastupdated','code',)
    list_per_page = 30 #limit records displayed on admin site to 15
    list_filter = (
        ('intervention',RelatedOnlyDropdownFilter),
    )
