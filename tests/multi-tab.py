"""Same-origin real browser tabs: exclusive writes, draft handoff and stale guards."""
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
  context=browser.new_context();context.add_init_script('window.testAlerts=[];window.alert=m=>testAlerts.push(String(m));')
  errors=[]
  def page():
   tab=context.new_page();tab.on('pageerror',lambda e:errors.append(str(e)));tab.on('dialog',lambda d:d.accept());tab.goto(f'http://127.0.0.1:{server.server_port}/');tab.wait_for_function('storageReady');return tab
  def settings(tab):tab.locator('[data-tab="settings"]').click()
  def raw(tab):return tab.evaluate('({state:localStorage.getItem(KEY),draft:localStorage.getItem(DRAFT),journal:localStorage.getItem(JOURNAL)})')
  owner=page();assert owner.evaluate('storageWritable');settings(owner)
  owner.locator('#program-block').select_option('hingePractice');owner.get_by_text('Prerequisite skills',exact=True).click();owner.locator('[data-skill="hingePattern"]').check();owner.locator('#save-programming').click()
  reader=page();assert not reader.evaluate('storageWritable');assert 'read-only' in reader.locator('#storage-notice').inner_text()
  # A reader opening during an unfinished paired write must not roll it back.
  before=raw(owner)
  owner.evaluate('''()=>{localStorage.setItem(JOURNAL,JSON.stringify({version:1,state:localStorage.getItem(KEY),draft:localStorage.getItem(DRAFT)}));localStorage.setItem(KEY,JSON.stringify({...state,defaultMinutes:90}));}''')
  during=page();assert not during.evaluate('storageWritable') and during.evaluate('state.defaultMinutes')==45
  assert json.loads(raw(owner)['state'])['defaultMinutes']==90 and raw(owner)['journal'] is not None
  owner.evaluate('''()=>{const old=JSON.parse(localStorage.getItem(JOURNAL));restoreTrainingPair(old);localStorage.removeItem(JOURNAL);rememberStorage();}''')
  during.close()
  settings(reader);assert reader.locator('#save-programming').is_disabled()
  payload=owner.evaluate('JSON.stringify(state)')
  reader.locator('#import').set_input_files({'name':'blocked.json','mimeType':'application/json','buffer':payload.encode()});assert raw(owner)==before
  owner.locator('[data-tab="today"]').click();owner.locator('#start').click();owner.get_by_role('button',name='Warmup complete · start work').click();owner.get_by_role('button',name='Complete next set').click();owner.get_by_role('button',name='Pause',exact=True).click()
  reader.locator('[data-tab="today"]').click();reader.wait_for_function('draft?.items[0].sets[0].done===true && draft.clock?.running===false')
  identity=owner.evaluate('draft.id');remaining=owner.evaluate('draft.clock.remaining')
  assert reader.locator('[data-check="0:0"]').is_disabled()
  saved=raw(owner);reader.evaluate('saveWorkout()');assert raw(owner)==saved
  # Closing the owner releases the browser-managed lock. Reload reads the latest draft.
  owner.close();reader.reload();reader.wait_for_function('storageReady && storageWritable')
  assert reader.evaluate('draft.id')==identity and reader.evaluate('draft.clock.remaining')==remaining
  contender=page();assert not contender.evaluate('storageWritable')
  reader.get_by_role('button',name='Complete next set').click();reader.get_by_role('button',name='Finish main work · cooldown').click();reader.locator('#save-workout').click()
  contender.wait_for_function('state.sessions.length===1 && draft===null')
  assert reader.evaluate('state.sessions.length')==1
  contender.evaluate('saveWorkout()');reader.evaluate('saveWorkout()');assert reader.evaluate('state.sessions.length')==1
  # An obsolete/uncooperative client changes storage: the owner freezes before overwriting it.
  reader.locator('[data-tab="today"]').click();reader.locator('#start').click();draft_id=reader.evaluate('draft.id')
  contender.evaluate('''()=>{const newer=JSON.parse(localStorage.getItem(KEY));newer.defaultMinutes=60;localStorage.setItem(KEY,JSON.stringify(newer));}''')
  reader.wait_for_function('storageConflict');newer=raw(reader);assert reader.locator('#start').count()==0
  reader.evaluate('saveWorkout()');assert raw(reader)==newer
  assert reader.evaluate('draft.id')==draft_id
  settings(reader)
  with reader.expect_download() as download:reader.locator('#export').click()
  backup=json.loads(Path(download.value.path()).read_text());assert backup['workoutDraft']['id']==draft_id and len(backup['sessions'])==1
  contender.close();reader.reload();reader.wait_for_function('storageReady && storageWritable')
  assert reader.evaluate('state.defaultMinutes')==60 and reader.evaluate('state.sessions.length')==1
  assert reader.evaluate('draft.id')==draft_id
  # Synchronous baseline check also catches a change before its storage event is delivered.
  reader.evaluate('''()=>{localStorage.setItem(KEY,JSON.stringify({...state,defaultMinutes:75}));saveWorkout();}''')
  assert reader.evaluate('storageConflict') and json.loads(raw(reader)['state'])['defaultMinutes']==75
  reader.reload();reader.wait_for_function('storageReady && storageWritable')
  reader.evaluate('navigator.serviceWorker.ready.then(()=>true)');context.set_offline(True);reader.reload();reader.wait_for_function('storageReady && storageWritable')
  assert reader.evaluate('state.sessions.length')==1 and reader.evaluate('draft.id')==draft_id
  context.set_offline(False)
  unsupported=context.new_page();unsupported.add_init_script("Object.defineProperty(navigator,'locks',{value:undefined});")
  unsupported.goto(f'http://127.0.0.1:{server.server_port}/');unsupported.wait_for_function('storageReady')
  assert unsupported.evaluate('storageLockUnavailable && !storageWritable')
  assert 'current browser' in unsupported.locator('#storage-notice').inner_text()
  unchanged=raw(reader);unsupported.evaluate('saveWorkout()');assert raw(reader)==unchanged
  assert not errors,errors
  print('PASS: exclusive tab writer; read-only import/save guards; live draft/set/timer view; close/reload handoff; duplicate save protection; external/stale write detection; backup; offline ownership; unsupported-lock read-only mode',flush=True)
  browser.close()
finally:
 server.shutdown();server.server_close();thread.join()
