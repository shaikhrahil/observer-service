from rest_framework import serializers

from .models import Observer


class ObserverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observer
        fields = "__all__"
