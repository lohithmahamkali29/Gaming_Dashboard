from rest_framework import serializers

from .models import Device, Racer, Rig


class RacerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Racer
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class RigSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True, read_only=True)
    assigned_racer = RacerSerializer(read_only=True)
    assigned_racer_id = serializers.PrimaryKeyRelatedField(source='assigned_racer', queryset=Racer.objects.all(), write_only=True, required=False, allow_null=True)

    class Meta:
        model = Rig
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
