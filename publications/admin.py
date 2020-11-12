from django.contrib import admin
from parler.admin import TranslatableAdmin
from django.utils.html import format_html
import data_wizard # Solution to data import madness that had refused to go
from django.forms import TextInput,Textarea #customize textarea row and column size
from import_export.formats import base_formats
from .models import (StgProductDomain,StgKnowledgeProduct,StgResourceType,
    StgResourceCategory)
from commoninfo.admin import OverideImportExport,OverideExport
# from publications.serializers import StgKnowledgeProductSerializer
from regions.models import StgLocation
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom
from .resources import (StgKnowledgeProductResourceExport,
    StgKnowledgeProductResourceImport)
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


@admin.register(StgResourceType)
class ResourceTypeAdmin(TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    list_display=['name','code','shortname','description']
    list_display_links =('code', 'name',)
    search_fields = ('translations__name','translations__shortname','code',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


@admin.register(StgResourceCategory)
class ResourceCategoryAdmin(TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    list_display=['name','code','shortname','description']
    list_display_links =('code', 'name',)
    search_fields = ('translations__name','translations__shortname','code') #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


# data_wizard.register(StgKnowledgeProduct)
#     "Import Knowledge Resource List",StgKnowledgeProductSerializer)
@admin.register(StgKnowledgeProduct)
class ProductAdmin(TranslatableAdmin,ImportExportModelAdmin,
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

    def get_export_resource_class(self):
        return StgKnowledgeProductResourceExport

    def get_import_resource_class(self):
        return StgKnowledgeProductResourceImport

     #This function is used to register permissions for approvals. See signals,py
    def get_actions(self, request):
        actions = super(ProductAdmin, self).get_actions(request)
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
            ('Attribution, Access and Approval Details', {
                'fields': ('author','year_published','internal_url',
                    'external_url','cover_image','comment'),
            }),
        )

    def get_location(obj):
           return obj.location.name
    get_location.short_description = 'Publication Place'

    def get_type(obj):
           return obj.type.name
    get_type.short_description = 'Type'


    # To display the choice field values use the helper method get_foo_display where foo is the field name
    list_display=['title','code',get_type,'author','year_published',get_location,
        'internal_url','show_external_url','get_comment_display']
    list_display_links = ['code','title',]
    readonly_fields = ('comment',)
    search_fields = ('translations__title','type__translations__name',
        'location__translations__name',) #display search field
    list_per_page = 50 #limit records displayed on admin site to 30
    actions = [transition_to_pending,transition_to_approved,
        transition_to_rejected]
    exclude = ('date_created','date_lastupdated','code',)
    list_filter = (
        ('location',RelatedOnlyDropdownFilter),
        ('type',RelatedOnlyDropdownFilter),
        ('comment',DropdownFilter),
    )


@admin.register(StgProductDomain)
class ProductDomainAdmin(TranslatableAdmin,OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    fieldsets = (
        ('Resource Attributes', {
                'fields':('name','shortname','description','parent','level') #afrocode may be null
            }),
        ('Resource Publications', {
                'fields':('publications',) #afrocode may be null
            }),
        )

    list_display=['name','code','shortname','parent','level']
    list_display_links =('name','shortname','code',)
    search_fields = ('translations__name','translations__shortname','code',) #display search field

    filter_horizontal = ('publications',) # should display multiselect records

    exclude = ('date_created','date_lastupdated','code',)
    list_per_page = 50 #limit records displayed on admin site to 15
    list_filter = (
        ('parent',RelatedOnlyDropdownFilter),
        ('publications',RelatedOnlyDropdownFilter,),# Added 16/12/2019 for M2M lookup
    )
