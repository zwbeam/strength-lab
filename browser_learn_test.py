from pathlib import Path
from playwright.sync_api import sync_playwright
base=Path(__file__).parent
html=(base/'index.html').read_text().replace('<script src="engine.js"></script>','').replace('<script src="app.js" defer></script>','').replace('<script src="session-timer.js"></script>','').replace('<script src="movement-instruction.js"></script>','').replace('<script src="learning.js"></script>','')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':844}); errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 # A localhost origin supplies real browser Web Locks; storage remains simulated.
 page.route('http://localhost:8765/**',lambda route:route.fulfill(status=200 if route.request.url.endswith('/') else 404,body=html if route.request.url.endswith('/') else '',content_type='text/html'))
 page.goto('http://localhost:8765/')
 for css in ['styles.css','interface-polish.css']:page.add_style_tag(content=(base/css).read_text())
 page.add_script_tag(content="const __store={};Object.defineProperty(window,'localStorage',{value:{getItem:k=>__store[k]??null,setItem:(k,v)=>{__store[k]=String(v)},removeItem:k=>{delete __store[k]}}});")
 for js in ['engine.js','session-timer.js','movement-instruction.js','learning.js','app.js']:page.add_script_tag(content=(base/js).read_text())
 page.locator('[data-tab="learn"]').first.click()
 assert page.locator('[data-tab="learn"]').inner_text().endswith('Learn')
 assert page.locator('[data-learn="atlas"]').count()==0
 assert page.locator('#learn-results [data-learn-move]').count()==31
 page.locator('[data-learn="pathways"]').click();assert page.locator('#focused-pathway').count()==1
 page.locator('[data-learn="exercises"]').first.click();assert page.locator('#programming-knowledge').count()==1
 assert not errors,errors
 print('PASS Learn navigation: Exercises, focused Pathways, preserved Programming; raw archive absent from primary views; no JS errors')
 b.close()
