from django.db import models
import uuid
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ # The _ is alias for gettext
from parler.models import TranslatableModel, TranslatedFields
from django.core.exceptions import ValidationError

class StgCategoryParent(TranslatableModel):
    """This model has stgcategory data"""
    category_id = models.AutoField(primary_key=True, verbose_name = 'Category Name')  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(max_length=230, blank=False, null=False,
            verbose_name = _('Category')),  # Field name made lowercase.
        shortname = models.CharField(max_length=50, blank=True, null=True,
            verbose_name = 'Short Name'),  # Field name made lowercase.
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
        verbose_name_plural = _('Disaggregation Categories')
        #ordering = ('name', )

    def __str__(self):
        return self.name #ddisplay disagregation Categories

class StgCategoryoption(TranslatableModel):
    categoryoption_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    category = models.ForeignKey(StgCategoryParent, models.PROTECT,
        verbose_name = 'Disaggregation Category')  # Field name made lowercase.
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
        verbose_name_plural = _('Disaggregation Options')
        #ordering = ('code', 'name', )

    def __str__(self):
        return self.name #ddisplay disagregation options

class StgDatasource(TranslatableModel):
    datasource_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(max_length=230, blank=False, null=False,
            verbose_name = 'Data Source'),  # Field name made lowercase.
        shortname = models.CharField(max_length=50, blank=True, null=True,
            verbose_name = 'Short Name'),  # Field name made lowercase.
        description = models.TextField( blank=False, null=False,
            default='No specific definition')
    )
    code = models.CharField(unique=True, max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'stg_datasource'
        verbose_name = 'Data Source'
        verbose_name_plural = 'Data Sources'
        #ordering = ('code', )

    def __str__(self):
        return self.name #display the data source name

    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgDatasource.objects.filter(translations__name=self.name).count() and not self.datasource_id:
            raise ValidationError({'name':_('Sorry! This data source exists')})


class StgValueDatatype(TranslatableModel):
    valuetype_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(max_length=50, verbose_name = 'Value Name'),  # Field name made lowercase.
        shortname = models.CharField(max_length=50, blank=True, null=True,
            verbose_name = 'Short Name'),  # Field name made lowercase.
        description = models.TextField(blank=True, null=True)
    )
    code = models.CharField(unique=True, max_length=50)  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
         managed = True
         db_table = 'stg_value_datatype'
         verbose_name = ' Data Value'
         verbose_name_plural = 'Data Value Types'
         #ordering = ('name', )

    def __str__(self):
         return self.name #ddisplay disagregation options


class StgMeasuremethod(TranslatableModel):
    measuremethod_id = models.AutoField(primary_key=True)
    translations = TranslatedFields(
        name = models.CharField(max_length=230, blank=False, null=False,
            verbose_name = 'Name'),  # Field name made lowercase.
        measure_value = models.DecimalField(max_digits=50, decimal_places=0,
            blank=True, null=True, verbose_name = 'Measure Type'),  # Field name made lowercase.
        description = models.TextField(max_length=200, blank=True, null=True)
    )
    code = models.CharField(max_length=50,unique=True, blank=True, null=False),  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'stg_measuremethod'
        verbose_name = ' Measure Type'
        verbose_name_plural = 'Indicator Measure Types'
        #ordering = ('name', )

    def __str__(self):
        return self.name #ddisplay measurement methods
