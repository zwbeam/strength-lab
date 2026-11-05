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
  getup=page.locator('details').filter(has=page.get_by_text('Turkish get-up',exact=True));getup.locator('summary').click()
  assert 'Controlled hip pass' in getup.inner_text()
  assert '3 to 10 total minutes' in getup.inner_text()
  getup.locator('[data-open-source="423"]').first.click()
  page.locator('#transcript-dialog').wait_for(state='visible')
  assert 'three minutes four minutes' in page.locator('#transcript-body').inner_text()
  page.get_by_role('button',name='Close',exact=True).click()
  inside=page.locator('details').filter(has=page.get_by_text('Single-arm club inside circle',exact=True));inside.locator('summary').click()
  assert 'three weights' in inside.inner_text()
  inside.locator('[data-open-source="543"]').first.click()
  page.locator('#transcript-dialog').wait_for(state='visible')
  assert 'at least three weights' in page.locator('#transcript-body').inner_text()
  page.get_by_role('button',name='Close',exact=True).click()
  assert not errors,errors
  print('PASS: shared get-up/club prerequisites and progression descriptions open the correct verified teaching transcripts in the actual library')
  browser.close()
finally:
 server.shutdown();server.server_close();thread.join()
