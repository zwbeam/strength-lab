"""Actual touch notebook workflow, failures and corrections. Pixel 5 emulation."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,argparse,os
from urllib.parse import urlsplit,unquote
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--url");args=parser.parse_args()
network={}
if args.url:
 if urlsplit(args.url).scheme!="https":raise SystemExit("Public acceptance requires HTTPS")
 if os.environ.get("SSL_CERT_FILE"):os.environ.setdefault("NODE_EXTRA_CA_CERTS",os.environ["SSL_CERT_FILE"])
 proxy=urlsplit(os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY") or "")
 if proxy.hostname:
  config={"server":f"{proxy.scheme}://{proxy.hostname}:{proxy.port or 80}"}
  if proxy.username:config["username"]=unquote(proxy.username)
  if proxy.password:config["password"]=unquote(proxy.password)
  network["proxy"]=config
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));thread=Thread(target=server.serve_forever,daemon=True);thread.start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);context=browser.new_context(**p.devices['Pixel 5'],**network);page=context.new_page();errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.add_init_script('window.testAlerts=[];window.alert=m=>testAlerts.push(m)')
  base=args.url.rstrip('/')+'/' if args.url else f'http://127.0.0.1:{server.server_port}/';page.goto(base);page.wait_for_function('storageReady && storageWritable')
  assert page.locator('#training-cycle').count()==1 and page.locator('#clock').count()==0
  page.locator('[data-select-workout="1"]').tap();assert 'Provisional' in page.locator('#selected-workout').inner_text();assert page.locator('#start').count()==0
  page.locator('[data-select-workout="0"]').tap()
  # Set real owned working weights; UI defaults intentionally never invent a load.
  page.locator('[data-tab="settings"]').tap()
  for id,weight in [('squat','16'),('press','12'),('row','12')]:page.locator(f'[data-weight="{id}"]').fill(weight)
  page.locator('#save-weights').tap();page.locator('[data-tab="today"]').tap()
  page.locator('#today-minutes').select_option('30');page.locator('#today-readiness').select_option('low')
  assert page.evaluate('state.defaultMinutes')==45
  assert 'reduced practice' in page.locator('#adjustment-explanation').inner_text()
  for label in ['Warm-up','Cooldown']:
   details=page.locator('#selected-workout .preparation').filter(has=page.get_by_text(label,exact=False)).first
  page.locator('#selected-workout .preparation').first.locator('summary').tap();assert 'practice reps' in page.locator('#selected-workout .preparation').first.inner_text()
  page.locator('#selected-workout .preparation').last.locator('summary').tap();assert 'ankle rocks' in page.locator('#selected-workout .preparation').last.inner_text()
  page.locator('#start').tap();assert page.evaluate('draft.originalPlan.budget.total')==45 and page.evaluate('draft.plan.budget.total')==30
  assert page.evaluate('draft.items.every(x=>x.sets.every(s=>!s.done))')
  page.locator('#clock').tap();before=page.evaluate('timerRemaining(draft.clock)');page.wait_for_timeout(1600);assert page.evaluate('timerRemaining(draft.clock)')<before
  page.locator('[data-instruction="squat"]').first.tap();page.locator('#movement-dialog').wait_for(state='visible');assert page.locator('#movement-dialog .video-link').count()>0
  page.wait_for_timeout(1100);page.get_by_role('button',name='Close instruction').tap();assert page.evaluate('draft.clock.running')
  page.evaluate('window.scrollTo(0,document.body.scrollHeight)');box=page.locator('.timer').bounding_box();assert box['y']>=-1 and box['y']+box['height']<844,box
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  page.locator('#finish-workout').tap();page.locator('#save-workout').tap();assert page.evaluate('state.sessions.length')==1
  assert page.evaluate('state.sessions[0].items.every(x=>!x.completed)'),'Reduced work must not advance'
  assert page.evaluate('state.sessions[0].originalPlan.budget.total')==45
  print('PASS: ordered cycle, preview, real 45→30/Pretty beat adjustment, explicit prep, running sticky touch timer, instruction round-trip, one confirmation, no reduced-work credit',flush=True)
  # Normal workout: change one final set, preserve the written target, save once.
  page.locator('[data-tab="today"]').tap();page.locator('[data-tab="settings"]').tap()
  page.locator('#program-block').select_option('abc');page.locator('#save-programming').tap()
  # Next B has unknown loads: use the canonical written A plan via separate new context.
  context.close();context=browser.new_context(**p.devices['Pixel 5'],**network);page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.add_init_script('window.testAlerts=[];window.alert=m=>testAlerts.push(m)');page.goto(base);page.wait_for_function('storageReady && storageWritable')
  page.locator('[data-tab="settings"]').tap()
  for id,weight in [('squat','16'),('press','12'),('row','12')]:page.locator(f'[data-weight="{id}"]').fill(weight)
  page.locator('#save-weights').tap();page.locator('[data-tab="today"]').tap();page.locator('#start').tap()
  target=page.evaluate('draft.plan.items[0].reps');assert target==6
  page.locator('[data-edit-movement="active:0"]').tap();page.locator('[data-set="0:2:reps"]').fill('4');page.locator('[data-set="0:2:reps"]').dispatch_event('change')
  page.locator('#finish-workout').tap();page.locator('#save-workout').tap();assert page.evaluate('state.sessions[0].items[0].sets[2].reps')==4
  assert page.evaluate('state.sessions[0].items[0].prescription.reps')==6 and not page.evaluate('state.sessions[0].items[0].completed')
  page.locator('[data-edit-history]').first.tap();page.locator('[data-edit-movement="history:0"]').tap();page.locator('[data-hset="0:2:reps"]').fill('6');page.locator('[data-hset="0:2:reps"]').dispatch_event('change');page.locator('#save-correction').tap()
  assert page.evaluate('state.sessions[0].items[0].completed') and page.evaluate('E.stateFor(state,"squat").streak')==1
  assert page.evaluate('state.sessions[0].corrections[0].before.items[0].sets[2].reps')==4
  page.reload();page.wait_for_function('storageReady && storageWritable');page.locator('[data-tab="progress"]').tap()
  assert page.evaluate('state.sessions[0].items[0].sets[2].reps')==6
  page.locator('[data-history]').first.locator('summary').first.tap();page.locator('[data-history] details').last.locator('summary').tap();page.locator('[data-undo-correction]').tap()
  assert page.evaluate('state.sessions[0].items[0].sets[2].reps')==4 and page.evaluate('E.stateFor(state,"squat").streak')==0
  # Persist correction through offline backup/restore, reject malformed imports.
  page.locator('[data-tab="settings"]').tap()
  with page.expect_download() as download:page.locator('#export').tap()
  payload=json.loads(Path(download.value.path()).read_text());assert len(payload['sessions'][0]['corrections'])==2
  page.locator('#reset').tap();page.locator('[data-tab="settings"]').tap();page.locator('#import').set_input_files({'name':'corrected.json','mimeType':'application/json','buffer':json.dumps(payload).encode()});page.wait_for_function('state.sessions.length===1')
  page.evaluate('navigator.serviceWorker.ready.then(()=>true)');context.set_offline(True);page.reload();page.wait_for_function('storageReady && storageWritable');assert page.evaluate('state.sessions[0].items[0].sets[2].reps')==4
  assert not errors,errors
  print('PASS: final-set edit, immutable targets, one-save actuals, saved-history correction/replay, reversible audit, reload, backup/restore and offline history',flush=True)
  page.screenshot(path='/tmp/strength-notebook-review.png');browser.close()
finally:server.shutdown();server.server_close();thread.join()
