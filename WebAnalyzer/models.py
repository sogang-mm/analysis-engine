from django.db import models

# Create your models here.
from rest_framework import exceptions
from AnalysisModule.config import DEBUG
from WebAnalyzer.tasks import analyzer_by_data
from WebAnalyzer.utils import filename
from django_mysql.models import JSONField

import ast


class MultiModalModel(models.Model):
    video = models.FileField(upload_to=filename.default, null=True)
    video_url = models.TextField(null=True)
    aggregation_result = models.TextField(null=False)
    token = models.AutoField(primary_key=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    result = JSONField(null=True)

    def save(self, *args, **kwargs):
        super(MultiModalModel, self).save(*args, **kwargs)

        if DEBUG:
            task_get = ast.literal_eval(str(analyzer_by_data(self.aggregation_result)))
        else:
            task_get = ast.literal_eval(str(analyzer_by_data.delay(self.aggregation_result).get()))

        self.result = task_get
        super(MultiModalModel, self).save()