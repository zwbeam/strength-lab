# Development status

Updated 2026-11-05. Branch: `development/reconciliation`.
Original main: `4cb58d8a4d30796246a83db752b8e420c8bc05c2`.
Existing development commits `ccbb31f` and `bbf8085` preserved.

## Completed

- Both ZIPs downloaded, integrity-tested and inspected outside the checkout.
- Full mechanical reconciliation documented in RECONCILIATION-AUDIT.md.
- All 720 transcripts / 955,522 words match the 24 research shards and index.
- Handoff workout UI, pure movement engine and offline research reader integrated.
- Previous V31/V32 interface retained at `legacy/index.html`, linked in Settings.
  Existing local storage and export tools remain available; no automatic data conversion.
- Pain-review/re-entry, pause/resume, movement-specific absence detection,
  bilateral confirmation, rebuild recovery and missing-equipment handling implemented.
- Per-movement volume defaults stop at explicit milestones; unsupported generic
  automatic density progression removed. Policy provenance is explicit.
- Duration-aware, movement-specific preparation and cooldown; full-text search fixed.
- Strict backup validation and workout persistence failure handling added.
- Local history preserved. No main merge, push, deployment or release package.

## Verification

Passed: legacy smoke, engine assertions, 3 completion tests, 13 recovery tests,
3 backup tests, syntax/whitespace checks, six Chromium DOM interaction suites.
Real HTTP browser suite covers root and repository subpath, first-visit offline
startup, transcript search/reader, persistent workout/draft/rest state, bilateral
logging, pain review and old storage. See audit for scope and known limits.

## Reproduce

From `/workspace/strength-lab`:

```sh
node v31-smoke-test.cjs
node engine.test.cjs
node completion.test.cjs
node recovery.test.cjs
node backup.test.cjs
node --check app.js
node --check engine.js
node --check sw.js
python3 tests/browser-smoke.py
```

Browser tests require Python Playwright and `/usr/bin/chromium`, present here.
Local socket/browser operations may require the supported execution approval flow.
Research verification takes the extracted original transcript directory:
`python3 scripts/audit-transcripts.py /path/to/Transcripts`.

Development server: `python3 -m http.server 8000 --bind 127.0.0.1 --directory /workspace/strength-lab`.
No dependency installation or build step is required for the application.

## Next work

- Extract and validate movement-specific club/grind cycles and prerequisites.
- Add source-specific user-selected progression instead of treating app defaults
  as universal source prescriptions; investigate source #259 stall alternatives.
- Model overlapping movement demands and fatigue when composing program blocks.
- Expand research interpretation beyond mechanical fidelity and selected close readings.
- Verify installed Android/PWA behavior and service-worker upgrades across old sessions.
- Verify published environment restoration in a genuinely fresh cloud task. Current
  tools expose only the same onboarding instance; fresh browsers do not prove restoration.

No user setup action is currently required. Full training intelligence remains
in development; this branch is not a release.
