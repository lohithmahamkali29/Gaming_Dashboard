from rest_framework import serializers

from devices.models import Racer
from .models import Race, RaceEntry


class RaceEntrySerializer(serializers.ModelSerializer):
    rig_name = serializers.CharField(source='rig.label', read_only=True)
    driver_name = serializers.SerializerMethodField()
    racer = serializers.PrimaryKeyRelatedField(queryset=Racer.objects.all(), required=False, allow_null=True)

    class Meta:
        model = RaceEntry
        fields = '__all__'

    def get_driver_name(self, obj):
        return obj.display_driver_name


class RaceSerializer(serializers.ModelSerializer):
    entries = RaceEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Race
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
