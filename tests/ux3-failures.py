"""Activities + partial queue + corrections under storage faults and real tab locks."""
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
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.add_init_script('window.testAlerts=[];window.alert=m=>testAlerts.push(m)');base=f'http://127.0.0.1:{server.server_port}/';page.goto(base);page.wait_for_function('storageReady && storageWritable')
  def snapshot():return page.evaluate('({state:localStorage.getItem(KEY),draft:localStorage.getItem(DRAFT)})')
  page.locator('[data-tab="settings"]').tap();page.locator('#advanced-settings>summary').tap();page.locator('#program-block').select_option('hingePractice');page.get_by_text('Prerequisite skills',exact=True).tap();page.locator('[data-skill="hingePattern"]').check();page.locator('#save-programming').tap();page.locator('[data-tab="today"]').tap()
  identity=page.evaluate('C.key(state)');page.locator('#activity-form>summary').tap();page.locator('#activity-duration').fill('10');page.locator('#activity-replaces').uncheck();before=snapshot()
  page.evaluate('''()=>{window.nativeSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k===KEY)throw Error('Injected activity failure');return nativeSet.call(this,k,v)}}''')
  page.locator('#save-activity').tap();assert snapshot()==before and page.evaluate('(state.activities||[]).length')==0
  page.evaluate('()=>{Storage.prototype.setItem=nativeSet}');page.locator('#save-activity').tap();assert page.evaluate('state.activities.length')==1 and page.evaluate('C.key(state)')==identity
  page.locator('#start').tap();page.locator('[data-stage="work"]').tap();page.locator('[data-edit-movement="active:0"]').tap();page.locator('.partial-set>summary').first.tap();page.locator('[data-set="0:0:done"]').check();page.locator('[data-set="0:0:reps"]').fill('1');page.locator('[data-set="0:0:reps"]').dispatch_event('change')
  page.locator('#finish-options>summary').tap();page.locator('#finish-kind').select_option('partial');page.reload();page.wait_for_function('storageReady && storageWritable');assert page.locator('#finish-kind').input_value()=='partial';before=snapshot()
  page.evaluate('''()=>{window.nativeRemove=Storage.prototype.removeItem;Storage.prototype.removeItem=function(k){if(k===DRAFT)throw Error('Injected paired save failure');return nativeRemove.call(this,k)}}''')
  page.locator('#save-workout').tap();assert snapshot()==before and page.evaluate('state.sessions.length')==0
  page.evaluate('()=>{Storage.prototype.removeItem=nativeRemove}');page.locator('#save-workout').tap();assert page.evaluate('state.sessions.length')==1 and page.evaluate('C.key(state)')==identity
  assert not page.evaluate('state.sessions[0].items[0].completed');page.evaluate('saveWorkout()');assert page.evaluate('state.sessions.length')==1
  page.locator('[data-edit-history]').tap();page.locator('[data-edit-movement="history:0"]').tap();page.locator('[data-hset="0:0:reps"]').fill('2');page.locator('[data-hset="0:0:reps"]').dispatch_event('change');before=snapshot()
  page.evaluate('''()=>{window.nativeSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k===KEY)throw Error('Injected correction failure');return nativeSet.call(this,k,v)}}''')
  page.locator('#save-correction').tap();assert snapshot()==before and not page.evaluate('state.sessions[0].corrections?.length')
  page.evaluate('()=>{Storage.prototype.setItem=nativeSet}');page.locator('#save-correction').tap();assert page.evaluate('state.sessions[0].corrections.length')==1
  reader=context.new_page();reader.goto(base);reader.wait_for_function('storageReady && !storageWritable');reader.locator('[data-tab="progress"]').tap();reader.locator('.history-table [data-history-view]').tap();assert reader.locator('[data-edit-history]').is_disabled();reader.locator('.history-table [data-edit-activity]').tap();assert reader.locator('#save-activity').is_disabled();reader.close()
  page.locator('[data-tab="settings"]').tap();page.locator('#advanced-settings').evaluate('(el)=>el.open=true');before=snapshot();bad=page.evaluate('JSON.parse(JSON.stringify(state))');bad['activities'][0]['duration']=-1
  page.locator('#import').set_input_files({'name':'bad-activity.json','mimeType':'application/json','buffer':json.dumps(bad).encode()});page.wait_for_function('testAlerts.some(x=>x.startsWith("Cannot restore backup"))');assert snapshot()==before
  page.evaluate('navigator.serviceWorker.ready.then(()=>true)');context.set_offline(True);page.reload();page.wait_for_function('storageReady && storageWritable');assert page.evaluate('state.activities.length===1 && state.sessions[0].corrections.length===1')
  assert not errors,errors;print('PASS: activity write rollback/retry; stable displaced/partial queue; atomic final save rollback/retry; no duplicate; correction rollback/retry; real read-only history/activity tabs; malformed activity import and offline restore',flush=True);browser.close()
finally:server.shutdown();server.server_close();thread.join()
