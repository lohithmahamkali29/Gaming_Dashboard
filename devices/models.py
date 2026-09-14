from django.db import models


class Racer(models.Model):
    name = models.CharField(max_length=120, unique=True)
    short_name = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Rig(models.Model):
    STATUS_CHOICES = [
        ('offline', 'Offline'),
        ('online', 'Online'),
        ('racing', 'Racing'),
    ]
    GAME_MODE_CHOICES = [
        ('manual', 'Development / Manual'),
        ('auto', 'Automatic'),
    ]

    name = models.CharField(max_length=120, unique=True)
    display_name = models.CharField(max_length=120, blank=True, help_text='Operator-facing name shown on the control surface.')
    hostname = models.CharField(max_length=255, blank=True, help_text='Machine/technical identity for the rig.')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    telemetry_port = models.PositiveIntegerField(default=20777)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline')
    provider = models.CharField(max_length=40, default='mock')
    assigned_racer = models.ForeignKey('Racer', null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_rigs')
    current_game = models.CharField(max_length=80, default='F1 25', help_text='Current simulator/runtime title for this rig.')
    game_detection_mode = models.CharField(max_length=20, choices=GAME_MODE_CHOICES, default='manual')
    metadata = models.JSONField(default=dict, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    @property
    def label(self):
        return self.display_name or self.name

    def __str__(self):
        return self.label


class Device(models.Model):
    DEVICE_TYPES = [
        ('rig', 'Rig'),
        ('display', 'Display'),
        ('controller', 'Controller'),
        ('other', 'Other'),
    ]

    rig = models.ForeignKey(Rig, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=120)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES, default='other')
    address = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default='unknown')
    metadata = models.JSONField(default=dict, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['rig__name', 'name']

    def __str__(self):
        return f'{self.rig.name} / {self.name}'
