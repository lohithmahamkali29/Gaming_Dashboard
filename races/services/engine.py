from django.utils import timezone

from telemetry.services.manager import TelemetryManager


class RaceEngine:
    def __init__(self, telemetry_manager=None):
        self.telemetry = telemetry_manager or TelemetryManager()

    def start(self, race):
        race.status = 'running'
        race.started_at = timezone.now()
        race.save(update_fields=['status', 'started_at', 'updated_at'])
        race.entries.update(status='racing')
        for entry in race.entries.select_related('rig').all():
            if entry.rig:
                entry.rig.status = 'racing'
                entry.rig.last_seen = timezone.now()
                entry.rig.metadata['last_telemetry'] = timezone.now().isoformat()
                entry.rig.metadata['telemetry_status'] = 'ACTIVE'
                entry.rig.metadata['packets_received'] = entry.rig.metadata.get('packets_received', 0) + 1
                entry.rig.save(update_fields=['status', 'last_seen', 'metadata', 'updated_at'])
        return race

    def tick(self, race):
        if race.status != 'running':
            return []
        entries = list(race.entries.select_related('rig').all())
        snapshots = []
        for entry in entries:
            snapshot = self.telemetry.read(entry.rig)
            entry.current_lap = min(snapshot.lap, race.total_laps)
            entry.lap_time = snapshot.lap_time
            entry.total_time = snapshot.total_time
            entry.telemetry = snapshot.as_dict()
            entry.status = 'finished' if entry.current_lap >= race.total_laps else 'racing'
            entry.save(update_fields=['current_lap', 'lap_time', 'total_time', 'telemetry', 'status'])
            entry.rig.status = 'online'
            entry.rig.last_seen = timezone.now()
            entry.rig.metadata['last_telemetry'] = timezone.now().isoformat()
            entry.rig.metadata['telemetry_status'] = 'ACTIVE'
            entry.rig.metadata['packets_received'] = entry.rig.metadata.get('packets_received', 0) + 1
            entry.rig.metadata['last_error'] = None
            entry.rig.save(update_fields=['status', 'last_seen', 'metadata', 'updated_at'])
            snapshots.append(entry)
        for position, entry in enumerate(sorted(snapshots, key=lambda item: (-item.current_lap, -item.telemetry.get('position', 0))), 1):
            if entry.position != position:
                entry.position = position
                entry.save(update_fields=['position'])
        return snapshots
