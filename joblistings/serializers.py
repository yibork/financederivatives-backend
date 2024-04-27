# serializers.py
from rest_framework import serializers
from .models import JobPage

class JobPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPage
        fields = '__all__'
