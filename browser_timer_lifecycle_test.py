from pathlib import Path
from playwright.sync_api import sync_playwright
base=Path(__file__).parent
html=(base/'index.html').read_text().replace('<script src="engine.js"></script>','').replace('<script src="app.js" defer></script>','').replace('<script src="session-timer.js"></script>','').replace('<script src="movement-instruction.js"></script>','').replace('<script src="learning.js"></script>','')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844}); errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 # A localhost origin supplies real browser Web Locks; storage remains simulated.
 page.route('http://localhost:8765/**',lambda route:route.fulfill(status=200 if route.request.url.endswith('/') else 404,body=html if route.request.url.endswith('/') else '',content_type='text/html'))
 page.goto('http://localhost:8765/')
 for css in ['styles.css','interface-polish.css']:page.add_style_tag(content=(base/css).read_text())
 page.add_script_tag(content="const __store={};Object.defineProperty(window,'localStorage',{value:{getItem:k=>__store[k]??null,setItem:(k,v)=>{__store[k]=String(v)},removeItem:k=>{delete __store[k]}}});")
 for js in ['engine.js','session-timer.js','movement-instruction.js','learning.js','app.js']:page.add_script_tag(content=(base/js).read_text())
 page.evaluate("state.timerMode='automatic'")
 page.get_by_role('button',name='Start workout').click()
 page.get_by_role('button',name='Warmup complete · start work').click()
 page.evaluate('() => {for(const item of draft.items)for(const set of item.sets)if(!set.weight)set.weight=8;saveDraft();render();}')
 assert page.locator('[data-check]').count()>1
 page.get_by_role('button',name='Complete next set').click()
 assert page.locator('#timer-label').inner_text().startswith('Rest')
 assert page.get_by_role('button',name='Pause').count()==1
 page.locator('[data-check="0:0"]').click()
 assert page.get_by_role('button',name='Pause').count()==0
 assert page.evaluate('draft.clock.kind==="work" && !draft.clock.running')
 page.evaluate('() => {for(const item of draft.items)for(const set of item.sets){set.done=true;set.weight=set.weight||8;}const last=draft.items.at(-1).sets.at(-1);last.done=false;saveDraft();render();}')
 page.get_by_role('button',name='Complete next set').click()
 assert page.get_by_role('heading',name='Working sets complete').count()==1
 assert page.locator('#clock').inner_text()=='00:00'
 assert not errors,errors
 print('PASS: rest after set, undo cancels rest, all-sets completion, no JS errors')
 browser.close()
