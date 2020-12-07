from rest_framework import serializers
from WebAnalyzer.models import *


class MultiModalSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MultiModalModel
        fields = ('video', 'video_url', 'aggregation_result', 'token', 'uploaded_date', 'updated_date', 'result')
        read_only_fields = ('token', 'uploaded_date', 'updated_date', 'result')