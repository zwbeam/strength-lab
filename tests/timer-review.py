"""UX review 1: real rendered touch controls, all modes, lifecycle and saved drafts."""
from datetime import datetime,timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
thread=Thread(target=server.serve_forever,daemon=True);thread.start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for mode in ['manual','automatic','hybrid']:
   context=browser.new_context(**p.devices['Pixel 5']);page=context.new_page();errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
   page.clock.install(time=datetime(2026,1,1,12,tzinfo=timezone.utc))
   page.goto(f'http://127.0.0.1:{server.server_port}/');page.wait_for_function('storageReady && storageWritable')
   page.locator('[data-tab="settings"]').tap();assert page.locator('#timer-mode').input_value()=='manual'
   page.locator('#timer-mode').select_option(mode);page.locator('#save-timer-mode').tap()
   page.locator('[data-tab="today"]').tap();page.locator('#start').tap();page.get_by_role('button',name='Warmup complete · start work').tap()
   assert page.locator('#workout-overview').count()==1
   assert page.locator('#clock').evaluate('(e)=>e.tagName')=='BUTTON'
   if mode=='manual':
    assert not page.evaluate('draft.clock.running');initial=page.evaluate('draft.clock.remaining')
    page.get_by_role('button',name='+30 sec',exact=True).tap();assert page.evaluate('draft.clock.remaining')==initial+30
    page.locator('#clock').tap();assert page.evaluate('draft.clock.running')
   before=page.evaluate('timerRemaining(draft.clock)');page.clock.fast_forward(3000)
   assert page.evaluate('timerRemaining(draft.clock)')<=before-2
   page.get_by_role('button',name='Pause',exact=True).tap();paused=page.evaluate('draft.clock.remaining')
   page.clock.fast_forward(5000);assert page.evaluate('draft.clock.remaining')==paused
   page.get_by_role('button',name='Resume',exact=True).tap();page.clock.fast_forward(1000)
   assert page.evaluate('timerRemaining(draft.clock)')<paused
   if mode=='manual':
    page.clock.fast_forward(1000000);assert page.evaluate('draft.clock.kind')=='rest' and not page.evaluate('draft.clock.running')
    page.locator('#timer-primary').tap();assert page.evaluate('draft.clock.running')
   elif mode=='automatic':
    page.clock.fast_forward(50000);assert page.evaluate('draft.clock.kind')=='rest' and page.evaluate('draft.clock.running')
   else:
    page.clock.fast_forward(1000000);assert page.evaluate('draft.clock.awaitConfirmation') and not page.evaluate('draft.clock.running')
    assert page.get_by_role('button',name='Confirm next exercise',exact=True).count()==1
    page.locator('#timer-primary').tap();assert page.evaluate('draft.clock.running')
   assert page.evaluate('draft.items.every(i=>i.sets.every(s=>!s.done))'),'Pacing must not fabricate completed work'
   # Preference changes only affect new sessions and preserve the active clock exactly.
   page.get_by_role('button',name='Pause',exact=True).tap();clock=page.evaluate('JSON.stringify(draft.clock)')
   page.locator('[data-tab="settings"]').tap();page.locator('#timer-mode').select_option('hybrid' if mode!='hybrid' else 'manual');page.locator('#save-timer-mode').tap()
   assert page.evaluate('draft.timerMode')==mode and page.evaluate('JSON.stringify(draft.clock)')==clock
   page.locator('[data-tab="today"]').tap();page.evaluate('navigator.serviceWorker.ready.then(()=>true)')
   context.set_offline(True);page.reload();page.wait_for_function('storageReady && storageWritable')
   assert page.evaluate('draft.timerMode')==mode and page.evaluate('JSON.stringify(draft.clock)')==clock
   assert page.locator('#workout-overview').count()==1
   page.locator('[data-set="0:0:weight"]').fill('8');page.locator('[data-set="0:0:weight"]').dispatch_event('change')
   page.locator('[data-check="0:0"]').tap();assert page.evaluate('draft.items[0].sets[0].done')
   page.locator('[data-check="0:0"]').tap();assert not page.evaluate('draft.items[0].sets[0].done')
   page.get_by_role('button',name='Skip / clear',exact=True).tap()
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
   assert not errors,errors;print('PASS:',mode,'touch countdown/pause/resume/add/skip, no auto-logging, preference snapshot, offline draft and free logging',flush=True)
   context.close()
  # Real wall time while the rendered page is frozen, without a simulated clock.
  context=browser.new_context(**p.devices['Pixel 5']);page=context.new_page();page.on('dialog',lambda d:d.accept());page.goto(f'http://127.0.0.1:{server.server_port}/')
  page.locator('#start').tap();page.get_by_role('button',name='Warmup complete · start work').tap();page.locator('#clock').tap()
  before=page.locator('#clock').inner_text();session=context.new_cdp_session(page);session.send('Page.setWebLifecycleState',{'state':'frozen'})
  other=context.new_page();other.wait_for_timeout(1800);session.send('Page.setWebLifecycleState',{'state':'active'});page.bring_to_front()
  page.wait_for_function('(before)=>document.querySelector("#clock").textContent!==before',arg=before)
  print('PASS: real frozen/background lifecycle reconciles wall-clock countdown on resume',flush=True)
  browser.close()
finally:server.shutdown();server.server_close();thread.join()
