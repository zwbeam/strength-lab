"""Check the actual library exposes the same curriculum prerequisites and sources."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
thread=Thread(target=server.serve_forever,daemon=True);thread.start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':390,'height':844});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/');page.locator('[data-tab="learn"]').click()
  page.locator('[data-learn-move="getup"]').click();getup=page.locator('#movement-instruction')
  assert 'Controlled hip pass' in getup.inner_text() and '3 to 10 total minutes' in getup.inner_text()
  getup.locator('.source-coverage summary').click();getup.locator('[data-open-source="423"]').first.click()
  page.locator('#transcript-dialog').wait_for(state='visible');assert 'three minutes four minutes' in page.locator('#transcript-body').inner_text()
  page.get_by_role('button',name='Close',exact=True).click();page.locator('#learn-back').click()
  page.locator('[data-learn-move="clubInside"]').click();inside=page.locator('#movement-instruction');assert 'three weights' in inside.inner_text()
  inside.locator('.source-coverage summary').click();inside.locator('[data-open-source="543"]').first.click()
  page.locator('#transcript-dialog').wait_for(state='visible');assert 'at least three weights' in page.locator('#transcript-body').inner_text()
  page.get_by_role('button',name='Close',exact=True).click()
  page.locator('[data-tab="settings"]').click()
  assert page.locator('[data-program-step="clubInside"]').count()==1
  assert page.locator('[data-club-start="clubInside"]').count()==0
  assert page.locator('[data-program-seconds="clubInside"]').count()==0
  assert page.locator('[data-program-seconds="cast"]').count()==1
  assert not errors,errors
  print('PASS: shared get-up/club prerequisites and progression descriptions open the correct verified teaching transcripts in the actual library')
  browser.close()
finally:
 server.shutdown();server.server_close();thread.join()
