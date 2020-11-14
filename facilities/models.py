from django.db import models
import uuid
from datetime import datetime #for handling year part of date filed
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _ # The _ is alias for gettext
from parler.models import TranslatableModel,TranslatedFields
from regions.models import StgLocation

def make_choices(values):
    return [(v, v) for v in values]

# New model to take care of resource types added 11/05/2019 courtesy of Gift
class StgFacilityType(TranslatableModel):
    type_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    code = models.CharField(_('Facility Code'),unique=True, max_length=50,
        blank=True,null=True)  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(_('Facility Type'),max_length=230, blank=False,
            null=False,
            ),  # Field name made lowercase.
        shortname = models.CharField(_('Short Name'),unique=True,max_length=50,
            blank=False,null=False),  # Field name made lowercase.
        description = models.TextField(_('Brief Description'),blank=True, null=True)  # Field name made lowercase.
    )
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = 'stg_facility_type'
        verbose_name = _('Facility Type')
        verbose_name_plural = _('  Facility Types')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #display the knowledge product category name

    def clean(self):
        if StgFacilityType.objects.filter(
            translations__name=self.name).count() and not self.type_id and not \
                self.code:
            raise ValidationError({'name':_('Facility type with the same \
                name exists')})

    def save(self, *args, **kwargs):
        super(StgFacilityType, self).save(*args, **kwargs)


# New model to take care of resource types added 11/05/2019 courtesy of Gift
class StgFacilityInfrastructure(TranslatableModel):
    infra_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    code = models.CharField(_('Code'),unique=True, max_length=50,
        blank=True,null=True)  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(_('Infrastructure Name'),max_length=230,
            blank=False, null=False),  # Field name made lowercase.
        shortname = models.CharField(_('Short Name'),unique=True,max_length=50,
            blank=False,null=False),  # Field name made lowercase.
        description = models.TextField(_('Brief Description'),blank=True, null=True)  # Field name made lowercase.
    )
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)


    class Meta:
        managed = True
        db_table = 'stg_facility_infrastructure'
        verbose_name = _('Infrastructure')
        verbose_name_plural = _('Health Infrastructures')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #display the knowledge product category name

    def clean(self):
        if StgFacilityInfrastructure.objects.filter(
            translations__name=self.name).count() and not self.infra_id and not \
                self.code:
            raise ValidationError({'name':_('Facility type with the same \
                name exists')})

    def save(self, *args, **kwargs):
        super(StgFacilityInfrastructure, self).save(*args, **kwargs)


class StgFacilityOwnership(TranslatableModel):
    owner_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    code = models.CharField(_('Code'),unique=True, max_length=50, blank=True,
        null=True)  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(_('Facility Owner'),max_length=230, blank=False,
            null=False),
        shortname = models.CharField(_('Short Name'),unique=True,max_length=50,
            blank=False,null=False),  # Field name made lowercase.
        description = models.TextField(_('Brief Description'),blank=True, null=True)  # Field name made lowercase.
    )
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)


    class Meta:
        managed = True
        db_table = 'stg_facility_owner'
        verbose_name = _('Facility Owner')
        verbose_name_plural = _(' Facility Owners')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #display the knowledge product category name

    def clean(self):
        if StgFacilityOwnership.objects.filter(
            translations__name=self.name).count() and not self.owner_id and not \
                self.code:
            raise ValidationError({'name':_('facility owner with the same \
                name exists')})

    def save(self, *args, **kwargs):
        super(StgFacilityOwnership, self).save(*args, **kwargs)


class StgHealthFacility(TranslatableModel):
    STATUS_CHOICES = (
        ('active', _('Active')),
        ('closed', _('Closed')),
    )
    # Regular expression to validate phone number entry to international format
    phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$', message="Phone format: '+999999999' maximum 15.")
    facility_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    code = models.CharField(unique=True, blank=True,null=False,max_length=45)
    type = models.ForeignKey(StgFacilityType, models.PROTECT,blank=False,
        null=False,verbose_name = _('Facility Type'))
    location = models.ForeignKey(StgLocation, models.PROTECT,
        verbose_name = _('Location'))
    owner = models.ForeignKey(StgFacilityOwnership, models.PROTECT,
        verbose_name = _('Facility Owner'))
    name = models.CharField(_('Facility Name'),max_length=230,blank=False,
        null=False)  # Field name made lowercase.
    shortname = models.CharField(_('Short Name (Abbreviation)'),max_length=230,
        blank=True, null=True,)
    admin_location = models.CharField(_('Administrative Location'),max_length=230,
        blank=True,null=True)
    translations = TranslatedFields(
        description = models.TextField(_('Facility Description'),blank=True, null=True) # Field name made lowercase.
    )  # End of translatable field(s)
    address = models.CharField(_('Contact Address'),max_length=500,blank=True,
        null=True)  # Field name made lowercase.
    email = models.EmailField(_('Email'),unique=True,max_length=250,
        blank=True,null=True)  # Field name made lowercase.
    phone_number = models.CharField(_('Telephone'),validators=[phone_regex],
        max_length=15, blank=True) # validators should be a list
    latitude = models.FloatField(_('Latitude'),blank=True, null=True)
    longitude = models.FloatField(_('Longitude'),blank=True, null=True)
    altitude = models.FloatField(_('Altitude (M)'),blank=True, null=True)
    geosource = models.CharField(_('Geo-source (LL source)'),max_length=500,
        blank=True,null=True)  # Field name made lowercase.
    url = models.URLField(_('Web (URL)'),blank=True, null=True,max_length=2083)
    status = models.CharField(_('Status'),max_length=10, choices= STATUS_CHOICES,
        default=STATUS_CHOICES[0][0])
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = 'stg_health_facility'
        verbose_name = _('Health Facility')
        verbose_name_plural = _('   Health Facilities')
        ordering = ('name',)

    def __str__(self):
        return self.name #display the data element name

    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgHealthFacility.objects.filter(name=self.name).count() and not \
            self.facility_id and not self.year_published and not self.location:
            raise ValidationError({'name':_('Facility  with the same name exists')})

    def save(self, *args, **kwargs):
        super(StgHealthFacility, self).save(*args, **kwargs)


class StgServiceDomain(TranslatableModel):
    LEVEL = ('Level 0','level 1','Level 2','Level 3', 'Level 4', 'Level 5',
        'Level 6','Level 7','Level 8','Level 9','Level 10',)
    domain_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    translations = TranslatedFields(
        name = models.CharField(_('Domain Name'),max_length=230, blank=False,
            null=False),  # Field name made lowercase.
        shortname = models.CharField(_('Short Name'),max_length=45,null=True),  # Field name made lowercase.
        description = models.TextField(_('Brief Description'),blank=True, null=True)
    )
    level = models.CharField(_('Domain Level'),max_length=50, choices=make_choices(LEVEL),
        default=LEVEL[0])
    code = models.CharField(_('Code'),unique=True, max_length=50, blank=True,
            null=True)  # Field name made lowercase.
    parent = models.ForeignKey('self',on_delete=models.CASCADE,
        blank=True,null=True,verbose_name = 'Parent Domain')  # Field name made lowercase.
    facilities = models.ManyToManyField(StgHealthFacility,
        db_table='stg_facility_services_lookup',
        blank=True,verbose_name =_('Health Facilities'))  # Field name made lowercase.
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)


    class Meta:
        managed = True # must be true to create the model table in mysql
        db_table = 'stg_facility_services'
        verbose_name = _('Facility Service')
        verbose_name_plural = _('Facility Services')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #display the knowledge product category name

    def clean(self):
        if StgServiceDomain.objects.filter(
            translations__name=self.name).count() and not self.domain_id and not \
                self.code:
            raise ValidationError({'name':_('Domain with the same name exists')})

    def save(self, *args, **kwargs):
        super(StgServiceDomain, self).save(*args, **kwargs)
