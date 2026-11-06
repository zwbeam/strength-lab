# Android-friendly development preview

## Publication status

**Preview files uploaded; owner must enable Pages once. Not yet publicly verified.**
The user authorized a separate web preview, not a production release or APK.
Do not claim that pushing development updates the existing installed PWA.

GitHub/network access now works. The existing public app is verified at
https://zwbeam.github.io/strength-lab/, with Pages configured to serve `main` at
`/` (legacy branch deployment). Its index/app/worker/manifest fingerprints and
main SHA `4cb58d8` were checked before and after the attempted publication and
remain unchanged. No existing Pages settings were changed.

To keep both main and the existing deployment untouched, publication uses the
separate public repository `zwbeam/strength-lab-preview` on its `preview` branch.
The owner created it and the complete isolated app was uploaded successfully.
The first deployment commit was `f482bac`, built from source `613c408`; subsequent
normal updates are recorded in Git. No source-main or original Pages change occurred.

The connector has contents/workflows write but no administration/Pages permission.
Enabling Pages through the API returned integration HTTP 403. The official
configure-pages action confirms first-time enablement requires a different token;
normal GITHUB_TOKEN cannot perform that owner step. No workflow/token workaround
was attempted. The required one-time owner action is:

1. Open https://github.com/zwbeam/strength-lab-preview/settings/pages.
2. Under Build and deployment, choose **Deploy from a branch**.
3. Select **preview** and **/(root)**, then **Save**.
4. Return and say **Pages enabled; verify the preview.**

Network access and repository creation are complete; do not ask to repeat them.
No credential sharing is needed. After Pages is enabled, ordinary preview-branch
content pushes can publish updates without changing repository settings.

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
To upload/update the isolated preview assets, run:

```sh
python3 scripts/publish-preview.py
```

The publisher fetches the latest source development ref, builds its exact committed
SHA, normally commits/pushes generated assets to the preview repository, and checks
original main/Pages settings remain unchanged. Pages must be enabled once by the
owner using the steps above; the publisher does not change Pages/default-branch
settings or request administrative permission. It
refuses unexpected/private repositories, unfamiliar branches/files or changed
preview hosting settings. It never force-pushes. It requires verification of the
actual resulting HTTPS URL before calling publication complete. No production
release or Android APK is made.

Expected preview address: `https://zwbeam.github.io/strength-lab-preview/`.
This is **not yet live/verified**; do not hand it to the user as a working app link.

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
first-time Pages enablement is blocked by the GitHub integration permission.

## Future preview updates

After first publication, `python3 scripts/publish-preview.py` fetches the latest
development branch, builds its exact committed SHA and commits normally to the
separate preview repository. Then run the actual-URL verifier with that source SHA.
No change to main or the existing site's settings is part of this process. A push
to the source development branch alone does not automatically publish the preview;
ask Codex to publish the latest preview after verified changes. No paid hosting or
automatic workflow is enabled.

Record the final verified URL and source/deployment commits here after publication.
Preview test data survives normal updates and never reads live history. Once live,
open the verified link in Chrome on Android; optionally choose menu → Add to home
screen (or Install app) and confirm the name includes DEV. Keep the normal Strength
Lab installation separate.
