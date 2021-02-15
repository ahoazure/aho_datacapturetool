from django.db import models
import uuid
import datetime
# from datetime import datetime #for handling year part of date filed
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
        verbose_name_plural = _(' Facilities Ownerhip')
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


class StgHealthFacility(TranslatableModel):
    STATUS_CHOICES = (
        ('active', _('Active')),
        ('closed', _('Closed')),
    )

    COUNTRY_CODES = ('+242','+244','+254', '+256',' +263',)
    # Regular expression to validate phone number entry to international format
    number_regex = RegexValidator(
    regex=r'^[0-9]{8,15}$', message="Format:'999999999' min 8, maximum 15.")
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
    # convert this to look up to the location and then queryset lower level
    admin_location = models.CharField(_('Administrative Location'),max_length=230,
        blank=True,null=True)
    # admin_location = models.ForeignKey(StgLocation, models.PROTECT,
    #     verbose_name=_('Administrative Location'),related_name='admin_location')
    translations = TranslatedFields(
        description = models.TextField(_('Facility Description'),blank=True,
        null=True) # Field name made lowercase.
    )  # End of translatable field(s)
    address = models.CharField(_('Contact Address'),max_length=500,blank=True,
        null=True)  # Field name made lowercase.
    email = models.EmailField(_('Email'),unique=True,max_length=250,
        blank=True,null=True)  # Field name made lowercase.
    phone_code = models.CharField(choices=make_choices(COUNTRY_CODES),
        default=COUNTRY_CODES[0],max_length=5,verbose_name='Country Code',)
    phone_part = models.CharField(_('Phone Number'),validators=[number_regex],
        max_length=15, blank=True) # validators should be a list
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

    """
    The purpose of this method is to concatenate phone parts into phone_number
     that has international format ---This takes care of Hillary's request
    """
    def get_phone(self):
        if self.phone_number is None or (self.phone_code and self.phone_part):
            phone_number =self.phone_code+self.phone_part
        return phone_number

    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgHealthFacility.objects.filter(name=self.name).count() and not \
            self.facility_id and not self.year_published and not self.location:
            raise ValidationError({'name':_('Facility  with the same name exists')})

    def save(self, *args, **kwargs):
        self.phone_number = self.get_phone()
        super(StgHealthFacility, self).save(*args, **kwargs)


class FacilityServiceAvilability(models.Model):
    PROMOTION_CHOICES = ( #choices for approval of indicator data by authorized users
        ('NCD health promotion', _('NCD promotion')),
        ('CD health promotion', _('Child health promotion')),
        ('Child health promotion', _('Child health promotion')),
        ('Adolescent health promotion',_('Adolescent health promotion')),
        ('Adult health promotion',_('Adult health promotion')),
        ('Elderly health promotion',_('Elderly health promotion')),
    )

    SERVICE_CHOICES = ( #choices for approval of indicator data by authorized users
        ('NCD HPR', _('NCD HPR')),
        ('CD health HPR', _('Child health HPR')),
        ('Child health HPR', _('Child health HPR')),
        ('Adolescent health HPR ',_('Adolescent health HPR')),
        ('Adult health HPR',_('Adult health HPR')),
        ('Elderly health HPR',_('Elderly health HPR')),
    )
    availability_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    code = models.CharField(unique=True, blank=True,null=False,max_length=45)
    domain = models.ForeignKey(StgServiceDomain, models.PROTECT,blank=False,
        null=False,verbose_name = _('Service Domain'),default=2)
    facility = models.ForeignKey(StgHealthFacility, models.PROTECT,
        verbose_name = _('Facility Name'))
    intervention = models.CharField(_('Intervention area'),max_length=50,
        blank=False,choices= PROMOTION_CHOICES,default=PROMOTION_CHOICES[0][0])
    service = models.CharField(_('Service provision area)'),max_length=50,
        blank=False,choices= SERVICE_CHOICES,default=SERVICE_CHOICES[0][0])
    provided = models.BooleanField(_('Service Provided last 3 Months?'),
        default=False)
    specialunit = models.BooleanField(_('Specialized Unit Provided?'),
        default=False)
    staff = models.BooleanField(_('Staff Capacity Appropriate?'),
        default=False)
    infrastructure = models.BooleanField(_('Infrastructure Capacity Appropriate?'),
        default=False)
    supplies = models.BooleanField(_('Supplies Appropriate?'),
        default=False)
    start_period = models.IntegerField(_('Starting period'),null=False,blank=False,
        default=datetime.date.today().year,#extract current date year value only
        help_text=_("This marks the start of reporting period"))
    end_period  = models.IntegerField(_('Ending Period'),null=False,blank=False,
        default=datetime.date.today().year, #extract current date year value only
        help_text=_("This marks the end of reporting. The value must be current \
            year or greater than the start year"))
    period = models.CharField(_('Period'),max_length=25,blank=True,null=False)
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)


    class Meta:
        managed = True # must be true to create the model table in mysql
        unique_together = ('domain','facility','start_period','end_period',
            'intervention')
        db_table = 'stg_facility_services_availability'
        verbose_name = _('Service Availability')
        verbose_name_plural = _('Services Avilability')
        ordering = ('domain',)

    def __str__(self):
        return str(self.domain)

    """
    The purpose of this method is to concatenate the date that are entered as
    start_period and end_period and save the concatenated value as a string in
    the database ---this is very important to take care of Davy's date complexity
    """
    def get_period(self):
        if self.period is None or (self.start_period and self.end_period):
            if self.start_period == self.end_period:
                period = int(self.start_period)
            else:
                period =str(int(self.start_period))+"-"+ str(int(self.end_period))
        return period

    """
    The purpose of this method is to compare the start_period to the end_period.
    If the start_period is greater than the end_period athe model should show
    an inlines error message and wait until the user corrects the mistake.
    """
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if self.start_period <=1900 or self.start_period > datetime.date.today().year:
            raise ValidationError({'start_period':_(
                'Sorry! Start year cannot < 1900 or greater than current Year ')})
        elif self.end_period <=1900 or self.end_period > datetime.date.today().year:
            raise ValidationError({'end_period':_(
                'Sorry! The ending year cannot be lower than the start year or \
                greater than the current Year ')})
        elif self.end_period < self.start_period and self.start_period is not None:
            raise ValidationError({'end_period':_(
                'Sorry! Ending period cannot be lower than the start period. \
                 Please make corrections')})

    # Ensure the intervention area matches the service provision area
        if self.intervention[:3]!= self.service[:3]:
            raise ValidationError({'intervention':_(
                'Sorry! Intervention area must match service provision area')})

    def save(self, *args, **kwargs):
        self.period = self.get_period()
        super(FacilityServiceAvilability,self).save(*args, **kwargs)


class FacilityServiceAvailabilityProxy(StgHealthFacility):
    class Meta:
        proxy = True
        managed = False
        verbose_name = 'Service Availability'
        verbose_name_plural = '  Services Availability Form'

    """
    This def clean (self) method was contributed by Daniel Mbugua to resolve
    the issue of parent-child saving issue in the multi-records entry form.
    My credits to Mr Mbugua of MSc DCT, UoN-Kenya
    """
    def clean(self): #Appreciation to Daniel M.
        pass
