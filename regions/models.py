from django.db import models
import uuid
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ # The _ is alias for gettext
from parler.models import TranslatableModel, TranslatedFields

def make_choices(values):
    return [(v, v) for v in values]

class StgLocationLevel(TranslatableModel):
    LEVEL = ('level 1','Level 2','Level 3', 'Level 4', 'Level 5',)
    locationlevel_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    translations = TranslatedFields(
        type = models.CharField(max_length=50, choices=make_choices(LEVEL),
            default=LEVEL[0],verbose_name = 'Location Level'),  # Field name made lowercase.
        name = models.CharField(max_length=230, blank=False, null=False,
            verbose_name = 'Level Name'),  # Field name made lowercase.
        description = models.TextField(blank=True, null=True)  # Field name made lowercase.
    )
    code = models.CharField(unique=True, max_length=50, blank=True, null=False)  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'stg_location_level'
        verbose_name = 'Location Level'
        verbose_name_plural = 'Location Levels'
        ordering = ('code', )

    def __str__(self):
        return self.name #display only the level name

class StgWorldbankIncomegroups(TranslatableModel):
    wb_income_groupid = models.AutoField(primary_key=True)  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(max_length=230, blank=False, null=False,
            verbose_name = 'Income Group',),  # Field name made lowercase.
        shortname = models.CharField(unique=True,max_length=50, blank=False,
            null=False,verbose_name = 'Short Name'),  # Field name made lowercase.
        description = models.TextField(blank=True, null=True)  # Field name made lowercase.
    )
    code = models.CharField(max_length=50, unique=True,blank=True, null=False)  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'stg_worldbank_incomegroups'
        verbose_name = _('Income Group')
        verbose_name_plural = 'Income Groups'
        ordering = ('code', )

    def __str__(self):
        return self.name #display only the level name

class StgEconomicZones(TranslatableModel):
    economiczone_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    translations = TranslatedFields(
    name = models.CharField(max_length=230,blank=False, null=False,
        verbose_name = 'Economic Block'),
    shortname = models.CharField(unique=True,max_length=50, blank=True, null=True,
        verbose_name = 'Short Name'),  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)  # Field name made lowercase.
    )
    code = models.CharField(max_length=50, unique=True, blank=True, null=False)
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'stg_economic_zones'
        verbose_name = 'Economic Block'
        verbose_name_plural = 'Economic Blocks'
        ordering = ('code', )

    def __str__(self):
        return self.name #display the data source name


class StgSpecialcategorization(TranslatableModel):
    specialstates_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(max_length=230,blank=False, null=False,
            verbose_name = 'Special State'),  # Field name made lowercase.
        shortname = models.CharField(unique=True,max_length=50,blank=False,null=False,
            verbose_name = 'Short Name'),  # Field name made lowercase.
        description = models.TextField(blank=True, null=True)  # Field name made lowercase.
    )
    code = models.CharField(max_length=50, unique=True, blank=True,null=False)
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'stg_specialcategorization'
        verbose_name = 'Special Categorization'
        verbose_name_plural = 'Special Categorizations'
        ordering = ('code', )

    def __str__(self):
        return self.name #display only the level name

class StgLocation(TranslatableModel):
    location_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    locationlevel = models.ForeignKey('StgLocationLevel', models.PROTECT,
        verbose_name = 'Location Level',
        help_text="You are not allowed to make changes to this Field because it \
            is related to other Records")  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(max_length=230,blank=False, null=False,
            verbose_name = 'Location Name'),  # Field name made lowercase.
        iso_alpha = models.CharField(unique=True, max_length=15, blank=False,
            null=False,verbose_name = 'ISO Alpha Code'),  # Field name made lowercase.
        iso_number = models.CharField(unique=True, max_length=15, blank=False,
            verbose_name = 'ISO Numeric Code'),
        description = models.TextField(blank=True, null=True),
        latitude = models.FloatField(blank=True, null=True),
        longitude = models.FloatField(blank=True, null=True),
        cordinate = models.TextField(blank=True, null=True)
    )
    code = models.CharField(unique=True, max_length=15, blank=True, null=False,
        verbose_name = 'Location Code')  # Field name made lowercase.
    parent = models.ForeignKey('self', models.PROTECT,blank=True, null=True,
        verbose_name = 'Parent Location',default=1,
        help_text="You are not allowed to edit this field because it is related to other records")  # Field name made lowercase.

    wb_income = models.ForeignKey('StgWorldbankIncomegroups', models.PROTECT,blank=False,
        null=False, verbose_name = 'WB Income Group', default='99')  # Field name made lowercase.
    zone = models.ForeignKey(StgEconomicZones, models.PROTECT, blank=False,
        null=False, verbose_name = 'Economic Block',default=6)  # Field name made lowercase.
    special = models.ForeignKey('StgSpecialcategorization', models.PROTECT,
        blank=False, null=False, verbose_name = 'Special Categorization',)  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'stg_location'
        verbose_name = 'Location' # this is important in the display on change details and the add button
        verbose_name_plural = 'Locations'
        ordering = ['code',]

    def __str__(self):
        return self.name #display the location name such as country

    # This function makes sure the location name is unique instead of enforcing unque constraint on DB
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgLocation.objects.filter(
            translations__name=self.name).count() and not self.location_id:
            raise ValidationError(
                {'name':_('Location with the same name already exists')})

    def save(self, *args, **kwargs):
        super(StgLocation, self).save(*args, **kwargs)
