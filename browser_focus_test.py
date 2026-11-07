"""In-memory Chromium DOM test. Not an installed-PWA/offline test."""
from pathlib import Path
from playwright.sync_api import sync_playwright
base=Path(__file__).parent
html=(base/'index.html').read_text()
html=html.replace('<script src="engine.js"></script>','').replace('<script src="app.js" defer></script>','').replace('<script src="session-timer.js"></script>','').replace('<script src="movement-instruction.js"></script>','').replace('<script src="learning.js"></script>','').replace('<script src="notebook.js"></script>','')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844})
 errors=[]
 page.on('pageerror',lambda err:errors.append(str(err)))
 # A localhost origin supplies real browser Web Locks; storage remains simulated.
 page.route('http://localhost:8765/**',lambda route:route.fulfill(status=200 if route.request.url.endswith('/') else 404,body=html if route.request.url.endswith('/') else '',content_type='text/html'))
 page.goto('http://localhost:8765/')
 page.add_style_tag(content=(base/'styles.css').read_text())
 page.add_style_tag(content=(base/'interface-polish.css').read_text())
 page.add_script_tag(content="const __store={};Object.defineProperty(window,'localStorage',{value:{getItem:k=>__store[k]??null,setItem:(k,v)=>{__store[k]=String(v)},removeItem:k=>{delete __store[k]}}});")
 page.add_script_tag(content=(base/'engine.js').read_text())
 page.add_script_tag(content=(base/'session-timer.js').read_text())
 page.add_script_tag(content=(base/'movement-instruction.js').read_text())
 page.add_script_tag(content=(base/'learning.js').read_text())
 page.add_script_tag(content=(base/'notebook.js').read_text())
 page.add_script_tag(content=(base/'app.js').read_text())
 page.get_by_role('button',name='Start workout').click()
 page.get_by_role('button',name='Warmup complete · start work').click();page.locator('[data-editor],details#workout-focus').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
 assert page.get_by_role('button',name='Complete next set').count()==1
 assert page.locator('[role="progressbar"]').get_attribute('aria-valuenow')=='0'
 page.locator('#workout-focus').evaluate('(el)=>el.open=true');page.get_by_role('button',name='Complete next set').click()
 assert page.locator('[role="progressbar"]').get_attribute('aria-valuenow')=='0'
 assert 'valid weight' in page.locator('#focus-validation').inner_text()
 page.locator('[data-set="0:0:weight"]').fill('12')
 page.locator('[data-set="0:0:weight"]').dispatch_event('change')
 page.locator('#workout-focus').evaluate('(el)=>el.open=true');page.get_by_role('button',name='Complete next set').click()
 assert page.locator('[role="progressbar"]').get_attribute('aria-valuenow')=='1'
 assert page.locator('[data-check="0:0"]').inner_text()=='✓'
 page.locator('#workout-focus').evaluate('(el)=>el.open=true');page.get_by_role('button',name='Complete next set').click()
 assert page.locator('[role="progressbar"]').get_attribute('aria-valuenow')=='1'
 page.locator('[data-set="0:1:weight"]').fill('12')
 page.locator('[data-set="0:1:weight"]').dispatch_event('change')
 page.locator('#workout-focus').evaluate('(el)=>el.open=true');page.get_by_role('button',name='Complete next set').click()
 assert page.locator('[role="progressbar"]').get_attribute('aria-valuenow')=='2'
 page.locator('[data-check="0:0"]').click()
 assert page.locator('[role="progressbar"]').get_attribute('aria-valuenow')=='1'
 assert page.get_by_role('button',name='Complete next set').count()==1
 assert not errors,errors
 print('PASS: focus quick-log, progress, undo, no JavaScript exceptions')
 browser.close()
