from django.db import models
import uuid
from datetime import datetime #for handling year part of date filed
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ # The _ is alias for gettext
from parler.models import TranslatableModel,TranslatedFields
from regions.models import StgLocation

def make_choices(values):
    return [(v, v) for v in values]

# New model to take care of resource types added 11/05/2019 courtesy of Gift
class StgResourceType(TranslatableModel):
    type_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(max_length=230, blank=False, null=False,
            verbose_name = 'Resource Type Name'),  # Field name made lowercase.
        description = models.TextField(blank=True, null=True,
            verbose_name = 'Description')  # Field name made lowercase.
    )
    code = models.CharField(unique=True, max_length=50, blank=True,
        null=True, verbose_name = 'Code')  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'stg_resource_type'
        verbose_name = 'Type'
        verbose_name_plural = 'Resource Types'
        ordering = ('code', )

    def __str__(self):
        return self.name #display the knowledge product category name


class StgKnowledgeProduct(TranslatableModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    BROAD_CATEGORY_CHOICES = (
        ('toolkit', 'Toolkit'),
        ('publication', 'Publication'),
    )
    product_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    type = models.ForeignKey(StgResourceType, models.PROTECT,blank=False,
        null=False,verbose_name = 'Resource Type')
    translations = TranslatedFields(
        title = models.CharField(max_length=230,blank=False, null=False,
            verbose_name = 'Title'),  # Field name made lowercase.
        categorization = models.CharField(max_length=15,choices= BROAD_CATEGORY_CHOICES,
            default=BROAD_CATEGORY_CHOICES[0][0],verbose_name='Categorization',
            help_text="You must specify the published resource as a scienctific \
            publication or a toolkit.Toolkit are resources like  M&E Guides "),  # Field name made lowercase.
        description = models.TextField(blank=True, null=True),  # Field name made lowercase.
        abstract = models.TextField(blank=True, null=True),  # Field name made lowercase.
        author = models.CharField(max_length=200, blank=False, null=False,
            verbose_name='Author/Owner'),  # Field name made lowercase.
        year_published = models.IntegerField(default=datetime.now().year,
            verbose_name='Year Published'),

    )  # End of translatable fields
    internal_url = models.FileField (upload_to='media/files',
        verbose_name = 'File', blank=True,)  # For uploading the resource into products repository.
    external_url = models.CharField(blank=True, null=True, max_length=2083)
    cover_image = models.ImageField(upload_to='media/images',
            verbose_name = 'Image', blank=True,) #for thumbnail..requires pillow
    location = models.ForeignKey(StgLocation, models.PROTECT, blank=False,
        null=False,verbose_name = 'Publisher Location', default = 1)  # Field cannot be deleted without deleting its dependants
    comment = models.CharField(max_length=10, choices= STATUS_CHOICES,
        default=STATUS_CHOICES[0][0], verbose_name='Status')
    code = models.CharField(unique=True, blank=True,null=False,max_length=45)
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        permissions = (
            ("approve_stgknowledgeproduct", "Can approve stgknowledgeproduct"),
            ("reject_stgknowledgeproduct", "Can reject stgknowledgeproduct"),
            ("pend_stgknowledgeproduct", "Can pend stgknowledgeproduct")
        )
        managed = True
        db_table = 'stg_knowledge_product'
        verbose_name = 'Knowledge Resource'
        verbose_name_plural = '  Knowledge Resources'
        ordering = ('code', )
        #unique_together = ('title','author','year_published',)

    def __str__(self):
        return self.title #display the data element name

    def clean(self): # Don't allow end_period to be greater than the start_period.
        import datetime
        if self.year_published <=1900 or self.year_published > datetime.date.today().year:
            raise ValidationError({'year_published':_(
                'Sorry! The publishing year cannot be lower than 1900 or \
                 greater than the current Year ')})

        if StgKnowledgeProduct.objects.filter(
            translations__title=self.title).count() and not self.product_id and not \
                self.year_published and not self.location:
            raise ValidationError({'title':_('Knowledge resource with the same \
                title already exists')})

    def save(self, *args, **kwargs):
        super(StgKnowledgeProduct, self).save(*args, **kwargs)


class StgProductDomain(TranslatableModel):
    domain_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    translations = TranslatedFields(
        name = models.CharField(max_length=230, blank=False, null=False,
            verbose_name = 'Domain Name'),  # Field name made lowercase.
        shortname = models.CharField(max_length=45,null=True,
            verbose_name = 'Short Name',),  # Field name made lowercase.
        description = models.TextField(blank=True, null=True),
        level = models.IntegerField(default=1,verbose_name='Level')
        )
    code = models.CharField(unique=True, max_length=50, blank=True,
            null=True, verbose_name = 'Domain Code')  # Field name made lowercase.
    parent = models.ForeignKey('self',on_delete=models.CASCADE,
        blank=True,null=True,verbose_name = 'Parent Domain')  # Field name made lowercase.
    publications = models.ManyToManyField(StgKnowledgeProduct,
        db_table='stg_product_domain_members',
        blank=True,verbose_name = 'Publications')  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True # must be true to create the model table in mysql
        db_table = 'stg_publication_domain'
        verbose_name = 'Resource Category'
        verbose_name_plural = ' Resource Categories'
        ordering = ('code', )

    def __str__(self):
        return self.name #display the knowledge product category name

    def clean(self):
        if StgProductDomain.objects.filter(
            translations__name=self.name).count() and not self.domain_id and not \
                self.code:
            raise ValidationError({'name':_('Resource Category with the same \
                name already exists')})

    def save(self, *args, **kwargs):
        super(StgProductDomain, self).save(*args, **kwargs)
