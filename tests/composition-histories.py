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
  for id,weight in [('snatch','8'),('front','5'),('cast','5'),('circles','5')]:page.locator(f'[data-weight="{id}"]').fill(weight)
  page.locator('#save-weights').click();page.get_by_text('Prerequisite skills',exact=True).click()
  for checkbox in page.locator('[data-skill]').all():checkbox.check()
  page.get_by_text('Coordinated program',exact=True).click();page.locator('#composition-enabled').check()
  blocks=['snatch','club','groundPractice','hingePractice']
  for checkbox in page.locator('[data-composition-block]').all():checkbox.set_checked(checkbox.get_attribute('data-composition-block') in blocks)
  page.locator('#save-programming').click();train()
  seen={}
  for n in range(32):
   next_day();block=page.evaluate('currentPlan().block');seen[block]=seen.get(block,0)+1
   assert page.locator('#program-decision').count()==1
   assert page.evaluate('currentPlan().estimated<=currentPlan().cap')
   records=record(partial=n==0)
   if n==0:assert not records[0]['completed']
   else:assert all(r['completed'] for r in records)
   assert page.evaluate('state.sessions.at(-1).programMode')=='coordinated'
  assert seen=={block:8 for block in blocks},seen
  next_day(28);train();assert all(rx['mode']=='reentry' for rx in page.evaluate('currentPlan().items'))
  assert not any(r['completed'] for r in record())
  next_day();page.locator('#today-minutes').select_option('15')
  assert page.evaluate('currentPlan().estimated<=currentPlan().cap')
  r=record(pain_id=ids()[0]);assert not r[0]['completed'];train()
  pain_id=r[0]['id'];assert pain_id not in ids()
  # Changing equipment and skills must select from the remaining eligible blocks.
  settings();page.locator('[data-equipment="kb"]').fill('');page.locator('[data-equipment="club"]').fill('');page.locator('#save-setup').click();train()
  assert page.evaluate('currentPlan().items.every(rx=>rx.bodyweight)')
  settings();page.get_by_text('Prerequisite skills',exact=True).click()
  for skill in ['hipDropTwoHand','hipDropSingleHand','bearSquat']:page.locator(f'[data-skill="{skill}"]').uncheck()
  page.locator('#save-programming').click();train();assert page.locator('#start').count()==0
  assert 'No workout is ready' in page.get_by_role('status').inner_text()
  settings();page.get_by_text('Prerequisite skills',exact=True).click();page.locator('[data-skill="bearSquat"]').check();page.locator('#save-programming').click();train()
  assert ids()==[] # the full 4-bout prescription does not fit the remaining 7 main-work minutes
  next_day();page.locator('#today-readiness').select_option('low');assert ids()==['bearSquat']
  assert not any(r['completed'] for r in record())
  train();page.locator('#today-readiness').select_option('normal')
  settings();page.locator('[data-equipment="kb"]').fill('8,12');page.locator('[data-equipment="club"]').fill('5');page.locator('#save-setup').click();train();next_day();page.locator('#today-minutes').select_option('45')
  assert page.evaluate('currentPlan().items.some(rx=>!rx.bodyweight)')
  assert not any(r['completed'] for r in record()) # reduced return after absence, not a free advancement
  count=page.evaluate('state.sessions.length');page.reload();page.wait_for_function('storageReady');assert page.evaluate('state.sessions.length')==count
  assert page.evaluate('state.programComposition.enabled')
  page.evaluate('navigator.serviceWorker.ready.then(()=>true)');page.context.set_offline(True);page.reload();page.wait_for_function('storageReady')
  assert page.evaluate('state.sessions.length')==36
  assert not errors,errors
  print('PASS: 36 real coordinated workouts across four blocks / multiple months, independent cycles, partial work, missed month, short duration, pain, equipment loss/return, skill regression, low readiness, decision UI and offline history',flush=True)
  browser.close()
finally:
 server.shutdown();server.server_close();thread.join()
