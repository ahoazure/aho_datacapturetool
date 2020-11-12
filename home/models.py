from django.db import models
import uuid
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ # The _ is alias for gettext
from parler.models import TranslatableModel, TranslatedFields
from django.core.exceptions import ValidationError

class StgCategoryParent(TranslatableModel):
    """This model has stgcategory data"""
    category_id = models.AutoField(_('Category Name'),primary_key=True,)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,
        max_length=36, blank=False, null=False,default=uuid.uuid4,editable=False,)
    translations = TranslatedFields(
        name = models.CharField(_('Category Name'),max_length=230, blank=False,
            null=False),  # Field name made lowercase.
        shortname = models.CharField(_('Short Name'),max_length=50, blank=True,
            null=True,),
        description = models.TextField(blank=True, null=True)  # Field name made lowercase.
    )
    code = models.CharField(unique=True, max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'stg_category_parent'
        verbose_name = _('Disaggregation Category')
        verbose_name_plural = _('  Disaggregation Categories')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #ddisplay disagregation Categories


class StgCategoryoption(TranslatableModel):
    categoryoption_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name =_('Unique ID'))  # Field name made lowercase.
    category = models.ForeignKey(StgCategoryParent, models.PROTECT,
        verbose_name = _('Category Name'))  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(max_length=230, blank=False, null=False,
            verbose_name = _('Modality Name')),  # Field name made lowercase.
        shortname = models.CharField(max_length=50, blank=True, null=True,
            verbose_name = _('Short Name')),  # Field name made lowercase.
        description = models.TextField(blank=True, null=True)  # Field name made lowercase.
    )
    code = models.CharField(unique=True,max_length=230, blank=True, null=False)  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'stg_categoryoption'
        verbose_name = _('Disaggregation Option')
        verbose_name_plural = _('   Disaggregation Options')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #ddisplay disagregation options

class StgDatasource(TranslatableModel):
    LEVEL_CHOICES = ( #choices for approval of indicator data by authorized users
        ('global', _('Global')),
        ('regional',_('Regional')),
        ('national',_('National')),
        ('sub-national',_('Sub-national')),
        ('unspecified',_('Non-specific'))
    )
    datasource_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Unique ID')  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(max_length=230, blank=False, null=False,
            verbose_name =_('Data Source')),  # Field name made lowercase.
        shortname = models.CharField(max_length=50, blank=True, null=True,
            verbose_name = _('Short Name')),  # Field name made lowercase.
        level = models.CharField(max_length=20,blank=False, null=False,
            choices= LEVEL_CHOICES,verbose_name =_('Source Level'),
            default=LEVEL_CHOICES[2][0],
            help_text=_("Level can be global, regional, national, subnational")),  # Field name made lowercase.
        description = models.TextField( blank=False, null=False,
            default=_('No definition'))
    )
    code = models.CharField(unique=True, max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = _('Date Created'))
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = _('Date Modified'))

    class Meta:
        managed = True
        db_table = 'stg_datasource'
        verbose_name = _('Data Source')
        verbose_name_plural = _('    Data Sources')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #display the data source name

    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgDatasource.objects.filter(translations__name=self.name).count() and not self.datasource_id:
            raise ValidationError({'name':_('Sorry! This data source exists')})


class StgValueDatatype(TranslatableModel):
    valuetype_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = _('Unique ID'))  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(max_length=50, verbose_name =_('Value Name')),  # Field name made lowercase.
        shortname = models.CharField(max_length=50, blank=True, null=True,
            verbose_name =_('Short Name')),  # Field name made lowercase.
        description = models.TextField(blank=True, null=True)
    )
    code = models.CharField(unique=True, max_length=50)  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = _('Date Created'))
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = _('Date Modified'))

    class Meta:
         managed = True
         db_table = 'stg_value_datatype'
         verbose_name = _(' Data Value')
         verbose_name_plural = _('Data Value Types')
         ordering = ('translations__name',)

    def __str__(self):
         return self.name #ddisplay disagregation options


class StgMeasuremethod(TranslatableModel):
    measuremethod_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False, null=False,default=uuid.uuid4,editable=False)
    translations = TranslatedFields(
        name = models.CharField(_('Measure Name'),max_length=230, blank=False,
            null=False,help_text=_("Name can be indicator types like unit, \
            Percentage, Per Thousand, Per Ten Thousand,Per Hundred Thousand etc")),  # Field name made lowercase.
        measure_value = models.DecimalField(_('Ratio'),max_digits=50,
            decimal_places=0,blank=True, null=True,help_text=_("Ratio can be \
            factors like 1 for unit, 100, 1000,10000 or higher values")),
        description = models.TextField(_('Description'),max_length=200, blank=True, null=True)
    )
    code = models.CharField(max_length=50,unique=True, blank=True, null=False)  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = _('Date Created'))
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = _('Date Modified'))

    class Meta:
        managed = True
        db_table = 'stg_measuremethod'
        verbose_name = _('Measure Type')
        verbose_name_plural = _(' Measure Types')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #ddisplay measurement methods
