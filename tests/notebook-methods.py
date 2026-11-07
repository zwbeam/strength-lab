"""Multiweek one-confirmation histories across continuous, total-time and EMOM methods."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
from pathlib import Path
from datetime import datetime,timedelta,timezone
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));thread=Thread(target=server.serve_forever,daemon=True);thread.start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(**p.devices['Pixel 5']);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.add_init_script('window.testAlerts=[];window.alert=m=>testAlerts.push(m)')
  epoch=datetime(2026,1,1,12,tzinfo=timezone.utc);day=0;page.clock.install(time=epoch);page.goto(f'http://127.0.0.1:{server.server_port}/');page.wait_for_function('storageReady && storageWritable')
  def configure(block,weights,skills):
   page.locator('[data-tab="settings"]').tap()
   for id,value in weights.items():page.locator(f'[data-weight="{id}"]').fill(str(value))
   page.locator('#save-weights').tap();page.locator('#program-block').select_option(block);page.get_by_text('Prerequisite skills',exact=True).tap()
   for skill in skills:page.locator(f'[data-skill="{skill}"]').check()
   page.locator('#save-programming').tap();page.locator('[data-tab="today"]').tap()
  def next_day(gap=3):
   global day
   day+=gap;page.clock.set_system_time(epoch+timedelta(days=day));page.locator('[data-tab="today"]').tap()
  def start():page.locator('#start').tap();page.get_by_role('button',name='Warmup complete · start work').tap()
  def finish():
   page.locator('#finish-workout').tap();page.locator('#save-workout').tap();assert page.evaluate('draft===null');return page.evaluate('state.sessions.at(-1).items')
  configure('singleClub',{'clubInside':5,'clubOutside':5,'clubShield':5},['clubTwoHandFoundation','clubGrip','clubInside','clubOutside','clubShield'])
  for _ in range(2):
   next_day();start();items=finish();assert all(x['completed'] and x['targetSets']==4 for x in items)
  next_day();assert page.evaluate('currentPlan().items.every(x=>x.sets===5)');start();page.locator('[data-edit-movement="active:0"]').tap();page.locator('[data-set="0:0:leftReps"]').fill('3');page.locator('[data-set="0:0:leftReps"]').dispatch_event('change');assert not finish()[0]['completed']
  next_day();page.locator('#today-readiness').select_option('low');start();assert all(not x['completed'] for x in finish())
  next_day(28);assert page.evaluate('currentPlan().items.every(x=>x.mode==="reentry")');start();assert all(not x['completed'] for x in finish())
  assert page.evaluate('state.sessions.length')==5
  configure('getup',{'getup':8},['floorPress','rollToElbow','pressToHand','hipPass','getupOverhead','getup'])
  next_day();start();page.locator('#finish-workout').tap();page.locator('#save-workout').tap();assert page.evaluate('draft!==null && state.sessions.length===5')
  assert page.evaluate('testAlerts.at(-1).includes("actual completed get-ups")')
  page.locator('[data-edit-movement="active:0"]').tap()
  for side in ['left','right']:
   page.locator(f'[data-set="0:0:{side}Reps"]').fill('2');page.locator(f'[data-set="0:0:{side}Reps"]').dispatch_event('change')
  item=finish()[0];assert item['completed'] and item['targetReps']==180 and item['durationScope']=='total'
  configure('snatch',{'snatch':8},['swing','clean','overhead']);next_day();start();assert finish()[0]['completed']
  next_day();start();page.locator('[data-edit-movement="active:0"]').tap();page.locator('[data-set="0:0:roundSeconds"]').fill('120');page.locator('[data-set="0:0:roundSeconds"]').dispatch_event('change');assert not finish()[0]['completed']
  page.locator('[data-edit-history]').first.tap();page.locator('[data-edit-movement="history:0"]').tap();page.locator('[data-hset="0:0:roundSeconds"]').fill('60');page.locator('[data-hset="0:0:roundSeconds"]').dispatch_event('change');page.locator('#save-correction').tap()
  assert page.evaluate('state.sessions.at(-1).items[0].completed') and page.evaluate('E.prescription(state,"snatch").sets')==5
  assert page.evaluate('state.sessions[0].items.every(x=>x.completed)'),'Later block corrections must preserve club data'
  assert not errors,errors
  print('PASS: 8 one-confirmation sessions across weeks; continuous bilateral club progression/imbalance/readiness/missed month; explicit total-time get-up counts; snatch cadence deviation and historical correction/replay; independent earlier cycles',flush=True)
  browser.close()
finally:server.shutdown();server.server_close();thread.join()
