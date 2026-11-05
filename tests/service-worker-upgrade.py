"""Upgrade from committed reconciliation baseline without losing an active draft.
This is browser/PWA-cache coverage, not physical Android installation coverage.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
import io
import shutil
import subprocess
import tarfile
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
with TemporaryDirectory(prefix='strength-upgrade-') as tmp:
    target=Path(tmp)
    archive=subprocess.check_output(['git','archive','374967f'],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:tar.extractall(target,filter='data')
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(target)))
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            context=browser.new_context(**p.devices['Pixel 5'])
            page=context.new_page();errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
            page.goto(f'http://127.0.0.1:{server.server_port}/')
            page.evaluate('navigator.serviceWorker.ready.then(()=>true)')
            page.wait_for_function('navigator.serviceWorker.controller !== null')
            page.on('dialog',lambda dialog:dialog.accept())
            page.locator('[data-tab="settings"]').click()
            page.locator('[data-weight="squat"]').fill('12');page.locator('#save-weights').click()
            page.locator('[data-tab="today"]').click();page.locator('#start').click()
            page.get_by_role('button',name='Warmup complete · start work').click()
            page.locator('[data-check="0:0"]').click()
            legacy='{"version":1,"sessions":[],"drafts":{}}'
            page.evaluate('(value)=>localStorage.setItem("strengthlab-data-v31",value)',legacy)
            before=page.evaluate('Object.fromEntries(["strengthlab-data-v31","strengthlab-data-v33","strengthlab-draft-v33"].map(key=>[key,localStorage.getItem(key)]))')
            for name in ['app.js','engine.js','sw.js']:shutil.copy2(ROOT/name,target/name)
            page.evaluate('navigator.serviceWorker.getRegistration().then(registration=>registration.update()).then(()=>true)')
            page.wait_for_function('caches.keys().then(keys=>keys.includes("strength-lab-programming-20261105-2"))')
            page.reload()
            after=page.evaluate('Object.fromEntries(["strengthlab-data-v31","strengthlab-data-v33","strengthlab-draft-v33"].map(key=>[key,localStorage.getItem(key)]))')
            assert before==after,'Upgrade changed saved data or active draft'
            assert page.locator('[data-check="0:0"]').inner_text()=='✓'
            context.set_offline(True);page.reload()
            assert page.locator('[data-check="0:0"]').inner_text()=='✓'
            page.get_by_role('button',name='Finish main work · cooldown').click();page.locator('#save-workout').click()
            assert page.evaluate('state.sessions.length')==1
            assert page.evaluate('state.sessions[0].items[0].actualSets')==1
            page.locator('[data-tab="settings"]').click();assert page.locator('#save-programming').count()==1
            assert page.evaluate('localStorage.getItem("strengthlab-data-v31")')==legacy
            assert not errors,errors
            print('PASS: baseline-to-current worker upgrade, byte-identical saved keys/draft, mobile-emulated offline reload and successful continuation of the old workout')
            browser.close()
    finally:
        server.shutdown();server.server_close();thread.join()
