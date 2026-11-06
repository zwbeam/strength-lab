"""Application-generated bodyweight histories, baseline review and storage roundtrip."""
from datetime import datetime,timedelta,timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json
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
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('dialog',lambda d:d.accept('10') if d.type=='prompt' else d.accept())
  epoch=datetime(2026,1,1,12,tzinfo=timezone.utc);page.clock.install(time=epoch);days=0
  page.goto(f'http://127.0.0.1:{server.server_port}/')
  def settings():page.locator('[data-tab="settings"]').click()
  def train():page.locator('[data-tab="today"]').click()
  def advance(gap=3):
   global days
   days+=gap;page.clock.set_system_time(epoch+timedelta(days=days));train()
  def configure(block,skill):
   settings();page.locator('#program-block').select_option(block);page.get_by_text('Prerequisite skills',exact=True).click();page.locator(f'[data-skill="{skill}"]').check();page.locator('#save-programming').click();train()
  def record(partial=False,quality='clean',pain=False,quick=False):
   page.locator('#start').click();page.get_by_role('button',name='Warmup complete · start work').click()
   assert page.locator('[data-set="0:0:weight"]').input_value()=='0'
   assert page.locator('[data-set="0:0:weight"]').get_attribute('readonly') is not None
   if quick:page.get_by_role('button',name='Complete next set').click();assert page.locator('[role="progressbar"]').get_attribute('aria-valuenow')=='1'
   page.evaluate('''({partial,quality,pain})=>{
    const indexes=Array.from(document.querySelectorAll('[data-check]')).map(b=>b.dataset.check);
    for(const index of indexes){
     if(partial&&index==='0:0'){const el=document.querySelector('[data-set="0:0:reps"]');el.value=String(Number(el.value)-1);el.dispatchEvent(new Event('change',{bubbles:true}));}
     const timing=document.querySelector(`[data-set="${index}:timingValid"]`);if(timing){timing.checked=true;timing.dispatchEvent(new Event('change',{bubbles:true}));}
     const button=document.querySelector(`[data-check="${index}"]`);if(button.textContent!=='✓')button.click();
    }
    const select=document.querySelector('[data-quality="0"]');select.value=quality;select.dispatchEvent(new Event('change',{bubbles:true}));
    if(pain){const el=document.querySelector('[data-pain="0"]');el.checked=true;el.dispatchEvent(new Event('change',{bubbles:true}));}
   }''',dict(partial=partial,quality=quality,pain=pain))
   page.get_by_role('button',name='Finish main work · cooldown').click();page.locator('#save-workout').click()
   return page.evaluate('state.sessions.at(-1).items[0]')
  settings();page.locator('[data-equipment="kb"]').fill('');page.locator('[data-equipment="club"]').fill('');page.locator('#save-equipment').click()
  configure('hingePractice','hingePattern');assert 'Bodyweight / no external load' in page.locator('.list-item').inner_text()
  assert not record(partial=True)['completed']
  for n in range(4):advance();r=record(quick=n==0);assert r['completed'] and r['weight']==0 and r['bodyweight']
  assert page.locator('[data-weight-for="hingePractice"]').count()==0
  configure('pushup','pushupTechnique');assert page.locator('#start').count()==0
  settings();details=page.locator('details').filter(has=page.locator('[data-pushup-baseline="pushup"]'));details.locator('summary').click();page.locator('[data-pushup-baseline="pushup"]').fill('10');page.locator('#save-programming').click();train()
  page.locator('#today-minutes').select_option('15');assert page.locator('#start').count()==0
  page.locator('#today-minutes').select_option('20');assert page.locator('#start').count()==1
  page.locator('#today-minutes').select_option('45')
  assert not record(partial=True)['completed']
  for sets in range(10,31):
   for repeat in range(2):
    advance();assert f'{sets} × 4' in page.locator('.list-item').inner_text()
    r=record();assert r['completed'] and r['targetSets']==sets and r['weight']==0 and r['sourceParameters']==609
  print('PASS: unloaded hinge and full 42-exposure 10–30-round push-up history without equipment; zero-load quick logging and incomplete-work rejection',flush=True)
  movement=page.locator('details').filter(has=page.locator('[data-retest-pushup]'));movement.locator('summary').click();page.locator('[data-retest-pushup]').click()
  advance();assert '10 × 4' in page.locator('.list-item').inner_text();assert not record(quality='minor')['completed']
  advance();record(pain=True);train();assert page.locator('#start').count()==0
  page.locator('[data-tab="progress"]').click();review=page.locator('details').filter(has=page.locator('[data-resolve-pain="pushup"]'));review.locator('summary').click();page.locator('[data-resolve-pain="pushup"]').click()
  advance(28);assert '7 × 4' in page.locator('.list-item').inner_text();r=record();assert r['mode']=='reentry' and not r['completed']
  settings();before=page.evaluate('JSON.stringify(state)');payload=json.loads(before);payload['sessions'][0]['notes']='restored-bodyweight-history'
  page.locator('#import').set_input_files({'name':'bodyweight-history.json','mimeType':'application/json','buffer':json.dumps(payload).encode()})
  page.wait_for_function('state.sessions[0].notes === "restored-bodyweight-history"');page.reload()
  assert page.evaluate('state.sessions.filter(s=>s.block==="hingePractice").length')==5
  assert page.evaluate('state.sessions.some(s=>s.items.some(r=>r.id==="pushup"&&r.bodyweight&&r.weight===0))')
  page.evaluate('navigator.serviceWorker.ready.then(()=>true)');page.context.set_offline(True);page.reload();assert page.locator('#app').inner_text()
  assert not errors,errors
  print('PASS: explicit baseline-cycle restart, technique/pain/re-entry controls, zero-load history restore and offline reload',flush=True)
  browser.close()
finally:
 server.shutdown();server.server_close();thread.join()
