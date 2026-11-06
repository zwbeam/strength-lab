# Android-friendly development preview

## Publication status

**Prepared and tested locally; not deployed or publicly verified yet.**
The user authorized a separate web preview, not a production release or APK.
Do not claim that pushing development updates the existing installed PWA.

Verified development/source checkpoint: `d5603e8` at the start of this task.
Remote main remains `4cb58d8`. Neither branch contained a deployment workflow;
main contains the older V32 static app. The repository had no CNAME/deployment
instructions. Git access works, but the current execution network blocked
`api.github.com` and `zwbeam.github.io` with proxy 403 responses. Therefore Pages
settings, actual hosting mode, account permissions and public URL remain unverified.
No Pages settings or live deployment have been changed.

A configuration draft allowing those two exact domains was saved successfully.
It requires the user to review/save and **Publish** the environment; saving the
draft does not activate access. Once that is applied, inspect `gh api
repos/zwbeam/strength-lab/pages`, repository metadata and any current workflows
before choosing the publication route. The private repo may have Pages/account
restrictions; do not assume them or request credentials until checked.

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

## Hosting decision still required

Prefer a dedicated subpath only if the actual existing Pages deployment can add
it without replacing the live content or changing main. Preserve the current live
root and its update mechanism. A main-root branch deployment cannot be assumed to
publish development-branch files. Do not switch Pages source or replace a Pages
artifact based only on this proposed path. Inspect the actual settings first.
If additive publication is unavailable under the existing configuration, prepare
the concrete alternative and any required user authorization before changing it.
No paid hosting or new external service is required by this build.

## Browser verification

```sh
python3 tests/preview-isolation.py
python3 tests/preview-url.py --url https://ACTUAL-DEPLOYED-PREVIEW/ --commit SOURCE_SHA
```

The first suite builds beside an untouched copy of main at a repository subpath.
It uses Pixel 5 Chromium emulation, checks all 76 assets, manifest/version, separate
keys/lock/scopes/caches, full overview, duration, timer pause/logging, saved progress,
settings/library, offline source reading, preview upgrade and live worker upgrade.
It verifies original live files and storage remain unchanged. This is not physical
Android testing and does not prove a deployed URL exists.

The second suite is for the **actual HTTPS URL** only. It verifies metadata/expected
SHA before exercising fresh preview data, assets, Android-sized layout, timers,
logging, Progress/Settings/library and offline reload. Do not report publication
success until this succeeds against the real address. It has not run yet because
network/hosting access is blocked.

## Future preview updates

After the hosting route is confirmed and documented here:

1. Fetch/test the latest development branch and build its exact committed SHA.
2. Publish only the isolated preview output to the confirmed preview location,
   preserving live files/settings/update mechanism and main.
3. Run `tests/preview-url.py` against that HTTPS URL with the expected source SHA.
4. Record the verified URL/SHA in this document and the development log. Existing
   preview test data persists through ordinary preview updates; no live data is read.

No automatic publishing workflow is enabled yet. A Git push alone currently makes
no promise about the version shown in any installed PWA. Once live, open the verified
HTTPS link in Chrome on Android; optionally choose Chrome's menu → Add to home screen
(or Install app) and confirm the name includes DEV. Keep the normal Strength Lab
installation separate.
