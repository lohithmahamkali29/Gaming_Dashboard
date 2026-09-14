from django.contrib import admin

from .models import Device, Racer, Rig


@admin.register(Racer)
class RacerAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'created_at']
    search_fields = ['name', 'short_name']


@admin.register(Rig)
class RigAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_name', 'status', 'assigned_racer', 'current_game', 'ip_address', 'provider', 'last_seen']
    list_filter = ['status', 'provider', 'game_detection_mode']
    search_fields = ['name', 'display_name', 'hostname', 'ip_address', 'current_game']
    raw_id_fields = ['assigned_racer']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'rig', 'device_type', 'status', 'last_seen']
    list_filter = ['device_type', 'status']
    search_fields = ['name', 'address']
