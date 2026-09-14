from django.core.management.base import BaseCommand

from devices.models import Racer, Rig
from races.models import Race, RaceEntry


class Command(BaseCommand):
    help = 'Create a small local demo grid for the dashboard.'

    def handle(self, *args, **options):
        racers = []
        for name in ['Lohith', 'Pranav', 'Rahul', 'Arjun']:
            racer, _ = Racer.objects.get_or_create(name=name)
            racers.append(racer)

        rigs = []
        for index, name in enumerate(['Apex One', 'Northstar', 'Velocity Lab'], 1):
            rig, _ = Rig.objects.update_or_create(
                name=name,
                defaults={
                    'display_name': ['Ferrari Simulator 01', 'Red Bull Rig', 'Motion Rig 01'][index - 1],
                    'hostname': f'RACING-PC-0{index}',
                    'ip_address': f'192.168.1.{100 + index}',
                    'status': 'online',
                    'provider': 'mock',
                    'assigned_racer': racers[index - 1],
                    'current_game': 'F1 25',
                    'game_detection_mode': 'manual',
                },
            )
            rigs.append(rig)

        race, created = Race.objects.get_or_create(
            name='Friday Night Sprint',
            defaults={'simulator': 'F1 25', 'track': 'Circuit de Spa', 'total_laps': 12, 'status': 'ready'},
        )
        if created:
            for position, rig in enumerate(rigs, 1):
                RaceEntry.objects.create(
                    race=race,
                    rig=rig,
                    racer=rig.assigned_racer,
                    driver_name=rig.assigned_racer.name if rig.assigned_racer else 'Unassigned',
                    car=['GT3 R', 'AMG GT3', '911 GT3'][position - 1],
                    grid_position=position,
                    position=position,
                )
        self.stdout.write(self.style.SUCCESS(f'Demo data ready: {race.name}'))
