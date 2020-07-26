from django.contrib import admin
from parler.admin import TranslatableAdmin
from django.forms import TextInput,Textarea #for customizing textarea row and column size
from .models import (StgLocationLevel,StgEconomicZones,StgWorldbankIncomegroups,
    StgSpecialcategorization,StgLocation)
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom


@admin.register(StgLocationLevel)
class RegionAdmin(TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    # resource_class = LocationLevelResourceExport
    list_display=['code','name','type','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('code','name','type') #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)
    # list_filter = (
    #     ('name',DropdownFilter),
    # )

@admin.register(StgEconomicZones)
class EconomicBlocksAdmin(TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    # resource_class = EconomicZoneResourceExport
    list_display=['code','name','shortname','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('name','shortname') #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code')


@admin.register(StgWorldbankIncomegroups)
class WBGroupsAdmin(TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    # resource_class = IncomegroupsResourceExport
    list_display=['code','name','shortname','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('code','name',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)


@admin.register(StgSpecialcategorization)
class SpecialStatesAdmin(TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    # resource_class = SpecialcategorizationResourceExport
    list_display=['code','name','shortname','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('name','shortname',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code')


@admin.register(StgLocation)
class LocationAdmin(TranslatableAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(
            name__icontains='Admins'):
            return qs #provide access to all instances/rows of all location, i.e. all AFRO member states
        return qs.filter(location_id=request.user.location_id)#provide the user with specific country details!

    # #This function is for filtering location to display regional level only. The database field must be parentid for the dropdown list
    # def formfield_for_foreignkey(self, db_field, request =None, **kwargs): #to implement user filtering her
    #     if db_field.name == "parent":
    #         if request.user.is_superuser or request.user.groups.filter(
    #             name__icontains='Admins'):
    #             kwargs["queryset"] = StgLocation.objects.filter(
    #             locationlevel__name__in =['Regional','Global']).order_by('locationlevel',) #superuser can access all countries at level 2 in the database
    #         else:
    #             kwargs["queryset"] = StgLocation.objects.filter(
    #                 location_id=request.user.location_id) #permissions for user country filter---works as per Davy's request
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

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

    #resource_class = LocationResourceExport

    list_display=['name','iso_alpha','code','zone','special',]
    list_display_links = ('code', 'name',) #display as clickable link
    search_fields = ('code','name', 'iso_alpha') #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)
    list_filter = (
        ('locationlevel',RelatedOnlyDropdownFilter),
        ('parent',RelatedOnlyDropdownFilter),
    )
