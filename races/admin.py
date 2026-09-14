from django.contrib import admin

from .models import Race, RaceEntry


class RaceEntryInline(admin.TabularInline):
    model = RaceEntry
    extra = 1


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'track', 'status', 'total_laps', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'track']
    inlines = [RaceEntryInline]


@admin.register(RaceEntry)
class RaceEntryAdmin(admin.ModelAdmin):
    list_display = ['driver_name', 'race', 'rig', 'position', 'current_lap', 'status']
    list_filter = ['status']
    search_fields = ['driver_name', 'car']

    class Media:
        css = {'all': ('admin/race-entry.css',)}
