import csv
import json
from datetime import datetime

from django.db.models import Count, Max, Min, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from devices.models import Racer, Rig
from .forms import RacerForm, RigUpdateForm
from races.models import Race, RaceEntry


def _iso_to_datetime(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _communication_row(rig, now):
    last_seen = rig.last_seen or rig.updated_at or rig.created_at
    last_telemetry = rig.metadata.get('last_telemetry') if isinstance(rig.metadata, dict) else None
    telemetry_dt = _iso_to_datetime(last_telemetry)
    age_seconds = (now - last_seen).total_seconds() if last_seen else None
    if not rig.ip_address and not rig.hostname and not rig.display_name:
        network_status = 'NOT CONFIGURED'
        telemetry_status = 'NOT CONFIGURED'
        state = 'OFFLINE'
    else:
        network_status = 'ONLINE' if age_seconds is not None and age_seconds <= 90 else 'OFFLINE' if age_seconds is not None else 'WARNING'
        if telemetry_dt is not None:
            telemetry_age = (now - telemetry_dt).total_seconds()
            telemetry_status = 'ACTIVE' if telemetry_age <= 60 else 'WARNING'
        elif rig.status == 'racing':
            telemetry_status = 'ACTIVE'
        elif rig.status == 'online':
            telemetry_status = 'WARNING'
        else:
            telemetry_status = 'DISCONNECTED'
        state = 'ONLINE' if network_status == 'ONLINE' and telemetry_status in {'ACTIVE', 'WARNING'} else 'WARNING' if network_status == 'ONLINE' else 'OFFLINE'
    if not rig.ip_address and not rig.hostname:
        telemetry_status = 'NOT CONFIGURED'
    return {
        'id': rig.id,
        'name': rig.display_name or rig.name,
        'rig_name': rig.name,
        'racer': rig.assigned_racer.name if rig.assigned_racer else 'Unassigned',
        'hostname': rig.hostname or '—',
        'ip_address': rig.ip_address or '—',
        'current_game': rig.current_game or '—',
        'network_status': network_status,
        'telemetry_status': telemetry_status,
        'status': state,
        'last_seen': last_seen.strftime('%Y-%m-%d %H:%M:%S') if last_seen else '—',
        'last_telemetry': telemetry_dt.strftime('%Y-%m-%d %H:%M:%S') if telemetry_dt else '—',
        'packets_received': int(rig.metadata.get('packets_received', 0)) if isinstance(rig.metadata, dict) else 0,
        'provider': rig.provider,
        'game_detection_mode': rig.game_detection_mode,
        'snippet': rig.metadata.get('last_error') if isinstance(rig.metadata, dict) else None,
        'heartbeat': 'CONNECTED' if network_status == 'ONLINE' else 'DISCONNECTED',
    }


def dashboard(request):
    rigs = Rig.objects.select_related('assigned_racer').all()[:8]
    racers = Racer.objects.all()[:10]
    rig_form = RigUpdateForm()
    racer_form = RacerForm()
    return render(request, 'dashboard/index.html', {
        'races': Race.objects.prefetch_related('entries__racer', 'entries__rig').all()[:8],
        'rigs': rigs,
        'racers': racers,
        'rig_form': rig_form,
        'racer_form': racer_form,
        'manual_game_mode': True,
    })


def update_rig(request, pk):
    rig = get_object_or_404(Rig, pk=pk)
    if request.method == 'POST':
        form = RigUpdateForm(request.POST, instance=rig)
        if form.is_valid():
            form.save()
    return redirect('dashboard')


def create_racer(request):
    if request.method == 'POST':
        form = RacerForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('dashboard')


def communication(request):
    rigs = Rig.objects.select_related('assigned_racer').all()
    payload = {
        'devices': [_communication_row(rig, timezone.now()) for rig in rigs],
    }
    if request.GET.get('format') == 'json':
        return JsonResponse(payload)
    return render(request, 'dashboard/communication.html', {
        'devices': payload['devices'],
        'summary': {
            'total': len(payload['devices']),
            'online': sum(1 for item in payload['devices'] if item['network_status'] == 'ONLINE'),
            'offline': sum(1 for item in payload['devices'] if item['network_status'] == 'OFFLINE'),
            'telemetry_active': sum(1 for item in payload['devices'] if item['telemetry_status'] == 'ACTIVE'),
            'telemetry_disconnected': sum(1 for item in payload['devices'] if item['telemetry_status'] in {'DISCONNECTED', 'WARNING'}),
        },
        'system_health': {
            'server': {'label': 'Race Control Server', 'status': 'ONLINE', 'details': 'Application responding normally.'},
            'network': {'label': 'Network Discovery', 'status': 'ACTIVE', 'details': 'Database-backed rig inventory is available.'},
            'telemetry': {'label': 'Telemetry Service', 'status': 'RUNNING', 'details': 'Mock provider is active for demo devices.'},
            'websocket': {'label': 'WebSocket Service', 'status': 'POLLING MODE', 'details': 'Using server polling for live communication updates in the MVP.'},
            'database': {'label': 'Database', 'status': 'ONLINE', 'details': f'{Rig.objects.count()} rig records available.'},
        },
    })


def communication_data(request):
    now = timezone.now()
    devices = [_communication_row(rig, now) for rig in Rig.objects.select_related('assigned_racer').all()]
    summary = {
        'total': len(devices),
        'online': sum(1 for item in devices if item['network_status'] == 'ONLINE'),
        'offline': sum(1 for item in devices if item['network_status'] == 'OFFLINE'),
        'telemetry_active': sum(1 for item in devices if item['telemetry_status'] == 'ACTIVE'),
        'telemetry_disconnected': sum(1 for item in devices if item['telemetry_status'] in {'DISCONNECTED', 'WARNING'}),
    }
    return JsonResponse({'devices': devices, 'summary': summary})


def race_detail(request, pk):
    race = get_object_or_404(Race.objects.prefetch_related('entries__rig', 'entries__racer'), pk=pk)
    return render(request, 'dashboard/race.html', {'race': race})


def race_history(request):
    races = Race.objects.prefetch_related('entries__racer', 'entries__rig').all()
    search = request.GET.get('search', '').strip()
    simulator = request.GET.get('simulator', '').strip()
    track = request.GET.get('track', '').strip()
    racer = request.GET.get('racer', '').strip()
    status = request.GET.get('status', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()

    if search:
        races = races.filter(Q(name__icontains=search) | Q(track__icontains=search) | Q(entries__driver_name__icontains=search) | Q(entries__racer__name__icontains=search))
    if simulator:
        races = races.filter(simulator__icontains=simulator)
    if track:
        races = races.filter(track__icontains=track)
    if status:
        races = races.filter(status=status)
    if date_from:
        races = races.filter(created_at__date__gte=date_from)
    if date_to:
        races = races.filter(created_at__date__lte=date_to)
    if racer:
        races = races.filter(entries__racer__name__icontains=racer)
    races = races.distinct()

    history = []
    for race in races:
        winner = race.entries.order_by('position', 'grid_position').first()
        best_lap = race.entries.exclude(lap_time__isnull=True).order_by('lap_time').first()
        history.append({'race': race, 'winner': winner, 'best_lap': best_lap})

    return render(request, 'dashboard/race_history.html', {
        'races': history,
        'search': search,
        'simulator': simulator,
        'track': track,
        'racer': racer,
        'status': status,
        'date_from': date_from,
        'date_to': date_to,
        'race_status_choices': Race.STATUS_CHOICES,
        'simulators': sorted({race.simulator for race in Race.objects.exclude(simulator='').all()}),
        'racers': Racer.objects.all(),
    })


def reports(request):
    races = Race.objects.prefetch_related('entries__racer', 'entries__rig').all()
    race_report_rows = []
    for race in races:
        entries = list(race.entries.select_related('racer', 'rig').all())
        if not entries:
            continue
        winner = min(entries, key=lambda item: item.position)
        best_entry = min((item for item in entries if item.lap_time is not None), key=lambda item: item.lap_time, default=None)
        race_report_rows.append({
            'race': race,
            'winner': winner,
            'best_lap': best_entry,
            'entry_count': len(entries),
            'duration': (race.finished_at or timezone.now() if race.started_at else timezone.now())
        })

    driver_rows = []
    for racer in Racer.objects.prefetch_related('race_entries__race').all():
        entries = list(racer.race_entries.all())
        if not entries:
            continue
        wins = sum(1 for entry in entries if entry.position == 1)
        podiums = sum(1 for entry in entries if entry.position <= 3)
        best_lap = min((entry.lap_time for entry in entries if entry.lap_time is not None), default=None)
        average_position = sum(entry.position for entry in entries) / len(entries)
        driver_rows.append({
            'racer': racer,
            'races': len({entry.race_id for entry in entries}),
            'wins': wins,
            'podiums': podiums,
            'best_lap': best_lap,
            'average_position': round(average_position, 2) if average_position else None,
            'best_position': min((entry.position for entry in entries), default=None),
        })

    rig_rows = []
    for rig in Rig.objects.select_related('assigned_racer').all():
        entries = list(rig.race_entries.select_related('race').all())
        if not entries:
            rig_rows.append({
                'rig': rig,
                'total_sessions': 0,
                'total_race_time': 0,
                'most_used_game': 'No data available yet.',
                'last_used': None,
                'current_status': rig.status,
                'has_data': False,
            })
            continue
        total_race_time = sum(float(entry.total_time or 0) for entry in entries)
        most_used_game = rig.race_entries.values_list('race__simulator', flat=True)
        game_counts = {}
        for game in most_used_game:
            game_counts[game] = game_counts.get(game, 0) + 1
        most_used_game = max(game_counts.items(), key=lambda item: item[1])[0] if game_counts else 'No data available yet.'
        last_used = max((entry.race.finished_at or entry.race.started_at for entry in entries if entry.race.started_at), default=None)
        rig_rows.append({
            'rig': rig,
            'total_sessions': len(entries),
            'total_race_time': total_race_time,
            'most_used_game': most_used_game,
            'last_used': last_used,
            'current_status': rig.status,
            'has_data': True,
        })

    return render(request, 'dashboard/reports.html', {
        'race_report_rows': race_report_rows,
        'driver_rows': sorted(driver_rows, key=lambda item: item['average_position'] or 999)[:10],
        'rig_rows': rig_rows,
        'has_race_data': bool(race_report_rows),
    })


def browse_save(request):
    races = Race.objects.prefetch_related('entries__racer', 'entries__rig').all()
    racers = Racer.objects.all()
    rigs = Rig.objects.select_related('assigned_racer').all()
    return render(request, 'dashboard/browse_save.html', {
        'races': races,
        'racers': racers,
        'rigs': rigs,
        'export_targets': [
            ('races', '/browse-save/export/races/csv/'),
            ('races', '/browse-save/export/races/json/'),
            ('racers', '/browse-save/export/racers/csv/'),
            ('racers', '/browse-save/export/racers/json/'),
            ('rigs', '/browse-save/export/rigs/csv/'),
            ('rigs', '/browse-save/export/rigs/json/'),
        ],
    })


def export_model_csv(request, model_name):
    field_map = {'races': ['id', 'name', 'simulator', 'track', 'total_laps', 'status', 'created_at'],
                 'racers': ['id', 'name', 'short_name', 'created_at'],
                 'rigs': ['id', 'name', 'display_name', 'hostname', 'ip_address', 'status', 'assigned_racer_id', 'current_game', 'game_detection_mode', 'created_at']}
    rows = []
    if model_name == 'races':
        rows = list(Race.objects.values(*field_map[model_name]))
    elif model_name == 'racers':
        rows = list(Racer.objects.values(*field_map[model_name]))
    elif model_name == 'rigs':
        rows = list(Rig.objects.values(*field_map[model_name]))
    else:
        return HttpResponse('Unsupported model.', status=404)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model_name}.csv"'
    writer = csv.DictWriter(response, fieldnames=field_map[model_name])
    writer.writeheader()
    for row in rows:
        writer.writerow({key: row.get(key, '') for key in field_map[model_name]})
    return response


def export_model_json(request, model_name):
    if model_name == 'races':
        payload = list(Race.objects.values('id', 'name', 'simulator', 'track', 'total_laps', 'status', 'created_at'))
    elif model_name == 'racers':
        payload = list(Racer.objects.values('id', 'name', 'short_name', 'created_at'))
    elif model_name == 'rigs':
        payload = list(Rig.objects.values('id', 'name', 'display_name', 'hostname', 'ip_address', 'status', 'assigned_racer_id', 'current_game', 'game_detection_mode', 'created_at'))
    else:
        return HttpResponse('Unsupported model.', status=404)
    response = HttpResponse(json.dumps(payload, default=str), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{model_name}.json"'
    return response
