Create/update the project's README.md as a professional GitHub repository README.

IMPORTANT:
Document the CURRENT implementation honestly.
Do not claim real F1 25 telemetry or Raspberry Pi deployment is complete if it is not.

Project name:

# 🏁 Sim Racing Control Center

Short description:

A Django-based LAN race management and live timing platform designed to manage multiple sim-racing rigs, drivers, races, telemetry connections, results, reports, and future real-time game telemetry.

==================================================
PROJECT OVERVIEW
==================================================

Sim Racing Control Center is designed for environments where multiple racing simulator PCs are connected through an Ethernet network/switch.

The long-term architecture is:

Multiple Racing PCs
        ↓
Ethernet Switch
        ↓
Race Control Server
        ↓
Telemetry Collector
        ↓
Race Engine
        ↓
Django / WebSocket
        ↓
Live Race Dashboard

The Race Control Server will initially be developed and tested on Windows.

Later the same application should be deployable to a Raspberry Pi.

The racing PCs should not need to run the Django application.

==================================================
CURRENT STATUS
==================================================

Current implementation is an MVP/foundation.

Completed/current functionality:

- Django-based web application
- Main Race Control UI
- Live Race dashboard foundation
- Rig/device management
- Local network device discovery
- Physical rig identity separated from display name
- Hostname/IP/device information
- Rig renaming
- Racer/driver assignment
- Racer management foundation
- Current game/simulator field
- Manual/automatic game detection architecture
- Scheduled races
- Race history
- Recorded race results
- Reports foundation
- Browse & Save section
- CSV export
- JSON export
- Mock telemetry
- Telemetry provider abstraction
- Race engine foundation
- Communication monitoring architecture
- Django Admin customization
- SQLite development database
- Automated tests

IMPORTANT:

Real game telemetry integration is NOT considered complete yet.

F1 25 UDP telemetry is the next major technical integration.

Assetto Corsa and other simulators will be added later through separate telemetry providers/adapters.

==================================================
APPLICATION NAVIGATION
==================================================

Current/target main navigation:

🏁 Live Race
📊 Race History
📅 Scheduled Races
🖥️ Rigs
👤 Racers
📑 Reports
💾 Browse & Save
📡 Communication
⚙️ Settings

Django Admin is an internal administrative interface and is NOT intended to be the main operator UI.

==================================================
FEATURES
==================================================

## Live Race

The Live Race dashboard is designed to display:

- Current race
- Simulator/game
- Track
- Lap
- Race status
- Driver positions
- Lap times
- Best lap
- Last lap
- Gap
- Speed
- Gear
- RPM
- Telemetry state

The current MVP can use simulated/mock telemetry.

The final implementation will consume real game telemetry.

## Rigs

Rigs represent physical racing machines.

A rig contains technical information such as:

- Device identity
- Hostname
- IP address
- MAC address when available
- Network status
- Telemetry status
- Last seen

Human-facing information is separate:

- Rig display name
- Assigned racer

A rig and racer are NOT the same entity.

A racer can use different rigs over time.

A rig can be used by different racers over time.

## Racers

Racers/drivers are persistent entities.

Race entries associate a racer with a rig for a specific race.

Historical race results must preserve the racer who actually participated in that race.

## Scheduled Races

Operators can create upcoming races with:

- Race name
- Simulator
- Track
- Date
- Time
- Number of laps
- Selected rigs/racers

## Race History

Completed races are stored and can be browsed.

Future filtering includes:

- Date
- Simulator
- Track
- Racer
- Status

## Reports

The reporting system is intended to provide:

- Race reports
- Driver performance
- Best lap times
- Race statistics
- Rig utilization
- Historical performance

Reports must be based on stored race data.

## Browse & Save

Race information can be browsed and exported.

Current export formats:

- CSV
- JSON

PDF reporting can be added later.

## Communication

The communication system is intended to monitor:

- Available devices
- Network status
- Telemetry status
- Last seen
- Last telemetry packet
- Current game
- Client/heartbeat status

Network connectivity and telemetry connectivity are separate.

For example:

Network: ONLINE
Telemetry: DISCONNECTED

is a valid state.

==================================================
TELEMETRY ARCHITECTURE
==================================================

Telemetry is intentionally separated from the rest of the application.

Current conceptual architecture:

TelemetryProvider
    |
    +-- MockTelemetryProvider
    |
    +-- F125TelemetryProvider
    |
    +-- AssettoCorsaTelemetryProvider
    |
    +-- Future providers

Today's development uses:

MockTelemetryProvider

Future real flow:

F1 25
    ↓
UDP telemetry
    ↓
F125TelemetryProvider
    ↓
Telemetry Manager
    ↓
Race Engine
    ↓
Django/WebSocket
    ↓
Live Dashboard

The dashboard should not directly depend on raw F1 25 packet structures.

==================================================
NETWORK ARCHITECTURE
==================================================

Development:

Windows PC
    |
    +-- Django
    +-- Telemetry Service
    +-- Database
    +-- Web Dashboard

Production concept:

Racing PC 1 ──┐
Racing PC 2 ──┤
Racing PC 3 ──┤
Racing PC 4 ──┤
              │
         Ethernet Switch
              │
              ▼
        Race Control Server
              │
              ▼
          Dashboard

The Race Control Server can eventually run on Raspberry Pi.

==================================================
MACHINE-SIDE ARCHITECTURE
==================================================

The racing PCs are game machines.

They do not need Django.

Future machine-side architecture:

Racing PC
    |
    +-- Racing Game
    |
    +-- Game telemetry output
    |
    +-- Optional lightweight Race Control Client Agent
    |
    └-- Heartbeat/status reporting

The optional client agent may eventually report:

- Device UUID
- Hostname
- IP
- Running supported game
- Game version
- Telemetry capability
- Telemetry status
- Heartbeat

==================================================
CURRENT PROJECT STRUCTURE
==================================================

Document the actual current structure based on the repository.

Expected architectural organization:

project-root/
│
├── manage.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── ...
│
├── devices/
│   ├── models.py
│   ├── admin.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── services/
│       └── discovery.py
│
├── races/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── services/
│       └── race_engine.py
│
├── telemetry/
│   ├── providers/
│   │   ├── base.py
│   │   ├── mock.py
│   │   ├── f125.py
│   │   └── assetto_corsa.py
│   └── services/
│       └── telemetry_manager.py
│
├── dashboard/
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── templates/
│   │   └── dashboard/
│   └── static/
│
├── templates/
│
├── static/
│
├── tests/
│
├── requirements.txt
│
├── README.md
│
└── .gitignore

IMPORTANT:

Before writing this section, inspect the repository and replace the example structure with the ACTUAL structure.

Do not document files that do not exist.

==================================================
DEVELOPMENT ENVIRONMENT
==================================================

Current development environment:

Windows

Python environment:

Rba conda environment

Run Django using:

conda run -n Rba python manage.py runserver

Run tests using:

conda run -n Rba python manage.py test

Development database:

SQLite

==================================================
SETUP
==================================================

Document the actual setup process.

Typical:

1. Clone repository
2. Create/activate Rba environment
3. Install dependencies
4. Run migrations
5. Create superuser if Django Admin is required
6. Start development server

Do not expose real credentials in README.

==================================================
ROADMAP / REMAINING WORK
==================================================

Create a clearly ordered roadmap.

PHASE 1 — MVP FOUNDATION

Current:

[x] Django project
[x] Main application UI
[x] Rig management
[x] Device discovery
[x] Rig renaming
[x] Racer assignment
[x] Current game field
[x] Race scheduling foundation
[x] Race history
[x] Reports foundation
[x] Browse & Save
[x] CSV/JSON export
[x] Mock telemetry
[x] Telemetry abstraction
[x] Race engine foundation
[x] Communication monitoring foundation

PHASE 2 — REAL TELEMETRY

Next major milestone:

[ ] Research/verify F1 25 telemetry protocol
[ ] Implement F1 25 UDP packet receiver
[ ] Implement F1 25 packet parser
[ ] Map F1 25 telemetry into common telemetry model
[ ] Connect real telemetry to race engine
[ ] Test one physical racing PC
[ ] Test multiple racing PCs
[ ] Telemetry timeout handling
[ ] Packet-loss handling
[ ] Connection diagnostics

PHASE 3 — CLIENT / MACHINE MANAGEMENT

[ ] Lightweight Windows client agent
[ ] Stable machine UUID
[ ] Client registration
[ ] Client heartbeat
[ ] Current game detection
[ ] Game version detection
[ ] Telemetry capability reporting
[ ] Remote configuration/status
[ ] Client auto-start/service

PHASE 4 — MULTI-GAME SUPPORT

[ ] F1 25 adapter
[ ] Assetto Corsa adapter
[ ] Assetto Corsa Competizione adapter
[ ] Additional simulator adapters
[ ] Common telemetry data model validation
[ ] Game-specific capability handling

PHASE 5 — RACE ENGINE

[ ] Accurate live position calculation
[ ] Lap detection
[ ] Sector timing
[ ] Gap calculation
[ ] Pit detection
[ ] DNF/DSQ handling
[ ] Safety car handling where supported
[ ] Race restart handling
[ ] Session state management

PHASE 6 — REPORTING

[ ] Detailed race reports
[ ] Driver statistics
[ ] Lap-by-lap analysis
[ ] Sector analysis
[ ] Rig utilization
[ ] Historical comparisons
[ ] PDF reports
[ ] Advanced exports

PHASE 7 — PRODUCTION HARDENING

[ ] PostgreSQL
[ ] Redis if actually required
[ ] Production WebSocket configuration
[ ] Authentication
[ ] User roles/permissions
[ ] Logging
[ ] Error monitoring
[ ] Backup/restore
[ ] Configuration management
[ ] Security review
[ ] Network security
[ ] Service management

IMPORTANT:

Do NOT introduce RabbitMQ/Kafka/other brokers unless the actual architecture requires them.

Redis should only be introduced after evaluating the multi-rig workload and WebSocket/channel-layer requirements.

PHASE 8 — RASPBERRY PI

[ ] Raspberry Pi OS setup
[ ] Python environment
[ ] Django deployment
[ ] Production web server
[ ] Process/service management
[ ] Database configuration
[ ] Network configuration
[ ] Automatic startup
[ ] Monitoring
[ ] Backup
[ ] Remote maintenance

PHASE 9 — PRODUCTION DEPLOYMENT

[ ] Multi-rig testing
[ ] Long-duration race testing
[ ] Network failure testing
[ ] PC restart recovery
[ ] Server restart recovery
[ ] Telemetry packet-loss testing
[ ] Race data integrity testing
[ ] Performance testing
[ ] Final operator documentation

==================================================
CURRENT LIMITATIONS
==================================================

Clearly document:

- Real F1 25 telemetry is not yet integrated.
- Mock telemetry is used for development/demo.
- Automatic game detection may not yet be implemented.
- Raspberry Pi deployment is not complete.
- Advanced reporting is still under development.
- Production database/deployment configuration is not final.

Do not describe these as bugs unless they actually are bugs.

==================================================
DESIGN PRINCIPLES
==================================================

Document these principles:

1. Rig identity is separate from racer identity.
2. Technical machine identity is separate from human display names.
3. Current game is runtime information.
4. Historical race entries preserve the racer/rig relationship at race time.
5. Network connectivity and telemetry connectivity are separate.
6. Telemetry providers are modular.
7. The dashboard must not depend directly on game-specific packet structures.
8. The Race Control server is separate from racing PCs.
9. Development happens on Windows before Raspberry Pi deployment.
10. Add infrastructure only when justified by actual requirements.

==================================================
README QUALITY
==================================================

Make the README professional and easy for another developer to understand.

Include:

- project description
- screenshots section placeholder
- architecture
- current features
- project structure
- setup
- development commands
- telemetry architecture
- network architecture
- machine-side architecture
- roadmap
- limitations
- contribution/development notes

Do not claim unfinished features as completed.

After updating README, show me the actual final project tree and summarize what is currently implemented versus what remains.
