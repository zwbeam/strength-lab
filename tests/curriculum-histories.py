"""Real HTTP histories for get-ups and single-arm club foundations.
Self-reported form events validate software, not physical training efficacy.
"""
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
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.on('dialog',lambda dialog:dialog.accept('10') if dialog.type=='prompt' else dialog.accept())
  epoch=datetime(2026,1,1,12,tzinfo=timezone.utc);page.clock.install(time=epoch);days=0
  page.goto(f'http://127.0.0.1:{server.server_port}/')
  def train():page.locator('[data-tab="today"]').click()
  def settings():page.locator('[data-tab="settings"]').click()
  def advance(gap=4):
   global days
   days+=gap;page.clock.set_system_time(epoch+timedelta(days=days));train()
  def configure(block,skills):
   settings();page.locator('#program-block').select_option(block)
   page.get_by_text('Prerequisite skills',exact=True).click()
   for skill in skills:page.locator(f'[data-skill="{skill}"]').check()
   page.locator('#save-programming').click();train()
  def record(continuous=True,imbalance=False,pain=False,clock_check=False,check_rest=False):
   page.locator('#start').click();page.get_by_role('button',name='Warmup complete · start work').click();page.locator('[data-editor],details#workout-focus').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
   if clock_check:
    page.locator('[data-movement-timer="0"]').click();assert page.locator('#clock').inner_text()=='03:00'
    page.get_by_role('button',name='Pause',exact=True).click();page.reload()
    assert page.get_by_role('button',name='Resume',exact=True).count()==1
   result=page.evaluate('''({continuous,imbalance,pain,checkRest})=>{
    let noRestWithin=false,breakBetween=false;
    const indexes=Array.from(document.querySelectorAll('[data-check]')).map(el=>el.dataset.check);
    for(const index of indexes){
     const [i,j]=index.split(':').map(Number),total=draft.plan.items[i].durationScope==='total';
     if(total)for(const [field,value] of [['leftReps',imbalance?2:4],['rightReps',3]]){const el=document.querySelector(`[data-set="${index}:${field}"]`);el.value=String(value);el.dispatchEvent(new Event('change',{bubbles:true}));}
     for(const field of ['bothSides','continuous']){const el=document.querySelector(`[data-set="${index}:${field}"]`);if(el){el.checked=field==='continuous'?continuous:true;el.dispatchEvent(new Event('change',{bubbles:true}));}}
     document.querySelector(`[data-check="${index}"]`).click();
     if(checkRest&&i===0&&j===0)noRestWithin=draft.clock.kind==='work'&&draft.clock.item===0&&SessionTimer.queue(draft).filter(entry=>entry.item===0&&entry.kind==='work').length===1;
     if(checkRest&&i===0&&draft.items[0].sets.every(set=>set.done))breakBetween=document.querySelector('#timer-label').textContent.startsWith('Rest between movements')&&document.querySelector('#clock').textContent==='02:00';
    }
    if(pain){const el=document.querySelector('[data-pain="0"]');el.checked=true;el.dispatchEvent(new Event('change',{bubbles:true}));}
    return {noRestWithin,breakBetween};
   }''',dict(continuous=continuous,imbalance=imbalance,pain=pain,checkRest=check_rest))
   if check_rest:assert result=={'noRestWithin':True,'breakBetween':True},result
   page.get_by_role('button',name='Finish main work · cooldown').click();(page.locator('#finish-kind').select_option('partial') if page.locator('#finish-kind').count() else None);page.locator('#save-workout').click()
   return page.evaluate('state.sessions.at(-1).items')
  settings()
  for id,weight in [('getup','8'),('clubInside','5'),('clubOutside','5'),('clubShield','5')]:page.locator(f'[data-weight="{id}"]').fill(weight)
  page.locator('#save-weights').click()
  configure('getup',[]);assert page.locator('#start').count()==0
  configure('getup',['floorPress','rollToElbow','pressToHand','hipPass','getupOverhead','getup'])
  for seconds in range(180,601,60):
   for repeat in range(2):
    advance();text=page.locator('.list-item').first.inner_text()
    assert f'1 × {seconds} sec total, alternating sides' in text,text
    assert '/ side' not in text
    if seconds==600 and repeat==0:
     page.locator('#today-minutes').select_option('15');assert page.locator('#start').count()==0
     page.locator('#today-minutes').select_option('20');assert page.locator('#start').count()==1
     page.locator('#today-minutes').select_option('45')
    item=record(clock_check=seconds==180 and repeat==0)[0]
    assert item['completed'] and item['actualReps']==seconds and item['sourceParameters']==423,item
  print('PASS: get-up 3–10 minute history, total-time units, weaker-side allowance, prerequisite gates, timer persistence and short-session deferral',flush=True)
  settings();page.locator('[data-equipment="kb"]').fill('8,10,12,16');page.locator('#save-equipment').click()
  page.locator('[data-tab="progress"]').click()
  details=page.locator('details').filter(has=page.locator('[data-weight-for="getup"]'));details.locator('summary').click();page.locator('[data-weight-for="getup"]').click()
  advance();assert '180 sec total' in page.locator('.list-item').inner_text();assert '10 kg' in page.locator('.list-item').inner_text()
  assert not record(imbalance=True)[0]['completed']
  advance();assert not record(continuous=False)[0]['completed']
  advance();item=record()[0];assert item['mode']=='rebuild' and item['targetReps']<180 and not item['completed']
  advance();record(pain=True);train();assert page.locator('#start').count()==0
  page.locator('[data-tab="progress"]').click();review=page.locator('details').filter(has=page.locator('[data-resolve-pain="getup"]'));review.locator('summary').click();page.locator('[data-resolve-pain="getup"]').click()
  advance(28);assert '120 sec total' in page.locator('.list-item').inner_text();item=record()[0];assert item['mode']=='reentry' and not item['completed']
  configure('singleClub',[]);assert page.locator('#start').count()==0
  configure('singleClub',['clubTwoHandFoundation','clubGrip','clubInside','clubOutside','clubShield'])
  advance();items=record(continuous=False);assert all(not item['completed'] for item in items)
  for sets in range(4,21):
   for repeat in range(2):
    advance(3);assert page.locator('.list-item').count()==3
    assert all(f'{sets} × 5' in text for text in page.locator('.list-item').all_text_contents())
    if sets==20 and repeat==0:
     page.locator('#today-minutes').select_option('15');assert page.locator('#start').count()==0
     page.locator('#today-minutes').select_option('20');assert page.locator('.list-item').count()==1
     page.locator('#today-minutes').select_option('45')
    items=record(check_rest=sets==4 and repeat==0)
    assert all(item['completed'] and item['targetSets']==sets and item['rest']==0 and item['sourceParameters']==578 for item in items)
  page.reload()
  assert page.evaluate('state.sessions.filter(s=>s.block==="getup").length')==21
  assert page.evaluate('state.sessions.filter(s=>s.block==="singleClub").length')==35
  page.locator('[data-tab="learn"]').click()
  assert page.get_by_text('Single-arm club outside circle',exact=True).count()>=1
  assert not errors,errors
  print('PASS: 34 complete single-arm club exposures (102 movement records), interrupted-work rejection, no inter-set rest, between-movement rest, full overview, duration deferrals, saved get-up data preserved',flush=True)
  browser.close()
finally:
 server.shutdown();server.server_close();thread.join()
