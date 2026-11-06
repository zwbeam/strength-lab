# Android-friendly development preview

## Publication status

**Live and publicly verified:** https://zwbeam.github.io/strength-lab-preview/

Verified source: `7c6f2c0070840db3da4a1c813ae57e1bb8411e92`.
Deployment: `2b5e4a71c1b62ae8287c2edb1625a358af809f05` on the separate preview repo.
The interface shows **Development preview · 7c6f2c0**. Later source commits that
only update tests/docs/publishing tools do not change this deployed app version.

The owner enabled Pages on `zwbeam/strength-lab-preview`, using the `preview`
branch and `/(root)`. GitHub reports the build complete. The actual public HTTPS
workflow passed using Pixel 5 Chromium emulation: metadata/manifest identity,
all 79 assets, Android-sized layout without horizontal overflow, full workout
overview, timer pause/resume, set logging, saved progress, Settings, movement
library, offline reload and offline transcript reading. This is not physical
Android testing. No further setup/authorization is required.

The existing app at https://zwbeam.github.io/strength-lab/ still serves main/root.
Its main SHA `4cb58d8`, Pages configuration and index/app/worker/manifest hashes
were checked unchanged. Preview history/legacy history, writer lock, manifest
identity, worker scope and cache prefix are separate. Fresh preview test data
is intentional; no live history was transferred. No release or APK was created.

## UX review 1

The deployed build contains the repaired touchable timer (Manual default,
Automatic/Hybrid preferences), Exercises, focused Pathways and source-reviewed
instruction. All 31 movements are represented; 29 have exact corpus video
mappings. Carry/front squat remain unmapped; partial instruction is labeled.
New tabs use isolated preview data; existing preview data is preserved on update.

Please check timer touch controls in all modes, pause/resume after switching
apps, lesson readability, pathway navigation and video opening on Android.
Automated mobile testing is not a substitute for this review.

## Open on Android

1. Open https://zwbeam.github.io/strength-lab-preview/ in Chrome.
2. Explore Train, Progress, Learn and Settings. The DEV banner identifies the preview.
3. Optionally choose Chrome menu → Add to home screen (or Install app), and
   confirm the name includes **Strength Lab DEV**. Keep the existing app separate.

The network/repository/Pages owner setup is complete. Do not ask to repeat it.

## Isolated build

```sh
python3 scripts/build-preview.py --ref origin/development/reconciliation --output /tmp/strength-lab-preview
```

Use an empty output directory outside the checkout. The builder reads a committed
Git tree; uncommitted application edits cannot masquerade as the displayed SHA.
It copies only runtime assets from the app's service-worker inventory, not Git,
tests, logs, source audits, uploaded ZIPs or environment files. It fails closed if
storage/banner contracts change. It does not publish, update Pages, create an APK
or modify the original application. A directory of static preview assets is not
a production release package.

Build properties:

- Visible **Development preview** banner with the actual full source SHA in
  `preview-build.json`; short SHA is shown in the interface.
- Manifest name `Strength Lab Development Preview`, home-screen label
  `Strength Lab DEV`, relative start/scope/id. At a dedicated preview subpath,
  that identity is distinct from the live root app.
- Separate `sl-dev-preview-*` V33 history/draft/journal and writer-lock names,
  plus a separate legacy data key. No automatic live-history migration.
- Separate `sl-dev-preview-cache-*` caches. They deliberately do not match the
  live worker's `strength-lab-*` deletion prefix. The preview worker caches and
  reads only its own scope/cache, never a live-site navigation fallback.
- Complete existing app/engine/source reader and relative assets. No new training
  features or source app/engine changes were introduced for this preview.

Locally verified path: `/strength-lab/dev-preview/`. This is a test-server path,
**not evidence that an equivalent public address is live**. Use one stable preview
channel/path; multiple preview channels need their own namespace before publishing.

## Publication route

The original repo's Pages source is main/root. A subpath there would require
changing main or the existing deployment. The separate preview repository keeps
the live app and its update mechanism unchanged and uses only free GitHub hosting.
To publish future verified development changes, run:

```sh
python3 scripts/publish-preview.py
```

The publisher fetches the latest source development ref, builds its exact committed
SHA, normally commits/pushes generated assets to the preview repository, and checks
original main/Pages settings remain unchanged. Pages is already enabled by the owner. The publisher does not change
Pages/default-branch settings or request administrative permission. It
refuses unexpected/private repositories, unfamiliar branches/files or changed
preview hosting settings. It never force-pushes. It requires verification of the
actual resulting HTTPS URL before calling publication complete. No production
release or Android APK is made.

Verified preview address: `https://zwbeam.github.io/strength-lab-preview/`.

## Browser verification

```sh
python3 tests/preview-isolation.py
python3 tests/preview-url.py --url https://ACTUAL-DEPLOYED-PREVIEW/ --commit SOURCE_SHA
```

The first suite builds beside an untouched copy of main at a repository subpath.
It uses Pixel 5 Chromium emulation, checks all 79 assets, manifest/version, separate
keys/lock/scopes/caches, full overview, duration, timer pause/logging, saved progress,
settings/library, offline source reading, preview upgrade and live worker upgrade.
It verifies original live files and storage remain unchanged. This is not physical
Android testing and does not prove a deployed URL exists.

The second suite is for the **actual HTTPS URL** only. It verifies metadata/expected
SHA before exercising fresh preview data, assets, Android-sized layout, timers,
logging, Progress/Settings/library and offline reload. Do not report publication
success until this succeeds against the real address. It passed against the public site on 2026-11-06. In managed cloud environments
it uses the configured HTTPS proxy and CA trust with TLS verification enabled.

## Future preview updates

After first publication, `python3 scripts/publish-preview.py` fetches the latest
development branch, builds its exact committed SHA and commits normally to the
separate preview repository. Then run the actual-URL verifier with that source SHA.
No change to main or the existing site's settings is part of this process. A push
to the source development branch alone does not automatically publish the preview;
ask Codex to publish the latest preview after verified changes. No paid hosting or
automatic workflow is enabled.

Record the new verified source/deployment commits here after each update.
Preview test data survives normal updates and never reads live history. Once live,
open the verified link in Chrome on Android; optionally choose menu → Add to home
screen (or Install app) and confirm the name includes DEV. Keep the normal Strength
Lab installation separate.

Latest confirmed content upload: source `7c6f2c0070840db3da4a1c813ae57e1bb8411e92`,
deployment `2b5e4a71c1b62ae8287c2edb1625a358af809f05`. Repeat normal publication
was verified without administrative writes; source main/Pages stayed unchanged.
The owner enabled Pages and this exact deployment passed public HTTPS verification.
