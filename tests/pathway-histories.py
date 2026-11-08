"""Actual application-generated practice paths; no fabricated session records."""
from datetime import datetime,timedelta,timezone
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
  page=browser.new_page(viewport={'width':390,'height':844});errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
  epoch=datetime(2026,1,1,12,tzinfo=timezone.utc);page.clock.install(time=epoch);days=0
  page.goto(f'http://127.0.0.1:{server.server_port}/')
  def settings():page.locator('[data-tab="settings"]').click();(page.locator('#advanced-settings').evaluate('(el)=>el.open=true') if page.locator('#advanced-settings').count() else None)
  def train():page.locator('[data-tab="today"]').click()
  def next_day(gap=3):
   global days
   days+=gap;page.clock.set_system_time(epoch+timedelta(days=days));train()
  def configure(block,skills):
   settings();page.locator('#program-block').select_option(block);page.get_by_text('Prerequisite skills',exact=True).click()
   for skill in skills:page.locator(f'[data-skill="{skill}"]').check()
   page.locator('#save-programming').click();train()
  def ids():return page.evaluate('currentPlan().items.map(rx=>rx.id)')
  def record(partial=False,pain_id=None):
   page.locator('#start').click();page.locator('[data-stage="work"]').click();page.locator('[data-editor],.partial-set,.method-fields,.notebook-exercise details').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
   assert page.locator('#workout-overview').count()==1
   page.evaluate('''({partial,painId})=>{
    const indexes=Array.from(document.querySelectorAll('[data-check]')).map(el=>el.dataset.check);
    for(const index of indexes){
     if(partial&&index==='0:0'){const el=document.querySelector('[data-set="0:0:reps"]');el.value=String(Number(el.value)-1);el.dispatchEvent(new Event('change',{bubbles:true}));}
     for(const field of ['bothSides','continuous','timingValid']){const el=document.querySelector(`[data-set="${index}:${field}"]`);if(el){el.checked=true;el.dispatchEvent(new Event('change',{bubbles:true}));}}
     document.querySelector(`[data-check="${index}"]`).click();
    }
    if(painId){const i=draft.plan.items.findIndex(rx=>rx.id===painId),el=document.querySelector(`[data-pain="${i}"]`);el.checked=true;el.dispatchEvent(new Event('change',{bubbles:true}));}
   }''',dict(partial=partial,painId=pain_id))
   page.locator('[data-stage="cooldown"]').click();(page.locator('#finish-kind').evaluate("el=>{el.closest('details').open=true;el.value='partial';el.dispatchEvent(new Event('change',{bubbles:true}))}") if page.locator('#finish-kind').count() else None);page.locator('#save-workout').click()
   return page.evaluate('state.sessions.at(-1).items')
  settings()
  for id in ['getupFloor','getupElbow','getupHand','getupHipPass']:page.locator(f'[data-weight="{id}"]').fill('8')
  for id in ['clubInside','clubOutside','clubShield','clubInsidePendulum','clubOutsidePendulum','clubFrontPullover','clubOutsidePullover','clubInsidePullover']:page.locator(f'[data-weight="{id}"]').fill('5')
  page.locator('#save-weights').click()
  configure('getupPractice',['floorPress']);assert ids()==['getupFloor']
  assert not record(partial=True)[0]['completed']
  for _ in range(2):next_day();assert ids()==['getupFloor'];assert record()[0]['completed']
  next_day();assert ids()==['getupFloor'] # evidence alone never confirms elbow skill
  configure('getupPractice',['rollToElbow']);assert 'getupElbow' in ids() and 'getupHand' not in ids()
  for _ in range(2):assert all(r['completed'] for r in record());next_day()
  configure('getupPractice',['pressToHand','hipPass']);assert 'getupHand' in ids() and 'getupHipPass' not in ids()
  for n in range(20):
   next_day()
   if n>=2:assert 'getupHipPass' in ids()
   if n==8:page.locator('#today-minutes').select_option('15')
   assert all(r['completed'] for r in record())
   train();page.locator('#today-minutes').select_option('45')
  assert page.evaluate('state.sessions.some(s=>s.items.some(r=>r.id==="getupHand"&&r.targetReps===10&&r.completed))')
  count=page.evaluate('state.sessions.length')
  settings();page.locator('[data-equipment="kb"]').fill('');page.locator('#save-setup').click();train();assert page.locator('#start').count()==0
  settings();page.locator('[data-equipment="kb"]').fill('8,10');page.locator('#save-setup').click()
  next_day(28);assert ids()==['getupFloor'];r=record()[0];assert r['mode']=='reentry' and r['targetReps']<5 and not r['completed']
  print('PASS: generated get-up pathway, explicit skill confirmations, partial-work rejection, hand rep endpoint, duration carryover, equipment loss and missed-month re-entry',flush=True)
  configure('clubIntermediate',['clubTwoHandFoundation','clubGrip','clubInside','clubOutside','clubShield'])
  for _ in range(2):next_day();assert set(ids())=={'clubInside','clubOutside','clubShield'};assert all(r['completed'] for r in record())
  train();assert page.locator('#start').count()==0 # practiced foundations cannot self-certify next techniques
  configure('clubIntermediate',['clubPendulumTwoHand','clubInsidePendulum','clubOutsidePendulum','clubFrontPullover'])
  for _ in range(2):next_day();assert set(ids())=={'clubInsidePendulum','clubOutsidePendulum','clubFrontPullover'};assert all(r['completed'] for r in record())
  configure('clubIntermediate',['clubOutsidePullover','clubInsidePullover'])
  for n in range(16):
   next_day()
   assert 'clubOutsidePullover' in ids()
   assert ('clubInsidePullover' in ids())==(n>=2)
   assert all(r['completed'] and r['sourceParameters'] is None for r in record())
  next_day();record(pain_id='clubFrontPullover');train()
  assert not {'clubFrontPullover','clubOutsidePullover','clubInsidePullover'}&set(ids())
  page.reload();assert page.evaluate('state.sessions.filter(s=>s.block==="getupPractice").length')==count+1
  assert not errors,errors
  print('PASS: generated club foundation support, staged pendulum/pullover availability over multiple weeks, active practice maintenance, transitive pain hold and saved earlier history',flush=True)
  browser.close()
finally:
 server.shutdown();server.server_close();thread.join()
