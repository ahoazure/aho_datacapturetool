from django.contrib import admin
from django import forms
from itertools import groupby #additional import for grouped desaggregation options
from parler.admin import TranslatableAdmin
from django.forms import TextInput,Textarea
from django.forms.models import ModelChoiceField, ModelChoiceIterator
from django.contrib.auth.decorators import permission_required #for approval actions
from .models import (StgDataElement,DataElementProxy,StgDataElementGroup,
    FactDataElement,)
from regions.models import StgLocation
from commoninfo.admin import OverideImportExport, OverideExport
from commoninfo.fields import RoundingDecimalFormField # For fixing rounded decimal
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom

#the following 3 functions are used to register global actions performed on the data. See actions listbox
def transition_to_pending (modeladmin, request, queryset):
    queryset.update(comment = 'pending')
transition_to_pending.short_description = "Mark selected as Pending"

def transition_to_approved (modeladmin, request, queryset):
    queryset.update (comment = 'approved')
transition_to_approved.short_description = "Mark selected as Approved"

def transition_to_rejected (modeladmin, request, queryset):
    queryset.update (comment = 'rejected')
transition_to_rejected.short_description = "Mark selected as Rejected"


@admin.register(StgDataElement)
class DataElementAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
        ('Primary Attributes', {
                'fields': ('name','shortname', 'description')
            }),
            ('Secondary Attributes', {
                'fields': ('measuremethod','aggregation_type',),
            }),
        )
    # Added to customize fields displayed on the import window
    # resource_class = DataElementExport
    list_display=['name','code','shortname','description',]
    list_display_links = ('code', 'name',)

    search_fields = ('name','code','shortname',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
    exclude = ('date_created','date_lastupdated',)

class DataElementProxyForm(forms.ModelForm):
    # categoryoption = GroupedModelChoiceField(group_by_field='category',
    #     queryset=StgCategoryoption.objects.all().order_by(
    #         'category__category_id'),
    # )
    # Overrride decimal place restriction that rejects number with >3 d.places
    value = RoundingDecimalFormField(max_digits=20,decimal_places=2)
    target_value = RoundingDecimalFormField(
        max_digits=20,decimal_places=2,required=False)

    class Meta:
        model = FactDataElement
        fields = ('dataelement','location','period', 'categoryoption',
            'datasource','start_year', 'end_year','value', 'comment',)

    def clean(self):
        cleaned_data = super().clean()

        dataelement_field = 'dataelement'
        dataelement = cleaned_data.get(dataelement_field)

        location_field = 'location'
        location = cleaned_data.get(location_field)

        categoryoption_field = 'categoryoption'
        categoryoption = cleaned_data.get(categoryoption_field)

        start_year_field = 'start_year'
        start_year = cleaned_data.get(start_year_field)

        end_year_field = 'end_year'
        end_year = cleaned_data.get(end_year_field)

        if dataelement and location and categoryoption and start_year and end_year:
            # if FactDataElement.objects.filter(dataelement=dataelement,
            #     location=location, categoryoption=categoryoption,
            #     start_year=start_year,end_year=end_year).exists():

                """ pop(key) method removes the specified key and returns the \
                corresponding value. Returns error If key does not exist"""
                cleaned_data.pop(dataelement_field)  # is also done by add_error
                cleaned_data.pop(location_field)
                cleaned_data.pop(categoryoption_field)
                cleaned_data.pop(start_year_field)
                cleaned_data.pop(end_year_field)

                if end_year < start_year:
                    raise ValidationError({'start_year':_(
                        'Sorry! Ending year cannot be lower than the start year. \
                        Please make corrections')})

        return cleaned_data

# Register fact_data indicator to allow wizard driven import
# data_wizard.register(
#     "Import Data Element Records",FactDataElementSerializer)
@admin.register(FactDataElement)
class DataElementFactAdmin(OverideImportExport):
    form = DataElementProxyForm #overrides the default django form

    """
    Davy requested that a user does not see other countries data. This function
    does exactly that by filtering location based on logged in user. For this
    reason only the country of the loggied in user is displayed whereas the
    superuser has access to all the countries. Thanks to
    https://docs.djangoproject.com/en/2.2/ref/contrib/admin/
    because it gave the exact logic of achiving this non-functional requirement
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name__icontains='Admins'):
            return qs #provide access to all instances/rows of fact data elements
        return qs.filter(location=request.user.location) #provide access to user's country instances of data elements

    """
    Davy requested that the form for data input be restricted to the user's country.
    Thus, this function is for filtering location to display country level.
    The location is used to fielter the dropdownlist based on the request object's
    USER, If the user is superuser, he/she can enter data for all AFRO member countries
    otherwise, can only enter data for his/her country.
    """
    def formfield_for_foreignkey(self, db_field, request =None, **kwargs): #to implement user filtering her
        if db_field.name == "location":
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocation.objects.filter(
                pk__gte=1).order_by('location_id')
            elif request.user.groups.filter(name__icontains='Admin'):
                kwargs["queryset"] = StgLocation.objects.filter(
                pk__gt=1).order_by('location_id')
            else:
                kwargs["queryset"] = StgLocation.objects.filter(
                    location_id=request.user.location_id) #permissions for user country filter---works as per Davy's request
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    #This function is used to get the afrocode from related indicator model for use in list_display
    def get_afrocode(obj):
        return obj.dataelement.code
    get_afrocode.admin_order_field  = 'dataelement__code'  #Lookup to allow column sorting by AFROCODE
    get_afrocode.short_description = 'Data Element Code'  #Renames column head

    #The following function returns available export formats.
    def get_export_formats(self):
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

    def get_import_formats(self):
        """
        Returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_actions(self, request):
        actions = super(DataElementFactAdmin, self).get_actions(request)
        if not request.user.has_perm('indicators.approve_factdataindicator'):
           actions.pop('transition_to_approved', None)
        if not request.user.has_perm('indicators.reject_factdataindicator'):
            actions.pop('transition_to_rejected', None)
        if not request.user.has_perm('indicators.delete_factdataindicator'):
            actions.pop('delete_selected', None)
        return actions

    # def get_export_resource_class(self):
    #     return FactDataResourceExport
    #
    # def get_import_resource_class(self):
    #     return FactDataResourceImport


    fieldsets = ( # used to create frameset sections on the data entry form
        ('Data Element Details', {
                'fields': ('dataelement', 'location', 'categoryoption',
                    'datasource','valuetype',)
            }),
            ('Reporting Period & Value', {
                'fields': ('start_year', 'end_year','value','target_value'),
            }),
        )
    #The list display includes a callable get_afrocode that returns data element code for display on admin pages
    list_display=['dataelement','location',get_afrocode,'categoryoption','period',
        'value','datasource','get_comment_display',]
    list_display_links = ('dataelement','location', get_afrocode,) #For making the code and name clickable
    search_fields = ('dataelement__name','location__name','period','dataelement__code') #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
    #this field need to be controlled for data entry. should only be active for the approving authority
    list_filter = (
        ('location', RelatedOnlyDropdownFilter,),
        ('categoryoption', RelatedOnlyDropdownFilter,),
        ('period',DropdownFilter),
        ('dataelement', RelatedOnlyDropdownFilter,)
    )
    readonly_fields=('comment', 'period', )
    actions = [transition_to_pending, transition_to_approved, transition_to_rejected]

# this class define the fact table as a tubular (not columnar) form for ease of entry as requested by Davy Liboko
class FactElementInline(admin.TabularInline):
    form = DataElementProxyForm #overrides the default django form
    model = FactDataElement
    # Very useful in controlling the number of empty rows displayed.In this case zero is Ok for insertion or changes
    extra = 1

    """
    This function is for filtering location to display country level. the database
    field must be parentid for the dropdown list    Note the use of
    locationlevel__name__in as helper for the name lookup while(__in)suffix is
    a special case that works with tuples in Python.
    """
    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        if db_field.name == "location":
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__name__in =['Regional','Country']).order_by(
                    'locationlevel', 'location_id') #superuser can access all countries
            # This works like charm!! only AFRO admin staff are allowed to process all countries and data
            elif request.user.groups.filter(name__icontains='Admins'):
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__name__in =['Regional','Country']).order_by(
                    'locationlevel', 'location_id')
            else:
                kwargs["queryset"] = StgLocation.objects.filter(location_id=request.user.location_id) #permissions for user country filter---works as per Davy's request
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fields = ('dataelement','location','datasource', 'valuetype',
        'categoryoption','start_year', 'end_year','value',)


@admin.register(DataElementProxy)
class DataElementProxyAdmin(TranslatableAdmin):
    def has_add_permission(self, request, obj=None): #This function removes the add button on the admin interface
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
    #list_display_links = ('code', 'name',)
    # resource_class = FactDataResourceExport #added to customize fields displayed on the import window
    #list_display_links = ('code', 'name',)
    inlines = [FactElementInline] # Use tabular form within the data element modelform

    fields = ('code', 'name')
    list_display=['name','code','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('code','name',) #display search field
    readonly_fields = ('code','name','description',)



@admin.register(StgDataElementGroup)
class DataElementGoupAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    field = ('name','shortname', 'description',) # used to create frameset sections on the data entry form
    list_display=['name','code','shortname', 'description',]
    filter_horizontal = ('dataelement',) # this should display an inline with multiselect
    exclude = ('code',)
