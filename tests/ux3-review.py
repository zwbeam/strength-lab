"""Review 3 acceptance in a real Pixel 5 touch browser; emulation, not a device."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
from pathlib import Path
from datetime import datetime,timedelta,timezone
import argparse,json,os
from urllib.parse import urlsplit,unquote
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--url');args=parser.parse_args();network={}
if args.url:
 if urlsplit(args.url).scheme!='https':raise SystemExit('Public verification requires HTTPS')
 if os.environ.get('SSL_CERT_FILE'):os.environ.setdefault('NODE_EXTRA_CA_CERTS',os.environ['SSL_CERT_FILE'])
 proxy=urlsplit(os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY') or '')
 if proxy.hostname:
  config={'server':f'{proxy.scheme}://{proxy.hostname}:{proxy.port or 80}'}
  if proxy.username:config['username']=unquote(proxy.username)
  if proxy.password:config['password']=unquote(proxy.password)
  network['proxy']=config
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));thread=Thread(target=server.serve_forever,daemon=True);thread.start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);context=browser.new_context(**p.devices['Pixel 5'],**network);page=context.new_page();errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.add_init_script('window.testAlerts=[];window.alert=m=>testAlerts.push(m)')
  # Audio is tested as actual oscillator invocations; hardware output needs Android review.
  page.add_init_script('''window.beeps=0;window.AudioContext=class {state='running';currentTime=0;destination={};resume(){return Promise.resolve()}createGain(){return {gain:{value:0},connect(){}}}createOscillator(){return {frequency:{value:0},connect(){},start(){window.beeps++},stop(){}}}};''')
  epoch=datetime(2026,11,8,12,tzinfo=timezone.utc);page.clock.install(time=epoch);base=args.url.rstrip('/')+'/' if args.url else f'http://127.0.0.1:{server.server_port}/';page.goto(base);page.wait_for_function('storageReady && storageWritable')
  assert page.locator('.calendar-day').count()==7 and page.locator('#cycle-progress').count()==0
  page.locator('[data-week="1"]').tap();assert page.locator('.calendar-day').count()==7;page.locator('[data-calendar-today]').tap()
  page.locator('[data-tab="settings"]').tap();assert not page.locator('#advanced-settings').evaluate('(el)=>el.open')
  page.locator('#training-days').select_option('3');page.locator('[data-activity-type="mountain"]').check();page.locator('#save-setup').tap()
  page.locator('#advanced-settings>summary').tap()
  for id,weight in [('squat','16'),('press','12'),('row','12')]:page.locator(f'[data-weight="{id}"]').fill(weight)
  page.locator('#save-weights').tap();page.locator('[data-tab="today"]').tap()
  identity=page.evaluate('C.project(state,today())[0].key')
  page.get_by_text('Reschedule workout',exact=True).tap();page.locator('#move-workout-date').fill('2026-11-10');page.locator('[data-move-workout]').tap()
  assert page.evaluate('C.project(state,today())[0].date')=='2026-11-10'
  page.get_by_text('Reschedule workout',exact=True).tap();page.locator('#move-workout-date').fill('2026-11-08');page.locator('[data-move-workout]').tap()
  assert page.evaluate('C.project(state,today())[0].key')==identity

  page.locator('#activity-form>summary').tap();page.locator('#activity-duration').fill('120');page.locator('#activity-effort').select_option('hard');page.locator('#save-activity').tap()
  assert page.evaluate('state.activities.length')==1 and page.evaluate('state.sessions.length')==0
  assert page.evaluate('C.project(state,today())[0].key')==identity
  assert page.evaluate('C.project(state,today())[0].date')=='2026-11-10'
  page.locator('#pause-training>summary').tap();page.locator('#pause-kind').select_option('duration');page.locator('#pause-days').fill('7');page.locator('#apply-pause').tap()
  assert page.evaluate('E.trainingPaused(state,today())') and page.locator('#start').count()==0
  page.clock.set_system_time(epoch+timedelta(days=20));page.locator('[data-tab="today"]').tap()
  assert not page.evaluate('E.trainingPaused(state,today())') and page.evaluate('C.project(state,today())[0].key')==identity
  page.locator('[data-calendar-today]').tap();assert page.locator('#start').count()==1
  page.locator('#today-minutes').select_option('30');page.locator('#today-readiness').select_option('low');assert 'reduced practice' in page.locator('#adjustment-explanation').inner_text()
  page.locator('#start').tap();assert page.evaluate('draft.originalPlan.budget.total')==45 and page.evaluate('draft.plan.budget.total')==30
  page.get_by_role('button',name='Warm-up done · begin work',exact=True).tap()
  assert page.locator('#clock').inner_text()=='REPS' and not page.evaluate('draft.clock.running')
  page.locator('#timer-primary').tap();assert page.evaluate('draft.clock.kind')=='rest' and page.evaluate('draft.clock.running')
  page.evaluate('''()=>{T.pause(draft);draft.clock.remaining=4;T.resume(draft);saveDraft();render()}''')
  page.clock.fast_forward(1000);assert page.locator('#timer-cue').inner_text()=='3'
  page.clock.fast_forward(1000);assert page.locator('#timer-cue').inner_text()=='2'
  page.clock.fast_forward(1000);assert page.locator('#timer-cue').inner_text()=='1'
  page.clock.fast_forward(1000);assert page.evaluate('beeps')>=4
  assert page.evaluate('draft.items.every(i=>i.sets.every(s=>!s.done))')
  page.locator('[data-edit-movement="active:0"]').tap();page.locator('[data-set="0:0:reps"]').fill('4');page.locator('[data-set="0:0:reps"]').dispatch_event('change')
  page.locator('[data-edit-movement="active:1"]').tap();assert page.locator('[data-editor][open]').count()==1 and page.evaluate('draft.items[0].sets[0].reps')==4
  page.locator('#workout-overview [data-instruction="press"]').tap();page.get_by_role('button',name='Close instruction').tap();assert page.evaluate('draft.items[0].sets[0].reps')==4
  page.evaluate('scrollTo(0,document.body.scrollHeight)');box=page.locator('.timer').bounding_box();assert box['y']>=-1 and box['y']+box['height']<844
  page.locator('#save-workout').tap();assert page.evaluate('draft===null && state.sessions.length===1')
  assert page.locator('.history-table').count()==1 and page.evaluate('state.sessions[0].items.every(x=>!x.completed)')
  page.locator('[data-edit-history]').tap();page.locator('[data-edit-movement="history:0"]').tap();page.locator('[data-hset="0:0:reps"]').fill('3');page.locator('[data-hset="0:0:reps"]').dispatch_event('change');page.locator('#save-correction').tap();assert page.evaluate('state.sessions[0].corrections.length')==1
  page.locator('[data-tab="learn"]').tap();page.locator('[data-learn="programming"]').tap();assert page.locator('#programming-education>details').count()>=9
  page.locator('#programming-education>details').first.locator('summary').tap();assert 'unfinished' in page.locator('#programming-education').inner_text()
  assert page.locator('#programming-education a').first.get_attribute('href')=='https://www.youtube.com/watch?v=sAcBo4H__hE'
  page.locator('[data-tab="settings"]').tap();page.locator('#advanced-settings>summary').tap()
  with page.expect_download() as download:page.locator('#export').tap()
  data=json.loads(Path(download.value.path()).read_text());assert len(data['activities'])==1 and data['sessions'][0]['corrections']
  page.locator('#import').set_input_files({'name':'roundtrip.json','mimeType':'application/json','buffer':json.dumps(data).encode()});page.wait_for_function('state.activities.length===1')
  page.evaluate('navigator.serviceWorker.ready.then(()=>true)');context.set_offline(True);page.reload();page.wait_for_function('storageReady && storageWritable');assert page.evaluate('state.activities.length===1 && state.sessions.length===1')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  assert not errors,errors;print('PASS: seven-day calendar/next week; activity displacement without credit; timed pause/vacation; real adjustments; untimed reps/rest-only; visual 3–2–1 and oscillator completion cue; single editor; sticky timer/instruction return; one-action finish; history correction; grounded Programming; backup and offline reload',flush=True)
  page.screenshot(path='/tmp/strength-ux3-review.png');browser.close()
finally:server.shutdown();server.server_close();thread.join()
