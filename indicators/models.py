from django.db import models
import uuid
from django.utils import timezone
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.fields import DecimalField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from home.models import ( StgDatasource, StgCategoryoption, StgMeasuremethod,
    StgValueDatatype,)
from regions.models import StgLocation

STATUS_CHOICES = ( #choices for approval of indicator data by authorized users
    ('pending', 'Pending'),
    ('approved','Approved'),
    ('rejected','Rejected'),
)

class StgIndicatorReference(TranslatableModel):
    reference_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(_("Reference Name"),max_length=230, blank=False,
            null=False,default="Global List of 100 Core Health Indicators"),  # Field name made lowercase.
        shortname = models.CharField(max_length=50, blank=True, null=True,
            verbose_name = 'Short Name'),  # Field name made lowercase.
        description = models.TextField( blank=True, null=True)
    )
    code = models.CharField(unique=True, max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'stg_indicator_reference'
        verbose_name = 'Reference'
        verbose_name_plural = ' References'
        #ordering = ('code', )


    def __str__(self):
        return self.name #display the data source name


class StgIndicator(TranslatableModel):
    indicator_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField( max_length=500, blank=False, null=False,
            verbose_name = _('Indicator Name')),  # Field name made lowercase.
        shortname = models.CharField(unique=True, max_length=120, blank=False,
            null=True, verbose_name = 'Short Name'),  # Field name made lowercase.
        gen_code = models.CharField( max_length=10, blank=True, null=True,
            verbose_name = 'Geneva Code'),  # Field name made lowercase.
        definition = models.TextField(blank=False,
            null=True,verbose_name = 'Indicator Definition' ),  # Field name made lowercase.
        preferred_datasources = models.CharField(max_length=5000,
            blank=True, null=True, verbose_name = 'Data Sources'),  # Field name made lowercase.
        numerator_description = models.TextField(blank=True,
            null=True, verbose_name = 'Numerator Description'),  # Field name made lowercase.
        denominator_description = models.TextField(blank=True,null=True,
            verbose_name = 'Denominator Description')  # Field name made lowercase.
    )
    afrocode = models.CharField(max_length=10,blank=True, null=False,
        unique=True, verbose_name = 'Indicator Code',)  # Field name made lowercase.
    measuremethod = models.ForeignKey(StgMeasuremethod, models.PROTECT,blank=True,
        null=True, verbose_name = 'Type of Measure')  # Field name made lowercase.
    reference = models.ForeignKey(StgIndicatorReference, models.PROTECT,
        default=1, verbose_name ='Indicator Reference')  # Field name made lowercase.

    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'stg_indicator'
        verbose_name = 'Indicator'
        verbose_name_plural = '  Indicators'
        ordering = ('afrocode',)

    def __str__(self):
        return self.name #display the indicator name

    # The filter function need to be modified to work with django parler as follows:
    # StgIndicator.objects.filter(translations__name=self.name)
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgIndicator.objects.filter(translations__name=self.name).count() and not self.indicator_id:
            raise ValidationError({'name':_('Sorry! Indicator with this name exists')})

    def save(self, *args, **kwargs):
        super(StgIndicator, self).save(*args, **kwargs)


class StgIndicatorDomain(TranslatableModel):
    domain_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(max_length=150, blank=False, null=False,
            verbose_name = 'Domain Name'),  # Field name made lowercase.
        shortname = models.CharField(max_length=45, verbose_name = 'Short Name'),
        level = models.SmallIntegerField(blank=False,null=False,default=1,
            verbose_name = 'Level'),  # Field name made lowercase.SmallIntegerField
        description = models.TextField(blank=True, null=True,)
    )
    code = models.CharField(unique=True, max_length=45, blank=True,
        null=True, verbose_name = 'Domain Code')
    parent = models.ForeignKey('self', models.PROTECT, blank=True, null=True,
        verbose_name = 'Parent Domain')  # Field name made lowercase.
    # this field establishes a many-to-many relationship with the domain table
    indicators = models.ManyToManyField(StgIndicator,
        db_table='stg_indicator_domain_members',blank=True,
        verbose_name = 'Indicators')  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'stg_indicator_domain'
        verbose_name = 'Indicator Domain'
        verbose_name_plural = ' Indicator Domains'
        ordering = ('code', )

    def __str__(self):
        return self.name #ddisplay disagregation options

class FactDataIndicator(models.Model):
  # discriminator for ownership of data this was decided on 13/12/2019 with Gift
    DATAOWNER_CHOICES = (
        (1, 'Country'),
        (2,'AFRO'),
    )
    fact_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    indicator = models.ForeignKey(StgIndicator, models.PROTECT,
        verbose_name = 'Indicator Name',)  # Field name made lowercase.
    location = models.ForeignKey(StgLocation, models.PROTECT,
        verbose_name = 'Location Name')  # Field name made lowercase.
    categoryoption = models.ForeignKey(StgCategoryoption, models.PROTECT,blank=False,
        verbose_name = 'Modality', default=999)  # Field name made lowercase.
    # This field is used to lookup sources of data such as routine systems, census and surveys
    datasource = models.ForeignKey(StgDatasource, models.PROTECT,
        verbose_name = 'Data Source')  # Field name made lowercase.
    # This field is used to lookup the type of data required such as text, integer or float
    valuetype = models.ForeignKey(StgValueDatatype, models.PROTECT,
        null=False,blank=False,default=999,verbose_name = 'Data Type')  # Field name made lowercase.
    numerator_value = models.DecimalField(max_digits=20, decimal_places=2,
        blank=True, null=True, verbose_name = _('Numerator'))  # Field name made lowercase.
    denominator_value = models.DecimalField(max_digits=20,decimal_places=2,
        blank=True, null=True, verbose_name = 'Denominator')  # Field name made lowercase.
    value_received = DecimalField(max_digits=20,decimal_places=2,
        blank=True, null=False, verbose_name = 'Value')  # Field name made lowercase.
    min_value = models.DecimalField(max_digits=20,decimal_places=2,
        blank=True, null=True,verbose_name = 'Minimum Value')  # Field name made lowercase.
    max_value = models.DecimalField(max_digits=20,decimal_places=2,
        blank=True, null=True, verbose_name = 'Maximum Value')  # Field name made lowercase.
    target_value = models.DecimalField(max_digits=20,decimal_places=2,
        blank=True, null=True,verbose_name = 'Target Value')  # Field name made lowercase.
    start_period = models.IntegerField(null=False,blank=False,
        verbose_name='Start Year', default=datetime.date.today().year,#extract current date year value only
        help_text="This Year marks the start of reporting period")
    end_period  = models.IntegerField(null=False,blank=False,
        verbose_name='Ending Year', default=datetime.date.today().year, #extract current date year value only
        help_text="This marks the end of reporting. The value must be current \
            year or greater than the start year")
    period = models.CharField(max_length=25,blank=True,null=False,
        verbose_name = 'Period') #try to concatenate period field
    comment = models.CharField(max_length=10, choices= STATUS_CHOICES,
        default=STATUS_CHOICES[0][0], verbose_name='Approval Status')  # Field name made lowercase.
    string_value= models.CharField(max_length=500,blank=True,null=True,
        verbose_name = 'Remarks') # davy's request as of 30/4/2019
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        permissions = (
            ("approve_factdataindicator","Can approve Indicator Data"),
            ("reject_factdataindicator","Can reject Indicator Data"),
            ("pend_factdataindicator","Can pend Indicator Data")
        )

        managed = True
        db_table = 'fact_data_indicator'
        verbose_name = 'Indicator Record'
        verbose_name_plural = '  Single-Record Form'
        ordering = ('indicator__name','location__name')
        unique_together = ('indicator', 'location', 'categoryoption','datasource',
            'period',) #enforces concatenated unique constraint

    def __str__(self):
         return str(self.indicator)

    """
    The purpose of this method is to compare the start_period to the end_period. If the
    start_period is greater than the end_period athe model should show an inlines error
    message and wait until the user corrects the mistake.
    """

    def clean(self): # Don't allow end_period to be greater than the start_period.
        if self.start_period <=1990 or self.start_period > datetime.date.today().year:
            raise ValidationError({'start_period':_(
                'Sorry! Start year cannot be less than 1990 or greater than current Year ')})
        elif self.end_period <=1990 or self.end_period > datetime.date.today().year:
            raise ValidationError({'end_period':_(
                'Sorry! The ending year cannot be lower than the start year or \
                greater than the current Year ')})
        elif self.end_period < self.start_period and self.start_period is not None:
            raise ValidationError({'end_period':_(
                'Sorry! Ending period cannot be lower than the start period. \
                 Please make corrections')})

        #This logic ensures that a maximum value is provided for a corresponing minimum value
        if self.min_value is not None and self.min_value !='':
            if self.max_value is None or self.max_value < self.min_value:
                raise ValidationError({'max_value':_(
                    'Data Integrity Problem! You must provide a Maximum that is \
                     greater that Minimum value ')})
            elif self.value_received is not None and self.value_received <= self.min_value:
                raise ValidationError({'min_value':_(
                    'Data Integrity Problem! Minimum value cannot be greater \
                     that the nominal value')})

        value_type= getattr( self.valuetype, 'code') #get value name of the value_type attribute

        data_value = FactDataIndicator.value_received

        if value_type =='AVT0001':
            if self.value_received is not None and self.value_received !='':
                data_value = int(self.value_received)
            if not isinstance(data_value, int):
                raise ValidationError({'value_received':_('The value provided must be \
                    an integer')})
        elif value_type =='AVT0002':
            if self.value_received is not None and self.value_received !='':
                data_value = round(float(self.value_received),2)
        elif value_type =='AVT0003':
            if self.value_received is not None and self.value_received !='':
                data_value = None
                raise ValidationError({'value_received':_('This value must be \
                    left blank if comment is provided in place of values')})

        if value_type =='AVT0003' and self.value_received is None:
                raise ValidationError({'string_value':_('Please provide comments \
                    for missing numeric indicator value')})

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
    This method overrides the save method to store the derived field into database.
    Note that the last line calls the super class FactDataIndicator to save the value
    """
    def save(self, *args, **kwargs):
        self.period = self.get_period()
        super(FactDataIndicator, self).save(*args, **kwargs)

# These proxy classes are used to register menu in the admin for tabular entry
class IndicatorProxy(StgIndicator):
    """
    Creates permissions for proxy models which are not created automatically by
    'django.contrib.auth.management.create_permissions'.Since we can't rely on
    'get_for_model' we must fallback to  'get_by_natural_key'. However, this
    method doesn't automatically create missing 'ContentType' so we must ensure
    all the models' 'ContentType's are created before running this method.
    We do so by unregistering the 'update_contenttypes' 'post_migrate' signal
    and calling it in here just before doing everything.
    """
    def create_proxy_permissions(app, created_models, verbosity, **kwargs):
        update_contenttypes(app, created_models, verbosity, **kwargs)
        app_models = models.get_models(app)
        # The permissions we're looking for as (content_type, (codename, name))
        searched_perms = list()
        # The codenames and ctypes that should exist.
        ctypes = set()
        for model in app_models:
            opts = model._meta
            if opts.proxy:
                # Can't use 'get_for_model' here since it doesn't return correct 'ContentType' for proxy models
                # See https://code.djangoproject.com/ticket/17648
                app_label, model = opts.app_label, opts.object_name.lower()
                ctype = ContentType.objects.get_by_natural_key(app_label, model)
                ctypes.add(ctype)
                for perm in _get_all_permissions(opts, ctype):
                    searched_perms.append((ctype, perm))

        # Find all the Permissions that have a content_type for a model we're looking for.
        #We don't need to check for codenames since we already have a list of the ones we're going to create.
        all_perms = set(Permission.objects.filter(
            content_type__in=ctypes,
        ).values_list(
            "content_type", "codename"
        ))

        objs = [
            Permission(codename=codename, name=name, content_type=ctype)
            for ctype, (codename, name) in searched_perms
            if (ctype.pk, codename) not in all_perms
        ]
        Permission.objects.bulk_create(objs)
        if verbosity >= 2:
            for obj in objs:
                sys.stdout.write("Adding permission '%s'" % obj)
        models.signals.post_migrate.connect(create_proxy_permissions)
        models.signals.post_migrate.disconnect(update_contenttypes)

    class Meta:
        managed = False
        verbose_name = 'Data Grid Form'
        verbose_name_plural = '   Multi-records Grid'
        proxy = True

    """
    This def clean (self) method was contributed by Daniel Mbugua to resolve
    the issue of parent-child saving issue in the multi-records entry form.
    My credits to Mr Mbugua of MSc DCT, UoN-Kenya
    """
    def clean(self): #Appreciation to Daniel M.
        pass
