from django.db import models

from devices.models import Racer, Rig


class Race(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('running', 'Running'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=160)
    simulator = models.CharField(max_length=80, default='F1 25', blank=True)
    track = models.CharField(max_length=160, blank=True)
    total_laps = models.PositiveIntegerField(default=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def winner(self):
        winner = self.entries.order_by('position', 'grid_position').first()
        if winner is None:
            return None
        return winner

    def __str__(self):
        return self.name


class RaceEntry(models.Model):
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('racing', 'Racing'),
        ('finished', 'Finished'),
        ('dnf', 'DNF'),
    ]

    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='entries')
    rig = models.ForeignKey(Rig, on_delete=models.PROTECT, related_name='race_entries')
    racer = models.ForeignKey(Racer, null=True, blank=True, on_delete=models.SET_NULL, related_name='race_entries')
    driver_name = models.CharField(max_length=120, blank=True)
    car = models.CharField(max_length=120, blank=True)
    grid_position = models.PositiveIntegerField(default=1)
    position = models.PositiveIntegerField(default=1)
    current_lap = models.PositiveIntegerField(default=0)
    lap_time = models.FloatField(null=True, blank=True)
    total_time = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    telemetry = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['position', 'grid_position']
        constraints = [
            models.UniqueConstraint(fields=['race', 'rig'], name='unique_rig_per_race'),
        ]

    @property
    def display_driver_name(self):
        if self.racer:
            return self.racer.name
        return self.driver_name or 'Unassigned'

    def __str__(self):
        return f'{self.display_driver_name} in {self.race.name}'
