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
  configure('groundPractice',['hipDropTwoHand','bearSquat'])
  assert set(ids())=={'hipDropTwoHand','bearSquat'}
  assert not record(partial=True)[0]['completed']
  for _ in range(2):next_day();assert all(r['completed'] for r in record())
  next_day();assert 'hipDropSingleHand' not in ids() # evidence does not confirm the skill
  configure('groundPractice',['hipDropSingleHand']);assert 'hipDropSingleHand' in ids()
  for n in range(8):
   next_day()
   if n==2:page.locator('#today-minutes').select_option('15')
   assert page.evaluate('currentPlan().estimated<=currentPlan().cap')
   assert all(r['completed'] and r['weight']==0 and r['sourceParameters'] is None for r in record())
   train();page.locator('#today-minutes').select_option('45')
  settings();page.locator('[data-equipment="kb"]').fill('');page.locator('[data-equipment="club"]').fill('');page.locator('#save-setup').click();train()
  assert 'hipDropSingleHand' in ids()
  next_day(28);assert 'hipDropSingleHand' not in ids();assert all(rx['mode']=='reentry' for rx in page.evaluate('currentPlan().items'))
  assert not any(r['completed'] for r in record())
  for _ in range(2):next_day();assert all(r['completed'] for r in record())
  next_day();assert 'hipDropSingleHand' in ids()
  record(pain_id='hipDropTwoHand');train();assert 'hipDropSingleHand' not in ids()
  page.reload();assert 'hipDropSingleHand' not in ids()
  settings();details=page.locator('details').filter(has=page.locator('[data-intermediate-reps="bearSquat"]')).last;page.locator('#movement-progress,#working-loads').evaluate_all('(els)=>els.forEach(el=>el.open=true)');details.locator('summary').click()
  page.locator('[data-intermediate-reps="bearSquat"]').select_option('90');page.locator('[data-intermediate-start="bearSquat"]').fill('1');page.locator('[data-intermediate-end="bearSquat"]').fill('3');page.locator('#save-programming').click();train()
  assert page.evaluate('currentPlan().items.find(rx=>rx.id==="bearSquat").reps')==90
  assert page.evaluate('state.sessions.length')==15
  next_day(1);settings();page.get_by_text('Recovery and scheduling defaults',exact=True).click();page.locator('#training-minGapDays').select_option('2');page.locator('#save-programming').click();train()
  assert page.locator('#start').count()==0 and 'Select a longer session' not in page.get_by_role('status').inner_text()
  assert 'bearSquat' in page.evaluate('currentPlan().scheduled')
  next_day(2);assert 'bearSquat' in ids()
  page.evaluate('navigator.serviceWorker.ready.then(()=>true)');page.context.set_offline(True);page.reload();assert page.evaluate('state.sessions.length')==15
  assert not errors,errors
  print('PASS: 15 generated ground sessions: partial work, explicit skill gate, multiweek advancement, short duration, no equipment, stale prerequisites/requalification, parent pain hold and offline history',flush=True)
  browser.close()
finally:
 server.shutdown();server.server_close();thread.join()
