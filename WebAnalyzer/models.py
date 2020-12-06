# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.db import models

from rest_framework import exceptions

from AnalysisModule import settings
from AnalysisModule.config import DEBUG
from WebAnalyzer.tasks import analyzer_by_image, analyzer_by_video
from WebAnalyzer.utils import filename
from WebAnalyzer.utils.media import *
from django_mysql.models import JSONField
import ast


class ImageModel(models.Model):
    image = models.ImageField(upload_to=filename.default)
    token = models.AutoField(primary_key=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    result = JSONField(null=True)

    def save(self, *args, **kwargs):
        super(ImageModel, self).save(*args, **kwargs)

        if DEBUG:
            task_get = ast.literal_eval(str(analyzer_by_image(self.image.path, 'image')))
        else:
            task_get = ast.literal_eval(str(analyzer_by_image.delay(self.image.path, 'image').get()))

        self.result = task_get
        super(ImageModel, self).save()


class VideoModel(models.Model):
    video = models.FileField(upload_to=filename.default, null=True)
    video_url = models.TextField(max_length=255, null=True)
    video_info = JSONField(null=True)
    video_text = models.TextField(null=True)
    extract_fps = models.IntegerField(default=1)
    analysis_type = models.TextField(max_length=255, null=False)
    token = models.AutoField(primary_key=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    result = JSONField(null=True)

    def save(self, *args, **kwargs):
        super(VideoModel, self).save(*args, **kwargs)
        if self.analysis_type == 'audio':
            audio = self.audio.create()
            data = audio.audio.path
        elif self.analysis_type == 'text':
            data = self.video_text
        else :
            if self.video_url is not None:
                video_path = self.video_url
            else :
                video_path = self.video.path
            data, urls = extract_frames(video_path, self.extract_fps)
            for frame_url in urls:
                self.frame.create(frame=frame_url)

            self.video_info = get_video_metadata(video_path)
            video_info = {
                "video_info": self.video_info,
                "frame_urls": urls
            }

        if DEBUG:
            task_get = ast.literal_eval(str(analyzer_by_video(data, video_info, self.analysis_type)))
        else:
            task_get = ast.literal_eval(str(analyzer_by_video.delay(data, video_info, self.analysis_type).get()))

        self.result = task_get
        super(VideoModel, self).save()


class AudioModel(models.Model):
    video = models.ForeignKey(VideoModel, related_name='audio', on_delete=models.CASCADE, null=True)
    audio = models.FileField(upload_to=filename.default)
    token = models.AutoField(primary_key=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(AudioModel, self).save(*args, **kwargs)
        if self.video != None:
            audio_path = extract_audio(self.video.video_url)
            self.audio = audio_path

        super(AudioModel, self).save()


class FrameModel(models.Model):
    video = models.ForeignKey(VideoModel, related_name='frame', on_delete=models.CASCADE, null=True)
    frame = models.ImageField(max_length=255)