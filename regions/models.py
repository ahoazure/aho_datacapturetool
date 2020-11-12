from django.db import models
import uuid
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ # The _ is alias for gettext
from parler.models import TranslatableModel, TranslatedFields

def make_choices(values):
    return [(v, v) for v in values]

class StgLocationLevel(TranslatableModel):
    LEVEL = ('level 1','Level 2','Level 3', 'Level 4', 'Level 5','Level 6','Level 7')
    locationlevel_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    translations = TranslatedFields(
        type = models.CharField(_('Location Level'),max_length=50,
            choices=make_choices(LEVEL),default=LEVEL[0]),  # Field name made lowercase.
        name = models.CharField(_('Level Name'),max_length=230, blank=False,
            null=False),  # Field name made lowercase.
        description = models.TextField(_('Description'),blank=True, null=True)  # Field name made lowercase.
    )
    code = models.CharField(unique=True, max_length=50, blank=True,null=False)  # Field name made lowercase.
    date_created = models.DateTimeField(_('Date Created'),blank=True,null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = 'stg_location_level'
        verbose_name = _('Location Level')
        verbose_name_plural = _('  Location Levels')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #display only the level name

    # The filter function need to be modified to work with django parler as follows:
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgLocationLevel.objects.filter(
            translations__name=self.name).count() and not self.locationlevel_id:
            raise ValidationError({'name':_('Sorry! This location level exists')})

    def save(self, *args, **kwargs):
        super(StgLocationLevel, self).save(*args, **kwargs)


class StgWorldbankIncomegroups(TranslatableModel):
    wb_income_groupid = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    translations = TranslatedFields(
        name = models.CharField(_('Income level'),max_length=230, blank=False,
            null=False),  # Field name made lowercase.
        shortname = models.CharField(_('Short Name'),unique=True,max_length=50,
            blank=False,null=False),
        description = models.TextField(_('Brief Description'),blank=True, null=True)  # Field name made lowercase.
    )
    code = models.CharField(max_length=50, unique=True,blank=True, null=False)  # Field name made lowercase.
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = 'stg_worldbank_incomegroups'
        verbose_name = _('Income Group')
        verbose_name_plural = 'Income Groups'
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #display only the level name

    # The filter function need to be modified to work with django parler as follows:
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgWorldbankIncomegroups.objects.filter(
            translations__name=self.name).count() and not self.wb_income_groupid:
            raise ValidationError({'name':_('Sorry! This economic grouping exists')})

    def save(self, *args, **kwargs):
        super(StgWorldbankIncomegroups, self).save(*args, **kwargs)

class StgEconomicZones(TranslatableModel):
    economiczone_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    translations = TranslatedFields(
    name = models.CharField(_('Economic Zone'),max_length=230,blank=False,
        null=False),
    shortname = models.CharField(_('Short Name'),unique=True,max_length=50,
        blank=True, null=True),  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)  # Field name made lowercase.
    )
    code = models.CharField(max_length=50, unique=True, blank=True, null=False)
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = 'stg_economic_zones'
        verbose_name = _('Economic Block')
        verbose_name_plural = _('Economic Blocks')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #display the data source name

    # The filter function need to be modified to work with django parler as follows:
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgEconomicZones.objects.filter(
            translations__name=self.name).count() and not self.economiczone_id:
            raise ValidationError({'name':_('Sorry! This economic block exists')})

    def save(self, *args, **kwargs):
        super(StgEconomicZones, self).save(*args, **kwargs)

class StgSpecialcategorization(TranslatableModel):
    specialstates_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    translations = TranslatedFields(
        name = models.CharField(_('Categorization Name'),max_length=230,
            blank=False, null=False),  # Field name made lowercase.
        shortname = models.CharField(_('Short Name'),unique=True,max_length=50,
            blank=False,null=False),  # Field name made lowercase.
        description = models.TextField(_('Brief Description'),blank=True, null=True)  # Field name made lowercase.
    )
    code = models.CharField(max_length=50, unique=True, blank=True,null=False)
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = 'stg_specialcategorization'
        verbose_name = _('Categorization')
        verbose_name_plural = _('Special Categorizations')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #display only the level name

    # The filter function need to be modified to work with django parler as follows:
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgSpecialcategorization.objects.filter(
            translations__name=self.name).count() and not self.specialstates_id:
            raise ValidationError({'name':_('Sorry! This states categorization exists')})

    def save(self, *args, **kwargs):
        super(StgSpecialcategorization, self).save(*args, **kwargs)


class StgLocation(TranslatableModel):
    location_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    locationlevel = models.ForeignKey(StgLocationLevel, models.PROTECT,
        blank=False,verbose_name = _('Location Level'),
        help_text=_("You are not allowed to make changes to this Field because it \
            is related to other Records"))  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(_('Location Name'),max_length=230,blank=False,
            null=False),  # Field name made lowercase.
        description = models.TextField(_('Brief Description'),blank=True, null=True),
        latitude = models.FloatField(_('Latitude'),blank=True, null=True),
        longitude = models.FloatField(_('Longitude'),blank=True, null=True),
        cordinate = models.TextField(_('Cordinates'),blank=True, null=True)
    )
    iso_alpha = models.CharField(_('ISO Alpha Code'),unique=True,max_length=15,
        blank=False,null=False)
    iso_number = models.CharField(_('ISO Numeric Code'),unique=True, max_length=15,
        blank=False)
    code = models.CharField(_('Unique Code'),unique=True, max_length=15,
        blank=True, null=False)
    parent = models.ForeignKey('self', models.PROTECT,blank=True, null=True,
        verbose_name = _('Parent Location'),default=1,
        help_text=_("You are not allowed to edit this field because it is\
        related to other records"))
    wb_income = models.ForeignKey(StgWorldbankIncomegroups, models.PROTECT,blank=False,
        null=False, verbose_name = _('Income level'), default='99')  # Field name made lowercase.
    zone = models.ForeignKey(StgEconomicZones, models.PROTECT, blank=False,
        null=False, verbose_name = _('Economic Block'),default=6)  # Field name made lowercase.
    special = models.ForeignKey(StgSpecialcategorization, models.PROTECT,
        blank=False, null=False, verbose_name = _('Special Categorization'))  # Field name made lowercase.
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = 'stg_location'
        verbose_name = _('Location') # this is important in the display on change details and the add button
        verbose_name_plural = _('   Locations')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #display the location name such as country

    # This function makes sure the location name is unique instead of enforcing unque constraint on DB
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgLocation.objects.filter(
            translations__name=self.name).count() and not self.location_id:
            raise ValidationError(
                {'name':_('Location with similar name exists')})

    def save(self, *args, **kwargs):
        super(StgLocation, self).save(*args, **kwargs)
