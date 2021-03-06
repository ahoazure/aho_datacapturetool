from django.contrib import admin
from django import forms
from django.conf import settings # allow import of projects settings at the root
from django.forms import BaseInlineFormSet
from parler.admin import (TranslatableAdmin,TranslatableStackedInline,
    TranslatableInlineModelAdmin)
import data_wizard # Solution to data import madness that had refused to go
from itertools import groupby #additional import for managing grouped dropdowm
from indicators.serializers import FactDataIndicatorSerializer
from django.forms.models import ModelChoiceField, ModelChoiceIterator
from .models import (StgIndicatorReference,StgIndicator,StgIndicatorDomain,
    FactDataIndicator,IndicatorProxy,AhoDoamain_Lookup,aho_factsindicator_archive,
    StgNarrative_Type,StgAnalyticsNarrative,StgIndicatorNarrative)
from django.forms import TextInput,Textarea # customize textarea row and column size
from commoninfo.admin import OverideImportExport,OverideExport
from .resources import (IndicatorResourceExport, IndicatorResourceImport,
    AchivedIndicatorResourceExport,DomainResourceExport,IndicatorResourceExport)
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom
from commoninfo.fields import RoundingDecimalFormField # For fixing rounded decimal
from regions.models import StgLocation,StgLocationLevel
from home.models import ( StgDatasource,StgCategoryoption)
from authentication.models import CustomUser, CustomGroup

from import_export.admin import (ImportExportModelAdmin, ExportMixin,
    ImportMixin,ExportActionModelAdmin)
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


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    (self.field.group_label(group), [self.choice(ch) for ch in choices])
                        for group,choices in groupby(self.queryset.all(),
                            key=lambda row: getattr(row, self.field.group_by_field))
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            for group, choices in groupby(self.queryset.all(),
	        key=lambda row: getattr(row, self.field.group_by_field)):
                    yield (self.field.group_label(group),
                        [self.choice(ch) for ch in choices])


class GroupedModelChoiceField(ModelChoiceField):
    def __init__(
        self, group_by_field, group_label=None, cache_choices=False,
        *args, **kwargs):
        """
        group_by_field is the name of a field on the model
        group_label is a function to return a label for each choice group
        """
        super(GroupedModelChoiceField, self).__init__(*args, **kwargs)
        self.group_by_field = group_by_field
        self.cache_choices = cache_choices
        if group_label is None:
            self.group_label = lambda group: group
        else:
            self.group_label = group_label

    def _get_choices(self):
        """
        Exactly as per ModelChoiceField except returns new iterator class
        """
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)
    choices = property(_get_choices, ModelChoiceField._set_choices)


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
    search_fields = ('code','translations__name','translations__shortname',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)


@admin.register(StgIndicator)
class IndicatorAdmin(TranslatableAdmin,OverideExport):
    def sort_data(self, request):
        language_code = settings.LANGUAGE_CODE
        StgIndicator.objects.translated(language_code).order_by('translations__name')
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    fieldsets = (
        ('Primary Attributes', {
                'fields': ('name','shortname','definition','reference') #afrocode may be null
            }),
            ('Secondary Attributes', {
                'fields': ('numerator_description', 'denominator_description',
                'preferred_datasources',),
            }),
        )
    resource_class = IndicatorResourceExport
    list_display=['name','afrocode','shortname','numerator_description',
        'denominator_description','reference',]
    list_display_links = ('afrocode', 'name',) #display as clickable link
    search_fields = ('translations__name','translations__shortname','afrocode') #display search field
    list_per_page = 50 #limit records displayed on admin site to 30
    list_filter = (
        ('reference', RelatedOnlyDropdownFilter),
    )

    class Media:
        exclude = ('date_created','date_lastupdated',) #show only related records


@admin.register(StgIndicatorDomain)
class IndicatorDomainAdmin(TranslatableAdmin,OverideExport):
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
    resource_class = DomainResourceExport
    list_display=['name','code','level','parent',]
    list_display_links = ('code', 'name',)
    search_fields = ('translations__name','translations__shortname','code') #display search field
    list_per_page = 50 #limit records displayed on admin site to 15
    filter_horizontal = ('indicators',) # this should display  inline with multiselect
    exclude = ('date_created','date_lastupdated',)
    list_filter = (
        ('parent',RelatedOnlyDropdownFilter,),
        ('indicators',RelatedOnlyDropdownFilter,),# Added 16/12/2019 for M2M lookup
        ('level',DropdownFilter,),# Added 16/12/2019 for M2M lookup
    )

class IndicatorProxyForm(forms.ModelForm):
    categoryoption = GroupedModelChoiceField(group_by_field='category',
        queryset=StgCategoryoption.objects.all().order_by('category__category_id'),
    )

    '''
    Implemented after overrriding decimal place restriction that facts with >3
    decimal places. The RoundingDecimalFormField is in serializer.py
    '''
    value_received = RoundingDecimalFormField(
        max_digits=20,decimal_places=2,required=False)#changed to false 15/09/20
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
        fields = ('indicator','location', 'categoryoption','datasource',
            'measuremethod','start_period','end_period','period',
            'value_received','string_value')

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
        measuremethod_field = 'measuremethod' #
        measuremethod = cleaned_data.get(measuremethod_field)
        start_year_field = 'start_period'
        start_period = cleaned_data.get(start_year_field)
        end_year_field = 'end_period'
        end_period = cleaned_data.get(end_year_field)

        user_field = 'user' #
        user = cleaned_data.get(user_field)

        # This construct modified on 26/03/2020 to allow new record entry
        if indicator and location and categoryoption and datasource and \
            start_period and end_period:
            if FactDataIndicator.objects.filter(indicator=indicator,
                location=location,datasource=datasource,
                categoryoption=categoryoption,start_period=start_period,
                end_period=end_period).exists():
                """
                pop(key) method removes the specified key and returns the
                corresponding value. Returns error If key does not exist
                """
                cleaned_data.pop(indicator_field)  # is also done by add_error
                cleaned_data.pop(location_field)
                cleaned_data.pop(categoryoption_field)
                cleaned_data.pop(datasource_field) # added line on 21/02/2020
                cleaned_data.pop(measuremethod_field)
                cleaned_data.pop(start_year_field)
                cleaned_data.pop(end_year_field)
                cleaned_data.pop(user_field)

                if end_period < start_period:
                    raise ValidationError({'start_period':_(
                        'Sorry! Ending year cannot be lower than the start year. \
                        Please make corrections')})

        return cleaned_data


# Register fact_data serializer to allow import os semi-structured data Excel/CSV
data_wizard.register(FactDataIndicator)
@admin.register(FactDataIndicator)
class IndicatorFactAdmin(OverideImportExport):
    form = IndicatorProxyForm #overrides the default django model form
    #resource_class = AchivedIndicatorResourceExport
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
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        if db_field.name == "location":
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocation.objects.all().order_by(
                'location_id')
                # Looks up for the location level upto the country level
            elif user in groups:
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__locationlevel_id__gte=1,
                locationlevel__locationlevel_id__lte=2).order_by(
                'location_id')
            else:
                kwargs["queryset"] = StgLocation.objects.filter(
                location_id=request.user.location_id).translated(
                language_code='en')

        if db_field.name == "user":
                kwargs["queryset"] = CustomUser.objects.filter(
                    email=request.user)

        # Restricted permission to data source implememnted on 20/03/2020
        if db_field.name == "datasource":
            if request.user.is_superuser:
                kwargs["queryset"] = StgDatasource.objects.all().order_by(
                'datasource_id')
            elif user in groups:
                kwargs["queryset"] = StgDatasource.objects.all().order_by(
                'datasource_id')
            else:
                kwargs["queryset"] = StgDatasource.objects.filter(pk__gte=2)
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

    def get_export_resource_class(self):
        return IndicatorResourceExport

    def get_import_resource_class(self):
        return IndicatorResourceImport

    readonly_fields = ('indicator', 'location', 'start_period',)
    fieldsets = ( # used to create frameset sections on the data entry form
        ('Indicator Details', {
                'fields': ('indicator','location', 'categoryoption','datasource',
                'measuremethod')
            }),
            ('Reporting Period & Data Values', {
                'fields': ('start_period','end_period','value_received',
                'numerator_value','denominator_value','min_value','max_value',
                'target_value','string_value',),
            }),
            ('Logged Admin/Staff', {
                'fields': ('user',)
            }),
        )
    # The list display includes a callable get_afrocode that returns indicator code for display on admin pages
    list_display=['indicator','location', get_afrocode,'period','categoryoption',
        'value_received','string_value','datasource','get_comment_display',]
    list_display_links = ('location',get_afrocode, 'indicator',) #display as clickable link
    search_fields = ('indicator__translations__name', 'location__translations__name',
        'period','indicator__afrocode') #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
     #this field need to be controlled for data entry. Active for the approving authority
    readonly_fields=('comment',)
    actions =[transition_to_pending, transition_to_approved, transition_to_rejected]
    list_filter = (
        ('location', RelatedOnlyDropdownFilter,),
        ('indicator', RelatedOnlyDropdownFilter,),
        ('period',DropdownFilter),
        ('categoryoption', RelatedOnlyDropdownFilter,),
        ('comment',DropdownFilter),
    )


class LimitModelFormset(BaseInlineFormSet):
    ''' Base Inline formset to limit inline Model records'''
    def __init__(self, *args, **kwargs):
        super(LimitModelFormset, self).__init__(*args, **kwargs)
        instance = kwargs["instance"]
        self.queryset = FactDataIndicator.objects.filter(
            indicator_id=instance).order_by('-date_created')[:5]

# this class define the fact table as a tubular (not columnar) form for ease of entry as requested by Davy Liboko
class FactIndicatorInline(admin.TabularInline):
    form = IndicatorProxyForm #overrides the default django form
    model = FactDataIndicator
    formset = LimitModelFormset
    extra = 2 # Used to control  number of empty rows displayed.

    """
    Davy and Serge requested that the form be restricted to user's country.
    Thus, this function is for filtering location to display country level.
    The location is used to filter the dropdownlist based on the request
    object's USER, If the user has superuser privileges or is a member of
    AFRO-DataAdmins, he/she can enter data for all the AFRO member countries
    otherwise, can only enter data for his/her country.=== modified 02/02/2021
    """
    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        if db_field.name == "location":
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocation.objects.all().order_by(
                'location_id')
                # Looks up for the location level upto the country level
            elif user in groups:
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__locationlevel_id__gte=1,
                locationlevel__locationlevel_id__lte=2).order_by(
                'location_id')
            else:
                kwargs["queryset"] = StgLocation.objects.filter(
                location_id=request.user.location_id).translated(
                language_code='en')

        if db_field.name == "user":
                kwargs["queryset"] = CustomUser.objects.filter(
                    email=request.user)

        # Restricted permission to data source implememnted on 20/03/2020
        if db_field.name == "datasource":
            if request.user.is_superuser:
                kwargs["queryset"] = StgDatasource.objects.all().order_by(
                'datasource_id')
            elif user in groups:
                kwargs["queryset"] = StgDatasource.objects.all().order_by(
                'datasource_id')
            else:
                kwargs["queryset"] = StgDatasource.objects.filter(pk__gte=2)
        return super().formfield_for_foreignkey(db_field, request,**kwargs)

    fields = ('indicator','location','datasource','measuremethod','start_period',
        'end_period','categoryoption','value_received','numerator_value',
        'denominator_value','min_value','max_value','target_value','string_value',
        'user')


@admin.register(IndicatorProxy)
class IndicatorProxyAdmin(TranslatableAdmin):
    #This method removes the add button on the admin interface
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

    inlines = [FactIndicatorInline] #try tabular form
    readonly_fields = ('afrocode', 'name',) # Make it read-only for referential integrity constraunts
    fields = ('afrocode', 'name')
    list_display=['name','afrocode','reference',]
    list_display_links=['afrocode', 'name']
    search_fields = ('afrocode','translations__name', 'translations__shortname',) #display search field
    list_filter = (
        ('translations__name',DropdownFilter),
    )


@admin.register(aho_factsindicator_archive)
class IndicatorFactArchiveAdmin(OverideExport,ExportActionModelAdmin):

    def has_add_permission(self, request): #removes the add button because no data entry is needed
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, extra_context=None):
        ''' Customize add/edit form '''
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(IndicatorFactArchiveAdmin, self).change_view(
            request,object_id,extra_context=extra_context)

    def get_afrocode(obj):
        return obj.indicator.afrocode
    get_afrocode.admin_order_field  = 'indicator__afrocode'  #Lookup to allow column sorting by AFROCODE
    get_afrocode.short_description = 'Indicator Code'  #Renames the column head

    """
    Serge requested that the form for data input be restricted to user's location.
    Thus, this function is for filtering location to display country level.
    The location is used to filter the dropdownlist based on the request
    object's USER, If the user has superuser privileges or is a member of
    AFRO-DataAdmins, he/she can enter data for all the AFRO member countries
    otherwise, can only enter data for his/her country.===modified 02/02/2021
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')
        facts_archive= aho_factsindicator_archive.objects.only(
            'indicator','location','categoryoption','datasource',
            'value_received','period','comment','user')[:2]

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

    resource_class = AchivedIndicatorResourceExport
    list_display=['indicator','location','categoryoption','datasource',
    'value_received','period','comment']
    search_fields = ('indicator__translations__name','location__translations__name',
        'period') #display search field
    list_per_page = 100 #limit records displayed on admin site to 50
    list_filter = (
        ('location', RelatedOnlyDropdownFilter,),
        ('indicator', RelatedOnlyDropdownFilter,),
        ('categoryoption', RelatedOnlyDropdownFilter,),
        ('comment',DropdownFilter),
    )



@admin.register(StgNarrative_Type)
class NarrativeTypeAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    list_display=['name','code','shortname','description',]
    list_display_links =('code','name',)
    search_fields = ('code','translations__name','translations__shortname') #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_lastupdated','code',)


@admin.register(StgAnalyticsNarrative)
class AnalyticsNarrativeAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    list_display=['narrative_type','location','domain','narrative_text']
    list_display_links =('narrative_type','domain')
    search_fields = ('code','location__translations__name',
        'domain__translations__name') #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_lastupdated','code',)
    list_filter = (
      ('location',RelatedOnlyDropdownFilter),
    )
    exclude = ('date_lastupdated','code',)

@admin.register(StgIndicatorNarrative)
class IndicatorNarrativeAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    list_display=['narrative_type','code','location','indicator','narrative_text',]
    list_display_links =('code',)
    search_fields = ('code','location__translations__name',
        'indicator__translations__name') #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_lastupdated','code',)
    list_filter = (
      ('location',RelatedOnlyDropdownFilter),
    )


@admin.register(AhoDoamain_Lookup)
class AhoDoamain_LookupAdmin(OverideExport):
    def has_delete_permission(self, request, obj=None): # Removes the add button on the admin interface
        return False

    def has_add_permission(self, request, obj=None): # Removes the add button on the admin interface
        return False

    #This method removes the save buttons from the model form
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(AhoDoamain_LookupAdmin, self).changeform_view(
            request, object_id, extra_context=extra_context)

    list_display=('indicator_name','code','domain_name', 'domain_level',)
    list_display_links = None # make the link for change object non-clickable
    readonly_fields = ('indicator_name','code','domain_name', 'domain_level',)
    search_fields = ('indicator_name','code','domain_name', 'domain_level',)
    ordering = ('indicator_name',)
    list_filter = (
        ('domain_name', DropdownFilter,),
    )
    ordering = ('indicator_name',)
