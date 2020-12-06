# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from WebAnalyzer import models

admin.site.register(models.ImageModel)
admin.site.register(models.VideoModel)
admin.site.register(models.FrameModel)
admin.site.register(models.AudioModel)