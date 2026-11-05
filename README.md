# Strength Lab development workbench

Static, local-first kettlebell and club training app. Serve this directory with
Python 3 (`python3 -m http.server 8000`) or another static HTTP server. No build,
package installation, account or backend is required.

The development interface combines per-set logging, persistent drafts and timers,
source-scoped movement cycles, configurable heavy/light waves, explicit pain review, reduced recovery work,
adjustable duration and an offline full-text transcript reader. Training parameters
are provisional app choices, not a completed synthesis of 720 lessons.

V31/V32 data stays under its original key. Open **Settings → Open previous training
log and backups** to access it. New workouts use the handoff's separate V33 data
key. Export backups regularly; clearing browser storage can delete local data.

Choose optional source blocks and own defaults in Settings → Training programming.
See [TRAINING-RULES.md](TRAINING-RULES.md) for the source/support boundaries.

See [DEVELOPMENT-STATUS.md](DEVELOPMENT-STATUS.md) for commands and remaining work,
and [RECONCILIATION-AUDIT.md](RECONCILIATION-AUDIT.md) for input provenance,
implementation decisions and validation scope. No release package has been created.
