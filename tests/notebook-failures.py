"""Real notebook final-save/correction rollback, partial recovery and writer guards."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));thread=Thread(target=server.serve_forever,daemon=True);thread.start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);context=browser.new_context(**p.devices['Pixel 5']);page=context.new_page();errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.add_init_script('window.testAlerts=[];window.alert=m=>testAlerts.push(m)')
  base=f'http://127.0.0.1:{server.server_port}/';page.goto(base);page.wait_for_function('storageReady && storageWritable')
  def snapshot():return page.evaluate('({state:localStorage.getItem(KEY),draft:localStorage.getItem(DRAFT)})')
  page.locator('[data-tab="settings"]').tap();page.locator('#program-block').select_option('hingePractice');page.get_by_text('Prerequisite skills',exact=True).tap();page.locator('[data-skill="hingePattern"]').check();page.locator('#save-programming').tap()
  page.locator('[data-tab="today"]').tap();page.locator('#start').tap();page.get_by_role('button',name='Warmup complete · start work').tap()
  page.locator('[data-edit-movement="active:0"]').tap();old=page.evaluate('draft.items[0].sets.length');page.get_by_role('button',name='Add set',exact=True).tap();assert page.evaluate('draft.items[0].sets.length')==old+1
  page.get_by_role('button',name=f'Remove set {old+1}',exact=True).tap();assert page.evaluate('draft.items[0].sets.length')==old
  page.locator('[data-set="0:0:done"]').check();page.locator('[data-set="0:0:reps"]').fill('1');page.locator('[data-set="0:0:reps"]').dispatch_event('change')
  page.locator('#finish-workout').tap();page.locator('#finish-kind').select_option('partial');page.evaluate('navigator.serviceWorker.ready.then(()=>true)');page.reload();page.wait_for_function('storageReady && storageWritable');page.locator('#finish-workout').tap();assert page.locator('#finish-kind').input_value()=='partial'
  before=snapshot();page.evaluate('''()=>{window.nativeRemove=Storage.prototype.removeItem;Storage.prototype.removeItem=function(k){if(k===DRAFT)throw Error('Injected final save failure');return nativeRemove.call(this,k)}}''')
  page.locator('#save-workout').tap();assert snapshot()==before and page.evaluate('state.sessions.length')==0 and page.evaluate('draft!==null')
  page.evaluate('()=>{Storage.prototype.removeItem=nativeRemove;}');page.locator('#save-workout').tap();assert page.evaluate('state.sessions.length')==1 and page.evaluate('state.sessions[0].items[0].actualSets')==1
  assert not page.evaluate('state.sessions[0].items[0].completed') and page.evaluate('state.sessions[0].finishOutcome')=='partial'
  page.evaluate('saveWorkout()');assert page.evaluate('state.sessions.length')==1
  page.locator('[data-edit-history]').tap();page.locator('[data-edit-movement="history:0"]').tap();page.locator('[data-hset="0:0:reps"]').fill('2');page.locator('[data-hset="0:0:reps"]').dispatch_event('change');saved=snapshot()
  page.evaluate('''()=>{window.nativeSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k===KEY)throw Error('Injected correction quota failure');return nativeSet.call(this,k,v)}}''')
  page.locator('#save-correction').tap();assert snapshot()==saved and not page.evaluate('state.sessions[0].corrections?.length')
  page.evaluate('()=>{Storage.prototype.setItem=nativeSet;}');page.locator('#save-correction').tap();assert page.evaluate('state.sessions[0].corrections.length')==1
  reader=context.new_page();reader.goto(base);reader.wait_for_function('storageReady && !storageWritable');reader.get_by_text('Recently recorded',exact=True).tap();reader.locator('[data-history-view]').tap();assert reader.evaluate('tab')=='progress';assert reader.locator('[data-edit-history]').is_disabled();reader.close()
  page.evaluate('navigator.serviceWorker.ready.then(()=>true)');context.set_offline(True);page.reload();page.wait_for_function('storageReady && storageWritable');page.locator('[data-tab="progress"]').tap();page.locator('[data-history]>summary').tap();page.locator('[data-edit-history]').tap();page.locator('[data-edit-movement="history:0"]').tap();page.locator('[data-hset="0:0:skipped"]').check();page.locator('#save-correction').tap();assert page.evaluate('state.sessions[0].items[0].actualSets')==0
  assert page.evaluate('state.sessions[0].corrections.length')==2 and page.evaluate('E.plan(state).slot')==0
  page.locator('[data-tab="settings"]').tap();before=snapshot();bad=page.evaluate('JSON.parse(JSON.stringify(state))');bad['sessions'][0]['corrections'][0]['before']['items'][0]['sets'][0]['weight']=-5
  page.locator('#import').set_input_files({'name':'malformed-correction.json','mimeType':'application/json','buffer':json.dumps(bad).encode()});page.wait_for_function('testAlerts.some(m=>m.startsWith("Cannot restore backup"))');assert snapshot()==before
  assert not errors,errors
  print('PASS: set add/remove, partial choice/draft reload, failed atomic finish rollback/retry, duplicate guard, failed correction rollback/retry, read-only second tab, offline correction and malformed audit rejection',flush=True)
  browser.close()
finally:server.shutdown();server.server_close();thread.join()
