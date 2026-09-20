# 🏁 Sim Racing Control Center — Docker Setup

This Docker setup is for the current Django MVP.

## What is included

- Django
- Django REST Framework
- SQLite
- Current dashboard/frontend
- Current mock telemetry
- Current project apps

No separate installation is required for:

- Anaconda
- Miniconda
- Python
- Node.js
- npm
- PostgreSQL
- Redis

The Python dependencies are installed inside the Docker image.

## Requirements

Install Docker Desktop:

- Windows: Docker Desktop
- macOS: Docker Desktop

Linux Docker can also be used.

## 1. Clone the repository

```bash
git clone https://github.com/lohithmahamkali29/Gaming_Dashboard.git
cd Gaming_Dashboard
```

Copy these Docker files into the project root:

```text
Dockerfile
compose.yaml
docker-entrypoint.sh
.dockerignore
requirements.txt
```

## 2. Build and start

```bash
docker compose up --build
```

The container automatically runs:

```text
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## 3. Test on the Race Control PC

Open:

```text
http://localhost:8000/
```

## 4. Test from another PC on the LAN

Find the Race Control PC's IPv4 address.

Windows:

```cmd
ipconfig
```

Then from the Racing PC open:

```text
http://SERVER_IP:8000/
```

Example:

```text
http://192.168.1.20:8000/
```

## 5. Check the container

```bash
docker ps
```

Expected container:

```text
sim-racing-control-center
```

View logs:

```bash
docker compose logs -f
```

## 6. Stop

```bash
docker compose down
```

## 7. Start again without rebuilding

```bash
docker compose up -d
```

## Important — SQLite

The current repository uses SQLite for development.

This Docker setup is intended for the current MVP/physical communication test.

The database is created inside the container when migrations run. For a production deployment, SQLite persistence should be configured explicitly, or the project can later move to PostgreSQL.

## Important — F1 25 UDP telemetry

The current repository documentation says real F1 25 telemetry is not yet considered complete.

Therefore this Compose file intentionally does NOT expose a UDP telemetry port yet.

When the F1 25 UDP listener is actually implemented and its port is confirmed, the Compose configuration can be extended, for example:

```yaml
ports:
  - "8000:8000"
  - "20777:20777/udp"
```

Do not add this until the project's actual F1 25 telemetry listener is ready.

## Test architecture

```text
                 Ethernet / LAN
Racing PC  ───────────────────────────┐
                                      │
                                      ▼
                              Race Control PC
                                      │
                                      ▼
                               Docker Container
                                      │
                              Django :8000
                                      │
                                      ▼
                                  Browser
```

Future telemetry:

```text
F1 25
  │
  │ UDP telemetry
  ▼
Race Control telemetry listener
  │
  ▼
Telemetry Manager
  │
  ▼
Race Engine
  │
  ▼
Django / Dashboard
```
