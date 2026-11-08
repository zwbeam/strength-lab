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
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept('10') if d.type=='prompt' else d.accept())
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
  settings();page.locator('[data-equipment="kb"]').fill('8,10');page.locator('#save-setup').click();page.locator('[data-weight="deadlift"]').fill('8');page.locator('#save-weights').click()
  configure('hingePathway',['hingePattern']);assert ids()==['hingePractice']
  assert not record(partial=True)[0]['completed']
  for _ in range(2):next_day();assert record()[0]['completed']
  next_day();assert page.locator('#start').count()==0 # no automatic skill certification
  configure('hingePathway',['deadliftTechnique']);assert ids()==['deadlift']
  for n in range(6):
   if n:next_day()
   if n==2:page.locator('#today-minutes').select_option('15')
   r=record()[0];assert r['completed'] and r['weight']==8 and r['sourceParameters'] is None
   train();page.locator('#today-minutes').select_option('45')
  page.locator('[data-tab="progress"]').click();page.locator('#movement-progress,#working-loads').evaluate_all('(els)=>els.forEach(el=>el.open=true)');page.locator('details').filter(has=page.locator('[data-weight-for="deadlift"]')).last.locator('summary').click();page.locator('[data-weight-for="deadlift"]').click();train()
  assert ids()==['hingePractice'] # changed child load cannot maintain stale parent evidence
  for n in range(3):
   next_day();r=record()[0]
   assert r['id']=='hingePractice' and r['completed']==(n>0)
  next_day();assert ids()==['deadlift'];assert page.evaluate('currentPlan().items[0].weight')==10
  assert not record(pain_id='deadlift')[0]['completed'];next_day();assert page.locator('#start').count()==0
  page.reload();page.wait_for_function('storageReady');assert page.evaluate('state.sessions.length')==13
  page.evaluate('navigator.serviceWorker.ready.then(()=>true)');page.context.set_offline(True);page.reload();page.wait_for_function('storageReady')
  assert page.evaluate('state.sessions.length')==13 and page.locator('#start').count()==0
  assert not errors,errors
  print('PASS: 13 actual unloaded/loaded hinge workouts, partial work, explicit skill gate, short duration, complete load cycle, owned 25% increase, stale-parent requalification, pain hold and offline history',flush=True)
  browser.close()
finally:
 server.shutdown();server.server_close();thread.join()
