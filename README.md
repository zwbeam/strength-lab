# Strength Lab

A free, offline-first, phone-friendly kettlebell and heavy-club workout logger.

## Included

- Four-week, 20-session training program, five weekdays per week
- Editable weight, set/time, and actual-rep entries per exercise
- Completed workout history, dates, RPE and notes
- Local-only persistent storage, with JSON backup/restore and CSV export for Google Sheets
- Installable Android PWA, with offline app shell once cached
- No accounts, analytics, external scripts, or recurring fees

## Host with GitHub Pages

1. Create a **public** GitHub repository called `strength-lab` (or any name).
2. Upload **all the files in this folder to the repository root**, including the PNG icons.
3. In repository **Settings → Pages**, select **Deploy from a branch**, `main`, `/ (root)`, and **Save**.
4. Open the URL GitHub Pages shows (typically `https://USERNAME.github.io/strength-lab/`) in **Chrome on Android**.
5. In Chrome's menu choose **Install app** or **Add to Home screen**.
6. Open Strength Lab, log one test workout, and export a JSON backup to verify storage.

**Important:** The app code is public if hosted in a public repo. Your private workout entries are not uploaded to GitHub; they remain in your browser storage. A lost phone, cleared site storage, or reinstall can delete those entries. Save JSON backups regularly.

## Update the app

Replace files in the GitHub repository. The offline service worker cache updates after redeployment; you may need to reopen or refresh the installed app twice. Existing browser workout data is held separately from the code cache. To change the internal storage schema in the future, add data migrations rather than silently overwriting user data.

## Local test

A service worker requires HTTP(S), not opening `index.html` using `file://`. In this folder, run `python -m http.server 8000` and open `http://localhost:8000` to test on desktop. Hosting with GitHub Pages enables Android installation.

Training suggestions are a baseline and should be tailored to technique, capacity, and symptoms.
