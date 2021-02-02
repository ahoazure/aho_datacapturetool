from django.contrib import admin
import data_wizard # Solution to data import madness that had refused to go
from django.forms import TextInput,Textarea #
from django.utils.html import format_html
from import_export.formats import base_formats
from parler.admin import TranslatableAdmin
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom
from import_export.admin import (ImportExportModelAdmin, ExportMixin,
    ImportExportActionModelAdmin)
from commoninfo.admin import OverideImportExport,OverideExport,OverideImport
from .models import (ResourceTypeProxy,HumanWorkforceResourceProxy,
    StgInstitutionType,StgTrainingInstitution,StgHealthWorkforceFacts,
    StgHealthCadre,StgInstitutionProgrammes,StgRecurringEvent,StgAnnouncements)
from facilities.models import (StgHealthFacility,)
from regions.models import StgLocation
from home.models import StgDatasource

#Methods used to register global actions performed on data. See actions listbox
def transition_to_pending (modeladmin, request, queryset):
    queryset.update(status = 'pending')
transition_to_pending.short_description = "Mark selected as Pending"

def transition_to_approved (modeladmin, request, queryset):
    queryset.update (status = 'approved')
transition_to_approved.short_description = "Mark selected as Approved"

def transition_to_rejected (modeladmin, request, queryset):
    queryset.update (status = 'rejected')
transition_to_rejected.short_description = "Mark selected as Rejected"


@admin.register(ResourceTypeProxy)
class ResourceTypeAdmin(TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    list_display=['name','code','description',]
    list_display_links =('code', 'name',)
    search_fields = ('code','translations__name',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


@admin.register(StgInstitutionType)
class InsitutionTypeAdmin(TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    list_display=['name','code','shortname','description']
    list_display_links =('code', 'name','shortname')
    search_fields = ('code','translations__name','translations__shortname') #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


@admin.register(StgInstitutionProgrammes)
class ProgrammesAdmin(TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    list_display=['name','code','description']
    list_display_links =('code', 'name',)
    search_fields = ('code','translations__name',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


@admin.register(HumanWorkforceResourceProxy)
class ResourceAdmin(TranslatableAdmin,ImportExportModelAdmin,
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

    #to make URl clickable, I changed show_url to just url in the list_display tuple
    def show_external_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.external_url)

    def show_url(self, obj):
        return obj.url if obj.url else 'None'

    show_external_url.allow_tags = True
    show_external_url.short_description= 'External File Link'

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

     #This function is used to register permissions for approvals. See signals,py
    def get_actions(self, request):
        actions = super(ResourceAdmin, self).get_actions(request)
        if not request.user.has_perm('resources.approve_stgknowledgeproduct'):
           actions.pop('transition_to_approved', None)
        if not request.user.has_perm('resources.reject_stgknowledgeproduct'):
            actions.pop('transition_to_rejected', None)
        if not request.user.has_perm('resources.delete_stgknowledgeproduct'):
            actions.pop('delete_selected', None)
        return actions

    def get_export_resource_class(self):
        return StgKnowledgeProductResourceExport

    def get_import_resource_class(self):
        return StgKnowledgeProductResourceImport

    fieldsets = (
        ('Publication Attributes', {
                'fields':('title','type','categorization','location',) #afrocode may be null
            }),
            ('Description & Abstract', {
                'fields': ('description', 'abstract',),
            }),
            ('Attribution & Access Details', {
                'fields': ('author','year_published','internal_url',
                    'external_url','cover_image',),
            }),
        )

    def get_location(obj):
           return obj.location.name
    get_location.short_description = 'Location'

    def get_type(obj):
           return obj.type.name
    get_type.short_description = 'Type'

    # To display the choice field values use the helper method get_foo_display where foo is the field name
    list_display=['title','code','author',get_type,get_location,'year_published',
        'internal_url','show_external_url','cover_image','get_comment_display']
    list_display_links = ['code','title',]
    readonly_fields = ('comment',)
    search_fields = ('translations__title','type__translations__name',
        'location__translations__name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
    actions = [transition_to_pending,transition_to_approved,
        transition_to_rejected]
    exclude = ('date_created','date_lastupdated','code',)
    list_filter = (
        ('location',RelatedOnlyDropdownFilter),
        ('type',RelatedOnlyDropdownFilter),
    )


@admin.register(StgTrainingInstitution)
class TrainingInsitutionAdmin(TranslatableAdmin,OverideExport):
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

    # #This function is for filtering location to display regional level only. The database field must be parentid for the dropdown list
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

    fieldsets = (
        ('Institution Details',{
                'fields': (
                    'name', 'type','accreditation','accreditation_info','regulator')
            }),

            ('Contact Details', {
                'fields': ('location','address','posta','email','phone_number',
                'url', 'latitude','longitude'),
            }),
            ('Academic Details', {
                'fields': ( 'faculty','language','programmes',),
            }),
        )

    filter_horizontal = ('programmes',) # this should display  inline with multiselect
    list_display=['name','type','code','location','url','email']
    list_display_links = ('code', 'name',) #display as clickable link
    search_fields = ('location__translations__name','translations__name',
        'type__translations__name') #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)
    list_filter = (
        ('location',RelatedOnlyDropdownFilter),
        ('type',RelatedOnlyDropdownFilter),
    )


@admin.register(StgHealthCadre)
class HealthCadreAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    fieldsets = (
        ('Occulation/Cadre Details',{
                'fields': (
                    'name', 'shortname','code','description','academic','parent')
            }),
    )
    list_display=['name','code','shortname','description','academic','parent']
    list_display_links = ('code', 'shortname','name',) #display as clickable link
    search_fields = ('code','translations__name', 'translations__shortname',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)
    list_filter = (
        ('code',DropdownFilter),
    )


data_wizard.register(StgHealthWorkforceFacts)
@admin.register(StgHealthWorkforceFacts)
class HealthworforceFactsAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    def get_actions(self, request):
        actions = super(HealthworforceFactsAdmin, self).get_actions(request)
        if not request.user.has_perm('health_workforce.approve_stghealthworkforcefacts'):
           actions.pop('transition_to_approved', None)
        if not request.user.has_perm('health_workforce.reject_stghealthworkforcefacts'):
            actions.pop('transition_to_rejected', None)
        if not request.user.has_perm('health_workforce.delete_stghealthworkforcefacts'):
            actions.pop('delete_selected', None)
        return actions

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

        # Restricted permission to data source implememnted on 20/03/2020
        if db_field.name == "datasource":
            if request.user.is_superuser or request.user.groups.filter(
                name__icontains='Admin' or request.user.location>=1):
                kwargs["queryset"] = StgDatasource.objects.all()
            else:
                kwargs["queryset"] = StgDatasource.objects.filter(pk__gte=2)
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

    fieldsets = (
        ('Health Occulation/Cadre Data',{
                'fields': (
                    'cadre_id', 'location','categoryoption','datasource',)
            }),
            ('Reporting Period & Values', {
                'fields':('start_year','end_year','measuremethod','value',
            )
            }),
    )
    actions =[transition_to_pending, transition_to_approved, transition_to_rejected]
    list_display=['location','cadre_id','categoryoption','period','value','status']
    list_display_links = ('cadre_id', 'location',) #display as clickable link
    search_fields = ('location__translations__name','cadre_id__translations__name',
        'period') #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)
    list_filter = (
        ('cadre_id',RelatedOnlyDropdownFilter),
        ('location', RelatedOnlyDropdownFilter,),
        ('period',DropdownFilter),
        ('status',DropdownFilter),
        ('categoryoption', RelatedOnlyDropdownFilter,),
    )


@admin.register(StgRecurringEvent)
class RecurringEventsAdmin(TranslatableAdmin,ImportExportModelAdmin,OverideImport,
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
    #to make URl clickable, I changed show_url to just url in the list_display tuple
    def show_external_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.external_url)

    def show_url(self, obj):
        return obj.url if obj.url else 'None'

    show_external_url.allow_tags = True
    show_external_url.short_description= 'Web Link (URL)'


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

    fieldsets = (
        ('Event Details', {
                'fields':('name','shortname','theme','start_year',
                'end_year','status') #afrocode may be null
            }),
            ('Target Focus and Location', {
                'fields': ('location', 'cadre_id',),
            }),
            ('Files and Web Resources', {
                'fields': ('internal_url','external_url','cover_image'),
            }),
        )
    filter_horizontal = ['cadre_id'] # this should display multiselect boxes
    list_display=['name','code','shortname','theme','period','internal_url',
        'show_external_url']
    list_display_links = ['name','code']
    search_fields = ('name','shortname','location__name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
    exclude = ('date_created','date_lastupdated','code',)
    list_filter = (
        ('location',RelatedOnlyDropdownFilter),
    )


@admin.register(StgAnnouncements)
class EventsAnnouncementAdmin(TranslatableAdmin,ImportExportModelAdmin,
    OverideImport,ImportExportActionModelAdmin):
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

    #to make URl clickable, I changed show_url to just url in the list_display tuple
    def show_external_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.external_url)

    def show_url(self, obj):
        return obj.url if obj.url else 'None'

    show_external_url.allow_tags = True
    show_external_url.short_description= 'Web Link (URL)'

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

    fieldsets = (
        ('Event Details', {
                'fields':('name','shortname','message','start_year',
                'end_year','location','status') #afrocode may be null
            }),
            ('Files and Web Resources', {
                'fields': ('internal_url','external_url','cover_image'),
            }),
        )
    list_display=['name','code','shortname','message','period','internal_url',
        'show_external_url']
    list_display_links = ['name','code']
    search_fields = ('name','shortname','location__name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
    exclude = ('date_created','date_lastupdated','code',)
    list_filter = (
        ('location',RelatedOnlyDropdownFilter),
    )
