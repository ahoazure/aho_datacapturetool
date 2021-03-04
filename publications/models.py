from django.db import models
import uuid
from datetime import datetime #for handling year part of date filed
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ # The _ is alias for gettext
from parler.models import TranslatableModel,TranslatedFields
from regions.models import StgLocation
from authentication.models import CustomUser

def make_choices(values):
    return [(v, v) for v in values]

# Model to take care of resource types added 11/05/2019 courtesy of Gift
class StgResourceType(TranslatableModel):
    type_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    translations = TranslatedFields(
        name = models.CharField(_('Type Name'),max_length=230, blank=False,
            null=False),  # Field name made lowercase.
        shortname = models.CharField(_('Short Name'),max_length=100, blank=True,
            null=True),
        description = models.TextField(_('Brief Description'),blank=True,
            null=True)  # Field name made lowercase.
    )
    code = models.CharField(_('Code'),unique=True, max_length=50, blank=True,
        null=True)  # Field name made lowercase.
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = 'stg_resource_type'
        verbose_name = _('Resource Type')
        verbose_name_plural = _('Resource Types')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #display the knowledge product category name

    def clean(self):
        if StgResourceType.objects.filter(
            translations__name=self.name).count() and not self.type_id and not \
                self.code:
            raise ValidationError({'name':_('Resource type with the same \
                name exists')})

    def save(self, *args, **kwargs):
        super(StgResourceType, self).save(*args, **kwargs)


# New model to take care of resource types added 11/05/2019 courtesy of Gift
class StgResourceCategory(TranslatableModel):
    category_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    translations = TranslatedFields(
        name = models.CharField(_('Category Name'),max_length=230, blank=False,
            null=False),  # Field name made lowercase.
        shortname = models.CharField(_('Short Name'),max_length=100, blank=True,
            null=True),
        description = models.TextField(_('Description'),blank=True,
            null=True)  # Field name made lowercase.
    )
    code = models.CharField(_('Code'),unique=True, max_length=50, blank=True,
        null=True)  # Field name made lowercase.
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)

    class Meta:
        managed = True
        db_table = 'stg_resource_category'
        verbose_name = _('Resource Category')
        verbose_name_plural = _(' Resource Categories')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #display the knowledge product category name

    def clean(self):
        if StgResourceCategory.objects.filter(
            translations__name=self.name).count() and not self.category_id and not \
                self.code:
            raise ValidationError({'name':_('Resource category with the same \
                name exists')})

    def save(self, *args, **kwargs):
        super(StgResourceCategory, self).save(*args, **kwargs)


class StgKnowledgeProduct(TranslatableModel):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    )

    product_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(CustomUser, models.PROTECT,blank=False,
		verbose_name = 'User Name (Email)',default=2) ## request helper fie
    type = models.ForeignKey(StgResourceType, models.PROTECT,blank=False,
        null=False,verbose_name = _('Resource Type'))
    categorization = models.ForeignKey(StgResourceCategory,models.PROTECT,
        blank=False,verbose_name=_('Resource Category'),default = 1)
    translations = TranslatedFields(
        title = models.CharField(_('Title'),max_length=500,blank=False, null=False),
        description = models.TextField(_('Brief Description'),blank=True, null=True),
        abstract = models.TextField(_('Abstract/Summary'),blank=True, null=True),
        author = models.CharField(_('Author/Owner'),max_length=200, blank=False,
            null=False),  # Field name made lowercase.
        year_published = models.IntegerField(_('Year Published'),
            default=datetime.now().year),

    )  # End of translatable fields
    code = models.CharField(unique=True, blank=True,null=False,max_length=45)
    internal_url = models.FileField (_('File'),upload_to='media/files',
        blank=True,)  # For uploading the resource into products repository.
    external_url = models.CharField(blank=True, null=True, max_length=2083)
    cover_image = models.ImageField(_('Cover Picture'),upload_to='media/images',
        blank=True,) #for thumbnail..requires pillow
    location = models.ForeignKey(StgLocation, models.PROTECT, blank=False,
        null=False,verbose_name = _('Resource Location'), default = 1)  # Field cannot be deleted without deleting its dependants
    comment = models.CharField(_('Status'),max_length=10, choices= STATUS_CHOICES,
        default=STATUS_CHOICES[0][0])
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)

    class Meta:
        permissions = (
            ("approve_stgknowledgeproduct", "Can approve stgknowledgeproduct"),
            ("reject_stgknowledgeproduct", "Can reject stgknowledgeproduct"),
            ("pend_stgknowledgeproduct", "Can pend stgknowledgeproduct")
        )
        managed = True
        db_table = 'stg_knowledge_product'
        verbose_name = _('Knowledge Resource')
        verbose_name_plural = _('   Knowledge Resources')
        ordering = ('translations__title',)

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
    LEVEL = (
    (1,_('level 1')),
    (2,_('level 2')),
    (3,_('level 3')),
    (4,_('level 4')),
    (5,_('level 5')),
    (6,_('level 6')),
    )
    domain_id = models.AutoField(primary_key=True)
    uuid = uuid = models.CharField(_('Unique ID'),unique=True,max_length=36,
        blank=False,null=False,default=uuid.uuid4,editable=False)
    translations = TranslatedFields(
        name = models.CharField(_('Resource Theme'),max_length=230, blank=False,
            null=False),
        shortname = models.CharField(_('Short Name'),max_length=45,null=True),  # Field name made lowercase.
        description = models.TextField(_('Brief Description'),blank=True,
            null=True),
        level =models.SmallIntegerField(_('Theme Level'),choices=LEVEL,
            default=LEVEL[0][0])
        )
    code = models.CharField(_('Theme Code'),unique=True, max_length=50, blank=True,
            null=True)  # Field name made lowercase.
    parent = models.ForeignKey('self',on_delete=models.CASCADE,
        blank=True,null=True,verbose_name = _('Parent Theme'))  # Field name made lowercase.
    publications = models.ManyToManyField(StgKnowledgeProduct,
        db_table='stg_product_domain_members',
        blank=True,verbose_name = _('Resources'))  # Field name made lowercase.
    date_created = models.DateTimeField(_('Date Created'),blank=True, null=True,
        auto_now_add=True)
    date_lastupdated = models.DateTimeField(_('Date Modified'),blank=True,
        null=True, auto_now=True)

    class Meta:
        managed = True # must be true to create the model table in mysql
        db_table = 'stg_publication_domain'
        verbose_name = _('Resource Theme')
        verbose_name_plural = _('  Resource Themes')
        ordering = ('translations__name',)

    def __str__(self):
        return self.name #display the knowledge product category name

    def clean(self):
        if StgProductDomain.objects.filter(
            translations__name=self.name).count() and not self.domain_id and not \
                self.code:
            raise ValidationError({'name':_('Resource Theme with the same \
                name exists')})

    def save(self, *args, **kwargs):
        super(StgProductDomain, self).save(*args, **kwargs)
