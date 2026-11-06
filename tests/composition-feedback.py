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
  def settings():page.locator('[data-tab="settings"]').click()
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
   page.locator('#start').click();page.get_by_role('button',name='Warmup complete · start work').click()
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
   page.get_by_role('button',name='Finish main work · cooldown').click();page.locator('#save-workout').click()
   return page.evaluate('state.sessions.at(-1).items')
  settings()
  for id,weight in [('snatch','8'),('front','5'),('cast','5'),('circles','5')]:page.locator(f'[data-weight="{id}"]').fill(weight)
  page.locator('#save-weights').click();page.get_by_text('Prerequisite skills',exact=True).click()
  for checkbox in page.locator('[data-skill]').all():checkbox.check()
  page.get_by_text('Coordinated program',exact=True).click();page.locator('#composition-enabled').check()
  blocks=['snatch','club','groundPractice','hingePractice']
  for checkbox in page.locator('[data-composition-block]').all():checkbox.set_checked(checkbox.get_attribute('data-composition-block') in blocks)
  page.locator('#save-programming').click();train()
  for n in range(4):
   next_day(6)
   if n<3:assert page.locator('#program-cadence').count()==0
   if n==0:
    page.locator('#program-decision summary').click();assert 'qualifying exposures' in page.locator('#program-decision').inner_text()
   assert all(r['completed'] for r in record())
  train();assert page.locator('#start').count()==0 # same-day overlapping work is still spaced
  next_day(1);page.locator('#program-decision summary').click()
  assert page.evaluate('currentPlan().composition.cadence.estimatedReturnDays')==24
  assert 'about 24 days' in page.locator('#program-cadence').inner_text()
  assert 'fewer active blocks' in page.locator('#program-cadence-warning').inner_text()
  assert 'no advancement credit' in page.locator('#program-decision').inner_text()
  settings();page.get_by_text('Coordinated program',exact=True).click()
  for block in ['snatch','club']:page.locator(f'[data-composition-block="{block}"]').uncheck()
  page.locator('#save-programming').click();train();page.locator('#program-decision summary').click()
  assert page.evaluate('currentPlan().composition.cadence.estimatedReturnDays')==12
  assert page.locator('#program-cadence-warning').count()==0
  assert page.evaluate('state.sessions.length')==4
  assert not errors,errors
  print('PASS: actual four-block cadence feedback from four generated workouts, visible rotation/absence explanation and clean-exposure goal; fewer blocks clear warning without altering history',flush=True)
  browser.close()
finally:
 server.shutdown();server.server_close();thread.join()
