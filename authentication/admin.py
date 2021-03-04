from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from regions.models import StgLocation
from django.contrib.admin.models import LogEntry
from .models import CustomUser, CustomGroup,AhodctUserLogs
from . import models
from django.forms import TextInput,Textarea #for customizing textarea row and column size
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom

@admin.register(models.CustomUser)
class UserAdmin (UserAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location
        if request.user.is_superuser:
            qs # return all instances of the request instances
        elif user in groups: # Fetch all instances of group membership
            qs=qs.filter(location=user_location)
        else:
            qs=qs.filter(email=request.user)
        return qs

    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')

        if db_field.name == "location":
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocation.objects.all().order_by(
                'location_id')
                # Looks up for the location level upto the country level
            elif user in groups and user_location==1:
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__locationlevel_id__gte=1,
                locationlevel__locationlevel_id__lte=2).order_by(
                'location_id')
            else:
                kwargs["queryset"] = StgLocation.objects.filter(
                location_id=request.user.location_id).translated(
                language_code='en')
        return super().formfield_for_foreignkey(db_field, request,**kwargs)

    readonly_fields = ('last_login','date_joined',)
    fieldsets = (
        ('Personal info', {'fields': ('title','first_name', 'last_name',
            'gender','location')}),
        ('Login Credentials', {'fields': ('email', 'username','password',)}),
        ('Account Permissions', {'fields': ('is_active', 'is_staff',
            'is_superuser', 'groups', 'user_permissions')}),
        ('Login Details', {'fields': ('last_login',)}),
    )
    limited_fieldsets = (
        ('Persional Details', {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name','location')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('Contacts and Password', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

    list_display = ['first_name','last_name','username','email','gender',
        'location','last_login']
    list_display_links = ['first_name','last_name','username','email']


# class GroupInline(admin.StackedInline):
#     model = CustomGroup
#     can_delete = False
#     verbose_name_plural = 'Group Roles'


admin.site.unregister(Group) # Must unregister the group in order to use the custom one
@admin.register(models.CustomGroup)
class GroupAdmin(BaseGroupAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location
        if request.user.is_superuser:
            qs # return all instances of the request instances
        elif user in groups and user_location==2: # Fetch instances of group membership
            qs=qs.filter(location=user_location)
        else:
            qs=qs.filter(user=request.user)
        return qs
    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        user_location = request.user.location.location_id
        db_locations = StgLocation.objects.all().order_by('location_id')

        if db_field.name == "location":
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocation.objects.all().order_by(
                'location_id')
                # Looks up for the location level upto the country level
            elif user in groups and user_location<=2:
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__locationlevel_id__gt=2,
                locationlevel__locationlevel_id__lte=3).order_by(
                'location_id')
            else:
                kwargs["queryset"] = StgLocation.objects.filter(
                location_id=request.user.location_id).order_by(
                'location_id')
        return super().formfield_for_foreignkey(db_field, request,**kwargs)

    list_display = ['name','roles_manager','location',]


# This is the admin interface that allows the super admin to track user activities!
@admin.register(AhodctUserLogs)
class AhoDCT_LogsAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None): #This function removes the add button on the admin interface
        return False

    def has_add_permission(self, request, obj=None): #This function removes the add button on the admin interface
        return False
    #This method removes the save buttons from the model form
    def changeform_view(self,request,object_id=None, form_url='',extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(AhoDCT_LogsAdmin, self).changeform_view(
            request, object_id, extra_context=extra_context)

    list_display=['username','email','first_name', 'last_name','location_translation',
        'app_label','record_name','action','action_time','last_login',]
    readonly_fields = ('username','email','first_name', 'last_name','location_translation',
        'app_label','record_name','action','action_time','last_login',)
    search_fields = ('username','email','first_name', 'last_name','location_translation',
        'app_label','record_name','action',)
    list_filter = (
        ('record_name', DropdownFilter,),
        ('app_label', DropdownFilter,),
        ('location_translation', DropdownFilter,),
        ('action', DropdownFilter),
    )
    ordering = ('-action_time',)
