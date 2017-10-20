
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from river.models.fields.state import StateField
from river.models.managers.workflow_object import WorkflowObjectManager
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import Group, User


class Application(models.Model):
    name_application = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name_application


class TypeRequest(models.Model):
    application = models.ForeignKey(Application)
    type_request = models.CharField(max_length=200)

    def __unicode__(self):
        return self.type_request


#class Location(models.Model):
    #name_location = models.CharField(max_length=200)

    #def __unicode__(self):
        #return self.name_location


class TicketRequest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default="")
    author = models.ForeignKey('auth.User')
    published_date = models.DateTimeField(blank=True, null=True)
    application = models.ForeignKey(Application)
    type = models.ForeignKey(TypeRequest)
    status = StateField(editable=False)
    #type = ChainedForeignKey(
        #TypeRequest,
        #chained_field="application",
        #chained_model_field="application",
        #show_all=False,
        #auto_choose=True,
        #sort=True,)
    #location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.title
