"""Chromium DOM smoke test for timer controls and workout overview; simulated localStorage."""
from pathlib import Path
from playwright.sync_api import sync_playwright
base=Path(__file__).parent
html=(base/'index.html').read_text().replace('<script src="engine.js"></script>','').replace('<script src="app.js" defer></script>','').replace('<script src="session-timer.js"></script>','').replace('<script src="movement-instruction.js"></script>','').replace('<script src="learning.js"></script>','').replace('<script src="notebook.js"></script>','')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 # A localhost origin supplies real browser Web Locks; storage remains simulated.
 page.route('http://localhost:8765/**',lambda route:route.fulfill(status=200 if route.request.url.endswith('/') else 404,body=html if route.request.url.endswith('/') else '',content_type='text/html'))
 page.goto('http://localhost:8765/')
 for css in ['styles.css','interface-polish.css']:page.add_style_tag(content=(base/css).read_text())
 page.add_script_tag(content="const __store={};Object.defineProperty(window,'localStorage',{value:{getItem:k=>__store[k]??null,setItem:(k,v)=>{__store[k]=String(v)},removeItem:k=>{delete __store[k]}}});")
 for js in ['engine.js','session-timer.js','movement-instruction.js','learning.js','notebook.js','app.js']:page.add_script_tag(content=(base/js).read_text())
 page.get_by_role('button',name='Start workout').click()
 page.get_by_role('button',name='Start 7-minute warmup').click()
 assert page.locator('#timer-label').inner_text()=='Warmup'
 page.get_by_role('button',name='Pause').click()
 assert page.get_by_role('button',name='Resume').count()==1
 before=page.locator('#clock').inner_text()
 page.get_by_role('button',name='+30 sec').click()
 assert page.locator('#clock').inner_text()!=before
 page.get_by_role('button',name='Resume').click()
 page.get_by_role('button',name='Warmup complete · start work').click();page.locator('[data-editor],details#workout-focus').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
 assert page.locator('.notebook-exercise').count()>=1
 assert page.get_by_role('button',name='Complete next set').count()==1
 assert page.get_by_role('button',name='Pause').count()==0
 page.get_by_role('button',name='Skip / clear').click()
 assert page.evaluate('draft.clock.kind==="rest" && !draft.clock.running')
 assert not errors,errors
 print('PASS: timer start, pause, extend, resume, stage transition, full exercise overview, no JavaScript exceptions')
 browser.close()
