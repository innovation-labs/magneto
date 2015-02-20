from django.db import models

from django_extensions.db.fields import *
from jsonfield import JSONField

from apps.common.models import *


class Company(TimeStamped, SluggedFromName):
    is_active = models.BooleanField(default=True)
    users = models.ManyToManyField('users.User', 
        through='companies.CompanyUser')


class CompanyGroup(TimeStamped):
    company = models.ForeignKey('companies.Company', related_name='groups')
    permissions = JSONField()


class CompanyUser(TimeStamped):
    user = models.ForeignKey('users.User', related_name='memberships')
    group = models.ForeignKey('companies.CompanyGroup', 
        related_name='memberships')
    company = models.ForeignKey('companies.Company', related_name='memberships')

    # override default group permissions?
    is_owner = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # default membership for the views
    is_default = models.BooleanField(default=False)

    # check whether the membership is active or not
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'group', 'company')


    def __unicode__(self):
        return '%s: %s' %(self.company.name, self.user.name)

    def set_sefault(self):
        if not self.is_active:
            self.user.membership.all().update(is_active=False)
            self.is_active = True
            self.save()




