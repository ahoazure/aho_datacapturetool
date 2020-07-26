from django.contrib import admin
from django import forms
from django.conf import settings # allow import of projects settings at the root
from django.forms import BaseInlineFormSet
from parler.admin import TranslatableAdmin
from .models import (StgIndicatorReference,StgIndicator,StgIndicatorDomain,
    FactDataIndicator,IndicatorProxy,)
from django.forms import TextInput,Textarea # customize textarea row and column size
from commoninfo.admin import OverideImportExport,OverideExport
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom
from commoninfo.fields import RoundingDecimalFormField # For fixing rounded decimal
from regions.models import StgLocation,StgLocationLevel
from home.models import ( StgDatasource,)

#The following 3 functions are used to register global actions performed on the data. See action listbox
def transition_to_pending (modeladmin, request, queryset):
    queryset.update(comment = 'pending')
transition_to_pending.short_description = "Mark selected as Pending"

def transition_to_approved (modeladmin, request, queryset):
    queryset.update (comment = 'approved')
transition_to_approved.short_description = "Mark selected as Approved"

def transition_to_rejected (modeladmin, request, queryset):
    queryset.update (comment = 'rejected')
transition_to_rejected.short_description = "Mark selected as Rejected"


@admin.register(StgIndicatorReference)
class IndicatorRefAdmin(TranslatableAdmin):

    def sort_data(self, request):
        language_code = settings.LANGUAGE_CODE
        StgIndicatorReference.objects.translated(language_code).order_by('translations__code')

    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    fieldsets = (
        ('Reference Attributes', {
                'fields': ('name','shortname',)
            }),
            ('Description', {
                'fields': ('description',),
            }),
        )
    list_display=['name','code','shortname','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('code','name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)


@admin.register(StgIndicator)
class IndicatorAdmin(TranslatableAdmin): #add export action to facilitate export od selected fields
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    fieldsets = (
        ('Primary Attributes', {
                'fields': ('name','shortname', 'gen_code','definition','reference') #afrocode may be null
            }),
            ('Secondary Attributes', {
                'fields': ('numerator_description', 'denominator_description',
                'preferred_datasources','measuremethod',),
            }),
        )
#    resource_class = ResourceResourceExport
    list_display=['name','afrocode','shortname','measuremethod']
    list_display_links = ('afrocode', 'name',) #display as clickable link
    search_fields = ('name', 'afrocode') #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
    list_filter = (
        ('reference', RelatedOnlyDropdownFilter),
        ('measuremethod', RelatedOnlyDropdownFilter),
    )

    class Media:
        exclude = ('date_created','date_lastupdated',) #show only related records


@admin.register(StgIndicatorDomain)
class IndicatorDomainAdmin(TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    fieldsets = (
        ('Domain Attributes', {
                'fields': ('name', 'shortname','parent','level') #afrocode may be null
            }),
            ('Domain Description', {
                'fields': ('description','indicators'),
            }),
        )
    # resource_class = DomainResourceExport
    list_display=['name','code','parent','level']
    list_display_links = ('code', 'name',)
    search_fields = ('name','shortname','code') #display search field
    list_per_page = 50 #limit records displayed on admin site to 15
    filter_horizontal = ('indicators',) # this should display  inline with multiselect
    exclude = ('date_created','date_lastupdated',)
    list_filter = (
        ('parent',RelatedOnlyDropdownFilter,),
        ('indicators',RelatedOnlyDropdownFilter,),# Added 16/12/2019 for M2M lookup
        ('translations__level',DropdownFilter,),# Added 16/12/2019 for M2M lookup
    )

class IndicatorProxyForm(forms.ModelForm):
    # categoryoption = GroupedModelChoiceField(group_by_field='category',
    #     #This queryset was modified by Daniel to order the grouped list by  date created
    #     queryset=StgCategoryoption.objects.all().order_by('category__category_id'),
    # )
    '''
    Implemented after overrriding decimal place restriction that facts with >3
    decimal places. The RoundingDecimalFormField is in serializer.py
    '''
    value_received = RoundingDecimalFormField(
        max_digits=20,decimal_places=2,required=True)
    min_value = RoundingDecimalFormField(
        max_digits=20,decimal_places=2,required=False)
    max_value = RoundingDecimalFormField(
        max_digits=20,decimal_places=2,required=False)
    target_value = RoundingDecimalFormField(
        max_digits=20,decimal_places=2,required=False)
    numerator_value = RoundingDecimalFormField(
        max_digits=20,decimal_places=2,required=False)
    denominator_value = RoundingDecimalFormField(
        max_digits=20,decimal_places=2,required=False)

    class Meta:
        fields = ('indicator','location', 'categoryoption','datasource','start_period',
            'end_period','period','value_received')
        model = FactDataIndicator

    def clean(self):
        cleaned_data = super().clean()
        indicator_field = 'indicator'
        indicator = cleaned_data.get(indicator_field)
        location_field = 'location'
        location = cleaned_data.get(location_field)
        categoryoption_field = 'categoryoption'
        categoryoption = cleaned_data.get(categoryoption_field)
        #This attribute was added after getting error- location cannot be null
        datasource_field = 'datasource' #
        datasource = cleaned_data.get(datasource_field)
        start_year_field = 'start_period'
        start_period = cleaned_data.get(start_year_field)
        end_year_field = 'end_period'
        end_period = cleaned_data.get(end_year_field)

        # This construct modified on 26/03/2020 to allow new record entry
        if indicator and location and categoryoption and start_period and end_period:
            if FactDataIndicator.objects.filter(indicator=indicator,
                location=location,datasource=datasource,categoryoption=categoryoption,
                start_period=start_period,end_period=end_period).exists():
                """
                pop(key) method removes the specified key and returns the
                corresponding value. Returns error If key does not exist
                """
                cleaned_data.pop(indicator_field)  # is also done by add_error
                cleaned_data.pop(location_field)
                cleaned_data.pop(categoryoption_field)
                cleaned_data.pop(datasource_field) # added line on 21/02/2020
                cleaned_data.pop(start_year_field)
                cleaned_data.pop(end_year_field)

                if end_period < start_period:
                    raise ValidationError({'start_period':_(
                        'Sorry! Ending year cannot be lower than the start year. \
                        Please make corrections')})

        return cleaned_data


# Register fact_data serializer to allow import os semi-structured data Excel/CSV
@admin.register(FactDataIndicator)
class IndicatorFactAdmin(OverideImportExport):
    form = IndicatorProxyForm #overrides the default django model form
    #resource_class = AchivedIndicatorResourceExport
    """
    Davy requested that a user does not see other countries data. This function
    does exactly that by filtering location based on logged in user. For this
    reason only the country of the loggied in user is displayed whereas the
    superuser has access to all the countries. Thanks Good for
    https://docs.djangoproject.com/en/2.2/ref/contrib/admin/
    because is gave the exact logic of achiving this non-functional requirement
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        #This works like charm!! only superusers and AFRO admin staff are allowed to view all countries and data
        if request.user.is_superuser or request.user.groups.filter(
            name__icontains='Admins'):
            return qs #provide access to all instances/rows of fact data indicators
        return qs.filter(location=request.user.location)  #provide access to user's country indicator instances

    """
    Davy requested that the form for data input be restricted to the user's country.
    Thus, this function is for filtering location to display country level.
    The location is used to filter the dropdownlist based on the request
    object's USER, If the user has superuser privileges or is a member of
    AFRO-DataAdmins, he/she can enter data for all the AFRO member countries
    otherwise, can only enter data for his/her country.The order_by('locationlevel',
    'location_id') clause make sure that the regional offices are first displayed
    in ascending order
    """
    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        if db_field.name == "location":# Implements user filtering
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocation.objects.filter(
                pk__gte=1).order_by('location_id')
            elif request.user.groups.filter(name__icontains='Admin'):
                kwargs["queryset"] = StgLocation.objects.filter(
                pk__gte=1).order_by('location_id')
            else:
                kwargs["queryset"] = StgLocation.objects.filter(
                    location_id=request.user.location_id)

        # Restricted permission to data source implememnted on 20/03/2020
        if db_field.name == "datasource":
            if request.user.is_superuser:
                kwargs["queryset"] = StgDatasource.objects.all()
            elif request.user.groups.filter(name__icontains='Admin'):
                kwargs["queryset"] = StgDatasource.objects.exclude(
                pk__gte=1) # Admin user can only access data from countries
            else:
                kwargs["queryset"] = StgDatasource.objects.filter(pk=1)
        return super().formfield_for_foreignkey(db_field, request,**kwargs)

    # #This function is used to get the afrocode from related indicator model for use in list_display
    def get_afrocode(obj):
        return obj.indicator.afrocode
    get_afrocode.admin_order_field  = 'indicator__afrocode'  #Lookup to allow column sorting by AFROCODE
    get_afrocode.short_description = 'Indicator Code'  #Renames the column head

    def get_actions(self, request):
        actions = super(IndicatorFactAdmin, self).get_actions(request)
        if not request.user.has_perm('indicators.approve_factdataindicator'):
           actions.pop('transition_to_approved', None)
        if not request.user.has_perm('indicators.reject_factdataindicator'):
            actions.pop('transition_to_rejected', None)
        if not request.user.has_perm('indicators.delete_factdataindicator'):
            actions.pop('delete_selected', None)
        return actions
    #
    # def get_export_resource_class(self):
    #     return IndicatorResourceExport
    #
    # def get_import_resource_class(self):
    #     return IndicatorResourceImport

    readonly_fields = ('indicator', 'location', 'start_period',)
    fieldsets = ( # used to create frameset sections on the data entry form
        ('Indicator Details', {
                'fields': ('indicator','location', 'categoryoption','datasource',
                'valuetype')
            }),
            ('Reporting Period & Values', {
                'fields': ('start_period','end_period','value_received','numerator_value',
                'denominator_value','min_value','max_value','target_value','string_value',),
            }),
        )
    # The list display includes a callable get_afrocode that returns indicator code for display on admin pages
    list_display=['location', 'indicator',get_afrocode,'period','categoryoption',
        'value_received','datasource','get_comment_display',]
    list_display_links = ('location',get_afrocode, 'indicator',) #display as clickable link
    search_fields = ('indicator__name', 'location__name','period','indicator__afrocode') #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
     #this field need to be controlled for data entry. Active for the approving authority
    readonly_fields=('comment',)
    actions =[transition_to_pending, transition_to_approved, transition_to_rejected]
    list_filter = (
        ('location', RelatedOnlyDropdownFilter,),
        ('categoryoption', RelatedOnlyDropdownFilter,),
        ('period',DropdownFilter),
        ('indicator', RelatedOnlyDropdownFilter,),
    )
class LimitModelFormset(BaseInlineFormSet):
    ''' Base Inline formset to limit inline Model records'''
    def __init__(self, *args, **kwargs):
        super(LimitModelFormset, self).__init__(*args, **kwargs)
        instance = kwargs["instance"]
        self.queryset = FactDataIndicator.objects.filter(
            indicator_id=instance).order_by('-date_created')[:2]

# this class define the fact table as a tubular (not columnar) form for ease of entry as requested by Davy Liboko
class FactIndicatorInline(admin.TabularInline):
    form = IndicatorProxyForm #overrides the default django form
    model = FactDataIndicator
    extra = 2 # Used to control  number of empty rows displayed.
    formset = LimitModelFormset

    """
    Davy requested that the form input be restricted to the user's country.
    Thus, this function is for filtering location to display country level.
    The location is used to fielter the dropdownlist based on the request
    object's USER, If the user is superuser, he/she can enter data for all the
    AFRO member countries otherwise, can only enter data for his/her country.
    """
    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        if db_field.name == "location":
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__name__in =['Regional','Country']).order_by(
                    'locationlevel', 'location_id') #superuser can access all countries at level 2 in the database
            elif request.user.groups.filter(name__icontains='Admin'):
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__name__in =['Regional','Country']).order_by(
                    'locationlevel', 'location_id')
            else:
                kwargs["queryset"] = StgLocation.objects.filter(
                    location_id=request.user.location_id) #permissions for user country filter---works as per Davy's request

    # This is a new construct created upon request by Davy to restrict data source access
        if db_field.name == "datasource":# Restricted data source implememnted on 20/03/2020
            if request.user.is_superuser:
                #superuser can access all countries at level 2 in the database
                kwargs["queryset"] = StgDatasource.objects.all()
            elif request.user.groups.filter(name__icontains='Admin'):
                kwargs["queryset"] = StgDatasource.objects.exclude(datasource_id=1)
            else:
                kwargs["queryset"] = StgDatasource.objects.filter(datasource_id=1)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fields = ('indicator','location','datasource','valuetype','start_period',
        'end_period','categoryoption','value_received','numerator_value',
        'denominator_value','min_value','max_value','target_value','string_value',)


@admin.register(IndicatorProxy)
class IndicatorProxy(TranslatableAdmin):
    #This method removes the add button on the admin interface
    def has_add_permission(self, request, obj=None):
        return False

    #resource_class = IndicatorResourceExport #added to customize fields displayed on the import window
    inlines = [FactIndicatorInline] #try tabular form
    readonly_fields = ('afrocode', 'name',) # Make it read-only for referential integrity constraunts
    fields = ('afrocode', 'name')
    list_display=['name','afrocode','reference',]
    list_display_links=['afrocode', 'name']
    search_fields = ('afrocode','name', 'shortname',) #display search field
    list_filter = (
        ('translations__name',DropdownFilter),
    )

# @admin.register(aho_factsindicator_archive)
# class IndicatorFactArchiveAdmin(TranslatableAdmin):
#     def has_add_permission(self, request): #removes the add button because no data entry is needed
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def get_afrocode(obj):
#         return obj.indicator.afrocode
#     get_afrocode.admin_order_field  = 'indicator__afrocode'  #Lookup to allow column sorting by AFROCODE
#     get_afrocode.short_description = 'Indicator Code'  #Renames the column head
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         # Only superusers and admin are allowed to view all countries data
#         if request.user.is_superuser or request.user.groups.filter(
#             name__icontains='Admins'):
#             return qs #provide access to all instances/rows of fact data indicators
#         return qs.filter(location=request.user.location)  #provide access to user's country indicator instances
#
#     resource_class = AchivedIndicatorResourceExport
#     list_display=['location', 'indicator',get_afrocode,'period','categoryoption',
#         'value_received','target_value','string_value','get_comment_display',]
#     search_fields = ('indicator__name', 'location__name','period',
#         'indicator__afrocode') #display search field
#     list_per_page = 50 #limit records displayed on admin site to 50



# @admin.register(StgNarrative_Type)
# class NarrativeTypeAdmin(TranslatableAdmin):
#     from django.db import models
#     formfield_overrides = {
#         models.CharField: {'widget': TextInput(attrs={'size':'100'})},
#         models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
#     }
#
#     list_display=['name','code','shortname','description',]
#     list_display_links =('code','name',)
#     search_fields = ('code','name','shortname') #display search field
#     list_per_page = 30 #limit records displayed on admin site to 15
#     exclude = ('date_lastupdated','code',)
#
#
# @admin.register(StgAnalyticsNarrative)
# class AnalyticsNarrativeAdmin(TranslatableAdmin):
#     from django.db import models
#     formfield_overrides = {
#         models.CharField: {'widget': TextInput(attrs={'size':'100'})},
#         models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
#     }
#
#     list_display=['narrative_type','location','domain','narrative_text']
#     list_display_links =('narrative_type','domain')
#     search_fields = ('code','location__name','domain__name') #display search field
#     list_per_page = 30 #limit records displayed on admin site to 15
#     exclude = ('date_lastupdated','code',)
#     list_filter = (
#       ('location',RelatedOnlyDropdownFilter),
#     )
#     exclude = ('date_lastupdated','code',)
#
#
# @admin.register(AhoDoamain_Lookup)
# class AhoDoamain_LookupAdmin(OverideExport):
#     def has_delete_permission(self, request, obj=None): # Removes the add button on the admin interface
#         return False
#
#     def has_add_permission(self, request, obj=None): # Removes the add button on the admin interface
#         return False
#
#     #This method removes the save buttons from the model form
#     def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
#         extra_context = extra_context or {}
#         extra_context['show_save_and_continue'] = False
#         extra_context['show_save'] = False
#         return super(AhoDoamain_LookupAdmin, self).changeform_view(
#             request, object_id, extra_context=extra_context)
#
#     list_display=('indicator_name','code','domain_name', 'domain_level',)
#     list_display_links = None # make the link for change object non-clickable
#     readonly_fields = ('indicator_name','code','domain_name', 'domain_level',)
#     search_fields = ('indicator_name','code','domain_name', 'domain_level',)
#     ordering = ('indicator_name',)
#     list_filter = (
#         ('domain_name', DropdownFilter,),
#     )
#     ordering = ('indicator_name',)


# @admin.register(StgIndicatorNarrative)
# class IndicatorNarrativeAdmin(OverideExport):
#     from django.db import models
#     formfield_overrides = {
#         models.CharField: {'widget': TextInput(attrs={'size':'100'})},
#         models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
#     }
#
#     list_display=['code','narrative_type','location','indicator',
#     'narrative_text',]
#     list_display_links =('code',)
#     search_fields = ('code','location__name','indicator__name') #display search field
#     list_per_page = 30 #limit records displayed on admin site to 15
#     exclude = ('date_lastupdated','code',)
#     list_filter = (
#       ('location',RelatedOnlyDropdownFilter),
#     )
