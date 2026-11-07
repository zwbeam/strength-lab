"""Review 1 Learn: actual phone-sized touch flows, statuses, maps, video targets, offline."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
records={r['id']:r for f in ROOT.glob('sources-*.json') for r in json.loads(f.read_text())}
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
thread=Thread(target=server.serve_forever,daemon=True);thread.start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);context=browser.new_context(**p.devices['Pixel 5'])
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
  base=f'http://127.0.0.1:{server.server_port}/';page.goto(base);page.get_by_role('button',name='Learn',exact=True).tap()
  assert page.locator('#learn-results [data-learn-move]').count()==31
  assert page.locator('[data-learn="atlas"]').count()==0 and page.locator('#source-search').count()==0
  page.locator('#learn-equipment').select_option('bodyweight');page.locator('#learn-family').select_option('ground');assert page.locator('#learn-results [data-learn-move]').count()==3
  page.locator('#learn-search').fill('single');assert page.locator('#learn-results [data-learn-move]').count()==1
  page.locator('[data-learn-move="hipDropSingleHand"]').tap();assert page.locator('#movement-instruction > .status-blocked').count()==1
  assert page.get_by_role('heading',name='Step by step',exact=True).count()==1
  video=page.locator('#movement-instruction .video-link').first;assert video.get_attribute('href')==records[98]['url'] and video.get_attribute('target')=='_blank'
  # Verify clean new-tab opening without claiming external video playback was tested.
  context.route(re.compile(r'https://www\.youtube\.com/.*'),lambda route:route.fulfill(body='<html><title>Verified source link target fixture</title></html>',content_type='text/html'))
  with page.expect_popup() as popup:video.tap()
  popup.value.wait_for_load_state();assert popup.value.url==records[98]['url'];popup.value.close()
  page.locator('[data-learn="pathways"]').first.tap();assert page.locator('#focused-pathway').count()==1
  page.locator('#focused-pathway [data-learn-move="hipDropTwoHand"]').tap();assert 'Two-hand hip-drop practice' in page.locator('.pathway-center').inner_text()
  assert page.locator('#focused-pathway [data-learn-move="hipDropSingleHand"]').count()==1
  page.locator('#pathway-movement').select_option('clean');assert 'Combinations' in page.locator('#movement-instruction').inner_text()
  assert page.locator('#movement-instruction [data-learn-move="press"]').count()==1
  page.locator('[data-learn="exercises"]').first.tap();page.locator('#learn-back').tap()
  page.locator('#learn-equipment').select_option('kb');page.locator('#learn-family').select_option('squat');page.locator('#learn-search').fill('goblet')
  page.locator('[data-learn-move="squat"]').tap();assert page.locator('#movement-instruction > .status-available').count()==1
  page.locator('[data-confirm-learned="squat"]').tap();assert page.locator('#movement-instruction > .status-learned').count()==1
  assert page.evaluate('state.sessions.length')==0
  page.locator('[data-confirm-learned="squat"]').tap();assert page.locator('#movement-instruction > .status-available').count()==1
  page.locator('[data-tab="today"]').tap();page.locator('#start').tap();page.get_by_role('button',name='Warmup complete · start work').tap();page.locator('[data-editor],details#workout-focus').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
  page.locator('[data-set="0:0:weight"]').fill('8');page.locator('[data-set="0:0:weight"]').dispatch_event('change');page.locator('[data-check="0:0"]').tap()
  page.get_by_role('button',name='Finish main work · cooldown').tap();(page.locator('#finish-kind').select_option('partial') if page.locator('#finish-kind').count() else None);page.locator('#save-workout').tap()
  page.locator('[data-tab="learn"]').tap();assert page.locator('#movement-instruction > .status-practicing').count()==1
  assert page.evaluate('E.stateFor(state,"squat").streak')==0 and page.evaluate('state.sessions.length')==1
  # A reader cannot edit saved flags, but can browse lessons and pathway controls.
  reader=context.new_page();reader.goto(base);reader.wait_for_function('storageReady && !storageWritable');reader.locator('[data-tab="learn"]').tap()
  reader.locator('[data-learn-move="getupHand"]').tap();assert reader.locator('#movement-instruction').count()==1
  assert reader.locator('[data-confirm-learned="getupHand"]').is_disabled()
  reader.locator('[data-learn="pathways"]').first.tap();reader.locator('#pathway-movement').select_option('getupHipPass');assert reader.locator('#focused-pathway').count()==1
  reader.close()
  page.evaluate('navigator.serviceWorker.ready.then(()=>true)');context.set_offline(True);page.reload();page.wait_for_function('storageReady && storageWritable');page.locator('[data-tab="learn"]').tap()
  page.locator('[data-learn-move="getupHand"]').tap();assert page.locator('#movement-instruction > .status-blocked').count()==1
  assert page.locator('#movement-instruction .video-link').get_attribute('href')==records[372]['url']
  page.locator('.source-coverage summary').tap();page.locator('#movement-instruction [data-open-source="372"]').first.tap();page.locator('#transcript-dialog').wait_for(state='visible')
  assert 'press roll elbow hand' in page.locator('#transcript-body').inner_text().lower();page.get_by_role('button',name='Close',exact=True).tap()
  page.locator('[data-learn="pathways"]').first.tap();page.locator('#focused-pathway').scroll_into_view_if_needed();page.screenshot(path='/tmp/strength-learn-review.png')
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
  assert page.evaluate('state.sessions.length')==1
  assert not errors,errors
  print('PASS: mobile Learn filters/instructions, all four statuses, touch maps and dimensions, exact video/new-tab target, read-only education, no false progression, offline corpus and saved history',flush=True)
  browser.close()
finally:server.shutdown();server.server_close();thread.join()
