# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login_app.models import User
from datetime import datetime
# Create your models here.
class Travel(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    users = models.ManyToManyField(User, related_name='trips')
