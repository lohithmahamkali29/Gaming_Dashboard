# Race Control

A small Django MVP for sim-racing rig discovery, race setup, and live timing.

## Run on Windows

Use the existing conda environment:

```powershell
conda run -n Rba python manage.py migrate
conda run -n Rba python manage.py seed_demo
conda run -n Rba python manage.py runserver
```

Open `http://127.0.0.1:8000/`. The dashboard uses polling for live updates because Django Channels is not required by this MVP. The telemetry provider boundary is ready for a UDP or simulator-specific implementation later.

## API

- `GET /api/devices/health/`
- `GET|POST /api/devices/rigs/`
- `GET|POST /api/devices/items/`
- `GET|POST /api/races/`
- `POST /api/races/<id>/start/`
- `GET /api/races/<id>/telemetry/`
