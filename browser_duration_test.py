from pathlib import Path
from playwright.sync_api import sync_playwright
base=Path(__file__).parent
html=(base/'index.html').read_text().replace('<script src="engine.js"></script>','').replace('<script src="app.js" defer></script>','')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':844}); errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 # A localhost origin supplies real browser Web Locks; storage remains simulated.
 page.route('http://localhost:8765/**',lambda route:route.fulfill(status=200 if route.request.url.endswith('/') else 404,body=html if route.request.url.endswith('/') else '',content_type='text/html'))
 page.goto('http://localhost:8765/')
 for css in ['styles.css','interface-polish.css']:page.add_style_tag(content=(base/css).read_text())
 page.add_script_tag(content="const __store={};Object.defineProperty(window,'localStorage',{value:{getItem:k=>__store[k]??null,setItem:(k,v)=>{__store[k]=String(v)},removeItem:k=>{delete __store[k]}}});")
 for js in ['engine.js','app.js']:page.add_script_tag(content=(base/js).read_text())
 page.locator('[data-tab="settings"]').first.click()
 page.locator('#default-minutes').select_option('60')
 page.locator('#save-duration').click()
 page.locator('[data-tab="today"]').first.click()
 assert page.locator('#today-minutes').input_value()=='60'
 page.locator('#today-minutes').select_option('15')
 assert page.locator('#today-minutes').input_value()=='15'
 assert page.evaluate('currentPlan().budget.total')==15
 if page.locator('#start').count()==0:
  assert page.get_by_text('No complete movement fits',exact=False).count()>0
  page.locator('#today-minutes').select_option('60')
 assert page.locator('#start').count()==1
 page.locator('#today-minutes').select_option('60')
 page.locator('#start').click()
 assert page.locator('[data-timer-mode="warmup"]').count()==1
 assert page.evaluate('draft.plan.budget.total')==60
 page.get_by_role('button',name='Warmup complete · start work').click()
 assert page.locator('section.exercise').count()==page.evaluate('draft.plan.items.length')
 assert page.locator('#workout-overview').count()==1
 assert not errors,errors
 print('PASS duration: settings default, today override, short-session handling, start, overview; no JS errors')
 b.close()
