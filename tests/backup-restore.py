"""Real UI export/restore, storage faults and retry tests with synthetic data."""
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
  page=browser.new_page();page.add_init_script('window.testAlerts=[];window.alert=message=>window.testAlerts.push(String(message));')
  page.on('dialog',lambda d:d.accept());errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/')
  def settings():page.locator('[data-tab="settings"]').click()
  def snapshot():return page.evaluate('({state:localStorage.getItem("strengthlab-data-v33"),draft:localStorage.getItem("strengthlab-draft-v33")})')
  def import_file(payload,name):
   page.evaluate('testAlerts=[]')
   page.locator('#import').set_input_files({'name':name,'mimeType':'application/json','buffer':json.dumps(payload).encode()})
  settings();page.locator('#program-block').select_option('hingePractice');page.get_by_text('Prerequisite skills',exact=True).click();page.locator('[data-skill="hingePattern"]').check();page.locator('#save-programming').click()
  page.locator('[data-tab="today"]').click();page.locator('#start').click();page.get_by_role('button',name='Warmup complete · start work').click();page.get_by_role('button',name='Complete next set').click();page.get_by_role('button',name='Pause',exact=True).click()
  settings()
  with page.expect_download() as download:page.locator('#export').click()
  payload=json.loads(Path(download.value.path()).read_text())
  draft=payload['workoutDraft'];assert draft['id'] and draft['stage']=='work' and draft['items'][0]['sets'][0]['done'] and not draft['clock']['running']
  # Discard must not erase the in-memory draft when storage removal fails.
  active=snapshot();page.locator('[data-tab="today"]').click()
  page.evaluate('''()=>{window.originalRemoveItem=Storage.prototype.removeItem;Storage.prototype.removeItem=function(key){if(key==='strengthlab-draft-v33')throw Error('Injected discard failure');return originalRemoveItem.call(this,key);};testAlerts=[];}''')
  page.locator('#discard').click();assert snapshot()==active and page.evaluate('draft!==null')
  page.evaluate('()=>{Storage.prototype.removeItem=originalRemoveItem;}')
  settings();page.locator('#reset').click();settings();empty=snapshot()
  # Failure to write the journal must leave both original keys untouched.
  page.evaluate('''()=>{window.originalSetItem=Storage.prototype.setItem;Storage.prototype.setItem=function(key,value){if(key==='strengthlab-transaction-v33')throw Error('Injected journal failure');return originalSetItem.call(this,key,value);};}''')
  import_file(payload,'journal-write-failed.json');page.wait_for_function('testAlerts.some(m=>m.includes("Previous saved data was preserved"))');assert snapshot()==empty
  page.evaluate('()=>{Storage.prototype.setItem=originalSetItem;}')
  invalid=json.loads(json.dumps(payload));invalid['workoutDraft']['items'][0]['sets']=[]
  import_file(invalid,'invalid-draft.json');page.wait_for_function('testAlerts.some(m=>m.startsWith("Cannot restore backup:"))');assert snapshot()==empty
  page.evaluate('''()=>{window.originalSetItem=Storage.prototype.setItem;Storage.prototype.setItem=function(key,value){if(key==='strengthlab-draft-v33')throw new DOMException('Injected draft quota failure','QuotaExceededError');return originalSetItem.call(this,key,value);};}''')
  import_file(payload,'failed-draft-write.json');page.wait_for_function('testAlerts.some(m=>m.includes("Previous saved data was preserved"))');assert snapshot()==empty
  assert page.evaluate('draft===null && state.sessions.length===0')
  page.evaluate('()=>{Storage.prototype.setItem=originalSetItem;}')
  import_file(payload,'valid-draft.json');page.wait_for_function('(id)=>draft?.id===id',arg=draft['id'])
  assert page.locator('[data-check="0:0"]').inner_text()=='✓'
  assert page.get_by_role('button',name='Resume',exact=True).count()==1
  assert page.evaluate('draft.clock.remaining')==draft['clock']['remaining']
  page.get_by_role('button',name='Resume',exact=True).click();settings()
  with page.expect_download() as running_download:page.locator('#export').click()
  running_payload=json.loads(Path(running_download.value.path()).read_text());running_clock=running_payload['workoutDraft']['clock'];assert running_clock['running']
  page.locator('#reset').click();settings();import_file(running_payload,'running-timer.json');page.wait_for_function('draft?.clock?.running===true')
  assert page.evaluate('draft.clock.endAt')==running_clock['endAt']
  page.reload();page.wait_for_function('storageReady');assert page.evaluate('draft.id')==draft['id'] and page.evaluate('draft.clock.endAt')==running_clock['endAt']
  page.get_by_role('button',name='Pause',exact=True).click()
  page.get_by_role('button',name='Complete next set').click();page.get_by_role('button',name='Finish main work · cooldown').click();before_save=snapshot()
  page.evaluate('''()=>{window.originalRemoveItem=Storage.prototype.removeItem;Storage.prototype.removeItem=function(key){if(key==='strengthlab-draft-v33')throw new Error('Injected removal failure');return originalRemoveItem.call(this,key);};testAlerts=[];}''')
  page.locator('#save-workout').click();page.wait_for_function('testAlerts.some(m=>m.includes("Previous saved data was preserved"))')
  assert snapshot()==before_save and page.evaluate('state.sessions.length')==0
  page.evaluate('()=>{Storage.prototype.removeItem=originalRemoveItem;}')
  page.locator('#save-workout').click();assert page.evaluate('state.sessions.length')==1
  assert page.evaluate('state.sessions[0].draftId')==draft['id'] and page.evaluate('draft===null')
  # Simulate a process interruption after writing history, before the transaction commits.
  page.evaluate('(previous)=>localStorage.setItem("strengthlab-transaction-v33",JSON.stringify({version:1,...previous}))',before_save)
  # A startup rollback can itself fail: retain the old snapshot and block writes.
  page.add_init_script('''if(sessionStorage.getItem('failRecovery')){const native=Storage.prototype.setItem;Storage.prototype.setItem=function(key,value){if(key==='strengthlab-data-v33')throw Error('Injected startup recovery failure');return native.call(this,key,value);};}''')
  page.evaluate("sessionStorage.setItem('failRecovery','yes')")
  page.reload();page.wait_for_function('storageReady');assert page.evaluate('storageRecoveryIssue && state.sessions.length===0 && draft!==null')
  assert page.get_by_role('alert').count()==1
  assert page.evaluate('localStorage.getItem("strengthlab-transaction-v33")') is not None
  failed_recovery=snapshot();assert page.locator('#save-workout').is_disabled();assert snapshot()==failed_recovery
  page.evaluate("sessionStorage.removeItem('failRecovery')")
  page.reload();page.wait_for_function('storageReady');assert snapshot()==before_save and page.evaluate('state.sessions.length')==0
  assert page.evaluate('draft.id')==draft['id'] and page.evaluate('localStorage.getItem("strengthlab-transaction-v33")') is None
  page.locator('#save-workout').click();assert page.evaluate('state.sessions.length')==1
  settings();saved=snapshot();duplicate=page.evaluate('JSON.parse(JSON.stringify(state))');duplicate['workoutDraft']=draft
  import_file(duplicate,'already-saved-draft.json');page.wait_for_function('testAlerts.some(m=>m.includes("already saved"))');assert snapshot()==saved
  duplicate_history=page.evaluate('JSON.parse(JSON.stringify(state))');duplicate_history['sessions'].append(duplicate_history['sessions'][0])
  import_file(duplicate_history,'duplicated-history.json');page.wait_for_function('testAlerts.some(m=>m.includes("Duplicate workout"))');assert snapshot()==saved
  page.evaluate('navigator.serviceWorker.ready.then(()=>true)');page.context.set_offline(True);page.reload()
  assert page.evaluate('state.sessions.length')==1
  assert not errors,errors
  print('PASS: active draft/timer export and restore; malformed rejection; second-write rollback; failed-save retry; duplicate rejection; offline reload')
  browser.close()
finally:
 server.shutdown();server.server_close();thread.join()
