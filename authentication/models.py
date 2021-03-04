"""
The two classes in this module overrides original Django User and Group classess.
"""
from django.db import models
from django.contrib.auth.models import Group, AbstractUser
from django.utils.translation import gettext_lazy as _ # The _ is alias for gettext
from regions.models import StgLocation

def make_choices(values):
    return [(v, v) for v in values]


"""
This model class overrides the original Django user model.
"""
class CustomUser(AbstractUser):
    GENDER = ( 'Male','Female', 'Other')
    TITLE = ( 'Mr.','Ms.', 'Mrs.','Dr.', 'Prof.', 'Other')
    title = models.CharField(_('title'),max_length=45, choices=make_choices(TITLE),
        default=GENDER[0])  # Field name made lowercase.
    gender = models.CharField(_('gender'),max_length=45, choices=make_choices(GENDER),
        default=GENDER[0])  # Field name made lowercase.
    email = models.EmailField(_('e-mail'),unique=True,blank=False, null=False)
    postcode = models.CharField(_('postal code'),blank=True, null=True,max_length=6)
    username = models.CharField(_('user name'),blank=False, null=False, max_length=150)
    location = models.ForeignKey(StgLocation, models.PROTECT,default=1,
        verbose_name = _('Location Name'))  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = _('Date Created'))
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = _('Date Modified'))

    REQUIRED_FIELDS = ['location', 'username']
    USERNAME_FIELD = 'email' #can also be replaced using username as unique identifier but issue is controlling redundancy

    class Meta:
        managed = True
        verbose_name = _('User')
        verbose_name_plural = _('  User Accounts')
        ordering = ('username', )

    def __str__(self):
        return self.email


"""
This model class overrides the original Django Users Group auth model.
"""
class CustomGroup(Group):
    role = models.OneToOneField('auth.Group', parent_link=True,unique=True,
        on_delete=models.CASCADE,verbose_name=_('System Role'))
    roles_manager = models.CharField(_('Roles Manager'),max_length=70, blank=False,
        default="Staff")
    location = models.ForeignKey(StgLocation, models.PROTECT,
        verbose_name = _('Role Manager Location'))  # Field name made lowercase.
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = _('Date Created'))
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = _('Date Modified'))

    class Meta:
        managed = True
        verbose_name = _('System Role')
        verbose_name_plural = _(' System Roles')


# This model class maps to a database View that looks up the django_admin logs,
# location, customuser and group hence reason its managed meta is False
class AhodctUserLogs(models.Model):
    username = models.CharField(_('Username'),blank=False, null=False,
        max_length=150)
    email = models.EmailField(unique=True,blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=True,
        verbose_name=_("First Name"))
    last_name= models.CharField(max_length=150, blank=True,
        verbose_name=_("Last Name"))
    location_translation = models.CharField(max_length=230, blank=True,
        verbose_name=_("Location "))
    app_label = models.CharField(max_length=150, blank=True,
        verbose_name=_("Menu Executed"))
    record_name= models.CharField(max_length=200, blank=True,
        default=_("Affected Record"))
    action= models.CharField(max_length=9, blank=True,
        default=_("Action Taken"))
    action_time=models.DateTimeField(blank=True,
        verbose_name = _('Action Timestamp'))
    last_login = models.DateTimeField(blank=True,
        verbose_name = _('Last Login Timestamp'))

    class Meta:
        managed = False
        db_table = 'dct_users_log'
        verbose_name = _('View Users Log')
        verbose_name_plural = _(' View User Logs')
        ordering = ('username', )

    def __str__(self):
        return self.first_name
